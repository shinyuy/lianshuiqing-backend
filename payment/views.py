from .models import Payment
from .serializers import PaymentSerializer

from django.http import JsonResponse
import json
from rest_framework import permissions
from os import getenv
from users.models import UserAccount

from django.utils import timezone
import uuid
import base64
import os
import aiohttp
import asyncio
from datetime import timedelta
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from order.models import Order, GuestOrder
from decimal import Decimal
from django.conf import settings
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
User = get_user_model()
from dish.models import Dish
from fidelity_card.models import FidelityCardSubscription




COLLECTION_API_USER = os.getenv("MOMO_COLLECTION_API_USER")
COLLECTION_API_KEY = os.getenv("MOMO_COLLECTION_API_KEY")
SUBSCRIPTION_KEY = os.getenv("Collection_MOMO_Ocp_Apim_Subscription_Key")
BASE_URL = os.getenv("MOMO_PRODUCTION_API")
TARGET_ENV = os.getenv("Collection_MOMO_ENV")


async def get_collection_token(session):
    credentials = f"{COLLECTION_API_USER}:{COLLECTION_API_KEY}"
    token = base64.b64encode(credentials.encode()).decode()

    headers = {   
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }
    async with session.post(f"{BASE_URL}/collection/token/", json={"providerCallbackHost": "https://lianshuiqing.com"}, headers=headers) as response:
        response.raise_for_status()
        data = await response.json()
        return data["access_token"]


async def request_to_pay(session, access_token, reference_id, phone, amount, item_names):
    url = f"{BASE_URL}/collection/v1_0/requesttopay"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "X-Target-Environment": TARGET_ENV,
        "X-Reference-Id": reference_id,
    }

    payload = {
        "amount": str(amount),
        "currency": "XAF",
        "externalId": str(uuid.uuid4().int % 1000000),
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": f"237{phone}",
        },
        "payerMessage": item_names,
        "payeeNote": item_names,
    }

    async with session.post(url, json=payload, headers=headers) as response:
        return response.status == 202


async def poll_payment_status(session, access_token, reference_id, max_wait_seconds=300):
    url = f"{BASE_URL}/collection/v1_0/requesttopay/{reference_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "X-Target-Environment": TARGET_ENV,
    }

    elapsed = 0
    interval = 5  

    while elapsed < max_wait_seconds:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                status = data.get("status")
                if status == "SUCCESSFUL":
                    return "SUCCESSFUL"
                elif status == "FAILED":
                    return "FAILED"

        await asyncio.sleep(interval)
        elapsed += interval

    return "TIMEOUT"



def calculate_total(items):
        total = 0
        for item in items:
            dish = Dish.objects.get(id=item['id'])
            total += dish.price * item['quantity']
        return total    


class MomoCartPaymentApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print("11111111111111111111111111111111111111111111111111111111111111")
        print(request.data)
        phone = request.data.get("phone")
        amount = request.data.get("amount")
        items = request.data.get("items")  # list of item names or objects
        print(items)
        is_authenticated = request.user.is_authenticated
        user = request.user
        guest = request.data.get("guest")
        branch = request.data.get("branch")
        order_type = request.data.get("order_type")
        notes = request.data.get("notes")
        
        if order_type not in ['delivery', 'dine-in', 'takeaway']:
            order_type = "dine-in"  # fallback to safe default
        
        if not all([phone, amount, items]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        reference_id = str(uuid.uuid4())

        try:
            total = calculate_total(items)
            result = async_to_sync(self.handle_payment)(phone, total, items, reference_id, is_authenticated, user, guest, branch, order_type, notes)
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500, safe=False)

    async def handle_payment(self, phone, total, items, reference_id, is_authenticated, user, guest, branch, order_type, notes):
        async with aiohttp.ClientSession() as session:
            guest = guest or {}
            token = await get_collection_token(session)
            item_names = ', '.join([item.get('name', 'Item') for item in items])
            
            initiated = await request_to_pay(session, token, reference_id, phone, total, item_names)
            
            if not initiated:
                return {"error": "Payment initiation failed"}
  
            status = await poll_payment_status(session, token, reference_id)
            print("11111111111111111111111111111111111111111111111111111111111")
            print(status)
            print("2222222222222222222222222222222222222222222222222222222222222222222")
            
            # if status != "SUCCESSFUL":
            #     return {"error": "Payment not completed"}
  
            payment_method = 'mobile_money'  # or 'cash', 'card'

            print("333333333333333333333333333333333333333333333333333333333333333333333")
            if is_authenticated:
                # Create user order
                
                order = await sync_to_async(Order.objects.create)(
                    user=user,
                    branch=branch,
                    type=order_type,
                    # table_number='A5',
                    total_price=total,
                    notes=notes,
                )


                await sync_to_async(Payment.objects.create)(
                    user=user,
                    order=order,
                    amount=Decimal(total),
                    method=payment_method,
                    is_successful=True
                )
                
                def update_fidelity(user):
                    sub = FidelityCardSubscription.objects.filter(
                        user=user, status="active"
                    ).order_by("-start_date").first()
                    if sub:
                        sub.reset_monthly_orders_if_needed()
                        sub.add_order()
                        return True
                    return False

                updated = await sync_to_async(update_fidelity)(user)
                
                return {"message": "Payment successful", "status": "SUCCESSFUL", "order_id": order.id}

            else:
                # Create guest order (requires you to get guest info from form or payload)
                
                # guest_order = await sync_to_async(GuestOrder.objects.create)(
                #     name=guest.get("name", "Guest"),
                #     phone=phone,
                #     email=guest.get("email", "")
                # )

                # Create a dummy Order linked to guest (with no user)
                order = await sync_to_async(Order.objects.create)(
                    user=None,
                    branch=branch,
                    type=order_type,
                    total_price=total,
                    notes=notes,
                )
                                
                guest_order = await sync_to_async(GuestOrder.objects.create)(
                    name=guest.get("name", "Guest"),
                    phone=phone,
                    email=guest.get("email", ""),
                    order=order
                )
 

                # dummy_user = await sync_to_async(User.objects.filter(is_superuser=True).first)()
                # if not dummy_user:
                #     return {"error": "No dummy superuser found for guest orders"}, 500

                # guest_wrapper_order = await sync_to_async(lambda: Order.objects.create(
                #     user=dummy_user
                # ))()

                await sync_to_async(Payment.objects.create)(
                    user=None,
                    order=order,
                    amount=Decimal(total),
                    method=payment_method,
                    is_successful=True
                )
                return {"message": "Payment successful", "status": "SUCCESSFUL", "order_id": guest_order.id}

































async def get_orange_token(session):
    username = os.getenv("OM_USERNAME")
    password = os.getenv("OM_PASSWORD")
    x_auth_token = os.getenv("OM_X_AUTH_TOKEN")

    if not all([username, password, x_auth_token]):
        return {"error": "Missing required environment variables"}

    token_bytes = f"{username}:{password}".encode("utf-8")
    base64_token = base64.b64encode(token_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {base64_token}",
        "X-AUTH-TOKEN": x_auth_token,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    async with session.post(
        "https://api-s1.orange.cm/token",
        data="grant_type=client_credentials",
        headers=headers
    ) as response:
        return await response.json()

async def initiate_web_payment(session, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-AUTH-TOKEN": os.getenv("OM_X_AUTH_TOKEN"),
    }

    async with session.post(
        "https://api-s1.orange.cm/omcoreapis/1.0.2/mp/init",
        json={},
        headers=headers
    ) as response:
        return await response.json()

async def make_payment(session, pay_token, number, amount, description):
    order_id = str(uuid.uuid4())[:10]

    payload = {
        "notifUrl": "https://contexxai.com/done",
        "channelUserMsisdn": os.getenv("OM_NUMBER"),
        "amount": str(amount),
        "subscriberMsisdn": number,
        "pin": os.getenv("OM_PIN"),
        "orderId": order_id,
        "description": description,
        "payToken": pay_token,
    }

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-AUTH-TOKEN": os.getenv("OM_X_AUTH_TOKEN"),
    }

    async with session["session"].post(
        "https://api-s1.orange.cm/omcoreapis/1.0.2/mp/pay",
        json=payload,
        headers=headers
    ) as response:
        return await response.json()

async def check_payment_status(session, pay_token, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-AUTH-TOKEN": os.getenv("OM_X_AUTH_TOKEN"),
    }

    url = f"https://api-s1.orange.cm/omcoreapis/1.0.2/mp/paymentstatus/{pay_token}"

    for _ in range(10):
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            status = data.get("data", {}).get("status")
            if status == "SUCCESS":
                return "SUCCESS"
        await asyncio.sleep(5)
    return "TIMEOUT"

async def orange_money_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    body = json.loads(request.body)
    number = body.get("number")
    items = body.get("items", [])
    total = body.get("total")

    if not all([number, items, total]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    item_names = ', '.join([item.get('name', 'Item') for item in items])

    async with aiohttp.ClientSession() as session:
        token_data = await get_orange_token(session)
        access_token = token_data.get("access_token")

        if not access_token:
            return JsonResponse({"error": "Failed to get access token"}, status=500)

        init_data = await initiate_web_payment(session, access_token)
        pay_token = init_data.get("data", {}).get("payToken")

        if not pay_token:
            return JsonResponse({"error": "Failed to initiate payment"}, status=500)

        session_context = {"session": session, "access_token": access_token}
        pay_result = await make_payment(session_context, pay_token, number, total, item_names)

        if pay_result.get("data", {}).get("status") == "PENDING":
            status = await check_payment_status(session, pay_token, access_token)

            if status == "SUCCESS":
                Payment.objects.create(
                    phone_number=number,
                    transaction_id=pay_token,
                    amount=total,
                    items=json.dumps(items),
                    method="Orange Money",
                    status="SUCCESSFUL"
                )
            return JsonResponse({"status": status})
        else:
            return JsonResponse({"error": "Payment initiation failed"}, status=500)
