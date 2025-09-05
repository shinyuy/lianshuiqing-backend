from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Branch, FidelityCard
from .serializers import (
  FidelityCardSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from users.models import UserAccount
from .serializers import FidelityCardSerializer
from django.conf import settings
import aiohttp
from asgiref.sync import sync_to_async
import aiohttp
import asyncio
import base64
import os
import uuid
from django.utils.decorators import classonlymethod
from django.shortcuts import get_object_or_404


from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.views import View
from asgiref.sync import async_to_sync, sync_to_async

from .models import FidelityCard, FidelityCardSubscription
from payment.models import Payment
from payment.views import get_collection_token, request_to_pay, poll_payment_status
from fidelity_card.serializers import FidelityCardSerializer, FidelityCardSubscriptionSerializer
from users.models import UserAccount

class FidelityCardApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:  
            data = request.data

            card_type = data.get('card_type')
            if not card_type:
                return JsonResponse({'error': 'Card type is required.'}, status=400)

            if card_type not in dict(FidelityCard.CARD_CHOICES):
                return JsonResponse({'error': 'Invalid card type.'}, status=400)

            branch = None
            branch_id = data.get('branch')
            if branch_id:
                try:
                    branch = Branch.objects.get(id=branch_id)
                except Branch.DoesNotExist:
                    return JsonResponse({'error': 'Branch not found.'}, status=404)

            fidelity_card = FidelityCard.objects.create(
                card_type=card_type,
                description=data.get('description', ''),
                branch_issued=branch,
                monthly_order_requirement=data.get('monthly_order_requirement', 0),
                six_month_points_requirement=data.get('six_month_points_requirement', 0),
                price=data.get('price', 0.00),
                renewal_price=data.get('renewal_price', 0.00),
                reward=data.get('reward', ''),
                raffle_spots=data.get('raffle_spots', 1),
                duration_days=data.get('duration_days', 365)
            )

            serializer = FidelityCardSerializer(fidelity_card)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        try:
            cards = FidelityCard.objects.all()
            serializer = FidelityCardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class DeleteFidelityCardApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            card_id = kwargs.get('id')  # ✅ from URL

            if not card_id:
                return JsonResponse({'error': 'Card ID is required.'}, status=400)

            try:
                card = FidelityCard.objects.get(id=card_id)
            except FidelityCard.DoesNotExist:
                return JsonResponse({'error': 'Card not found.'}, status=404)

            card.delete()
            return JsonResponse({'message': 'Card deleted successfully.'}, status=204)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class UserFidelityCardSubscriptionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """
        Return all fidelity card subscriptions for a given user.
        """
        user = get_object_or_404(UserAccount, id=user_id)
        subscriptions = FidelityCardSubscription.objects.filter(user=user)

        serializer = FidelityCardSubscriptionSerializer(subscriptions, many=True)
        return Response(
            {
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
                "subscriptions": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserActiveFidelityCardSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """
        Return the active fidelity card subscription for a given user.
        """
        user = get_object_or_404(UserAccount, id=user_id)
        subscription = (
            FidelityCardSubscription.objects.filter(user=user, status="active")
            .order_by("-start_date")
            .first()
        )

        if not subscription:
            return Response(
                {"detail": "No active subscription found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FidelityCardSubscriptionSerializer(subscription)
        return Response(
            {
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
                "subscription": serializer.data,
            },
            status=status.HTTP_200_OK,
        )



# -------------------
# MOMO SUBSCRIPTION
# -------------------
class MomoFidelitySubscriptionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.data.get("phone_number")
        card_type = request.data.get("card_type")

        if not phone or not card_type:
            return JsonResponse({"error": "phone_number and card_type are required"}, status=400)

        try:  
            fidelity_card = FidelityCard.objects.get(card_type=card_type)
        except FidelityCard.DoesNotExist:
            return JsonResponse({"error": "Invalid fidelity card type"}, status=404)

        if fidelity_card.price <= 0:
            return JsonResponse({"error": "Invalid card price"}, status=400)

        reference_id = str(uuid.uuid4())

        try:
            result = async_to_sync(self.handle_payment)(
                phone, fidelity_card, reference_id, request.user
            )
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    async def handle_payment(self, phone, fidelity_card, reference_id, user):
        async with aiohttp.ClientSession() as session:
            token = await get_collection_token(session)
            item_name = f"Fidelity Card Subscription: {fidelity_card.get_card_type_display()}"

            initiated = await request_to_pay(
                session, token, reference_id, phone, fidelity_card.price, item_name
            )
            if not initiated:
                return {"error": "Payment initiation failed"}

            status = await poll_payment_status(session, token, reference_id)
            if status != "SUCCESSFUL":
                return {"error": "Payment not completed", "status": status}

            # Record Payment
            await sync_to_async(Payment.objects.create)(
                user=user,
                amount=Decimal(fidelity_card.price),
                method="MoMo",
                is_successful=True,
                transaction_id=reference_id
            )

            # Create FidelityCardSubscription
            subscription = await sync_to_async(FidelityCardSubscription.objects.create)(
                user=user,
                fidelity_card=fidelity_card,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=fidelity_card.duration_days),
                status="active",
                transaction_id=reference_id,
                payment_method="MoMo",
                amount_paid=fidelity_card.price
            )

            return {
                "message": "Subscription successful",
                "status": "SUCCESSFUL",
                "subscription_id": subscription.id,
                "card_type": fidelity_card.card_type,
                "start_date": subscription.start_date,
                "end_date": subscription.end_date,
                "amount_paid": fidelity_card.price
            }




# -------------------
# ORANGE MONEY SUBSCRIPTION
# -------------------
async def get_orange_token(session):
    username = os.getenv("OM_USERNAME")
    password = os.getenv("OM_PASSWORD")
    x_auth_token = os.getenv("OM_X_AUTH_TOKEN")

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


async def make_payment(session_ctx, pay_token, number, amount, description):
    order_id = str(uuid.uuid4())[:10]
    payload = {
        "notifUrl": os.getenv("OM_NOTIF_URL", "https://yourdomain.com/om-fidelity-done"),
        "channelUserMsisdn": os.getenv("OM_NUMBER"),
        "amount": str(amount),
        "subscriberMsisdn": number,
        "pin": os.getenv("OM_PIN"),
        "orderId": order_id,
        "description": description,
        "payToken": pay_token,
    }
    headers = {
        "Authorization": f"Bearer {session_ctx['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-AUTH-TOKEN": os.getenv("OM_X_AUTH_TOKEN"),
    }
    async with session_ctx["session"].post(
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

    for _ in range(10):  # Poll ~50s
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            status = data.get("data", {}).get("status")
            if status == "SUCCESS":
                return "SUCCESS"
        await asyncio.sleep(5)
    return "TIMEOUT"


class OmFidelitySubscriptionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @classonlymethod
    def as_view(cls, **initkwargs):
        return super().as_view(**initkwargs)

    async def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        card_type = request.data.get("card_type")

        if not card_type or not phone_number:
            return JsonResponse({"error": "card_type and phone_number are required"}, status=400)

        try:
            fidelity_card = FidelityCard.objects.get(card_type=card_type)
        except FidelityCard.DoesNotExist:
            return JsonResponse({"error": "Invalid fidelity card type"}, status=404)

        async with aiohttp.ClientSession() as session:
            token_data = await get_orange_token(session)
            access_token = token_data.get("access_token")
            if not access_token:
                return JsonResponse({"error": "Failed to get access token"}, status=500)

            init_data = await initiate_web_payment(session, access_token)
            pay_token = init_data.get("data", {}).get("payToken")
            if not pay_token:
                return JsonResponse({"error": "Failed to initiate payment"}, status=500)

            session_ctx = {"session": session, "access_token": access_token}
            pay_result = await make_payment(
                session_ctx, pay_token, phone_number,
                fidelity_card.price, f"Fidelity Card Subscription - {fidelity_card.card_type}"
            )

            if pay_result.get("data", {}).get("status") == "PENDING":
                status = await check_payment_status(session, pay_token, access_token)
                if status == "SUCCESS":
                    # Save payment
                    await sync_to_async(Payment.objects.create)(
                        user=request.user,
                        amount=Decimal(fidelity_card.price),
                        method="Orange Money",
                        is_successful=True,
                        transaction_id=pay_token
                    )
                    # Create subscription
                    await sync_to_async(FidelityCardSubscription.objects.create)(
                        user=request.user,
                        fidelity_card=fidelity_card,
                        start_date=timezone.now(),
                        end_date=timezone.now() + timedelta(days=fidelity_card.duration_days),
                        status="active",
                        transaction_id=pay_token,
                        payment_method="Orange Money",
                        amount_paid=fidelity_card.price
                    )
                    return JsonResponse({"status": "SUCCESS"}, status=200)
                return JsonResponse({"status": status}, status=200)

            return JsonResponse({"error": "Payment initiation failed"}, status=500)