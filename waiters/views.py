from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from users.models import UserAccount
from users.serializers import UserAccountSerializer
from django.conf import settings
import resend
from django.template.loader import render_to_string
from users.permissions import IsAdminOrManager
from django.contrib.auth.models import BaseUserManager
import os

resend.api_key = settings.RESEND_API_KEY


class InviteWaiterApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            first_name = request.data.get('first_name', 'Waiter')
            last_name = request.data.get('last_name', '')
            branch = request.user.branch

            if UserAccount.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists.'}, status=400)

            # Create waiter account with temporary password
            temp_password = UserAccount.objects.generate_random_password()
            waiter = UserAccount.objects.create_user(
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name,
                role='waiter',
                branch=branch
            )
            
            FRONTEND_URL = os.getenv("FRONTEND_URL")
            
            activation_link = f"{FRONTEND_URL}/en/auth/login"
            
            html = f"""  
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
  <h2>You're Invited to Join LIAN SHUI QING</h2>

  <p>Hi {waiter.first_name},</p>

  <p>You’ve been invited to join <strong>LIAN SHUI QING</strong> as a waiter.</p>
  <p>Your temporal password is {temp_password}</p>

  <p>Click the button below to access your account and change your password:</p>

  <p>
    <a href="{activation_link}" 
      style="background-color: #0a7cff; 
             color: #ffffff; 
             padding: 12px 20px; 
             text-decoration: none; 
             border-radius: 5px; 
             font-weight: bold; 
             display: inline-block;">
      Activate Account
    </a>   
  </p>

  <p>Your temporary login email is: <strong>{waiter.email}</strong></p>

  <p>If you were not expecting this invitation, feel free to ignore this message.</p>

  <p>Welcome aboard,<br>
  The LIAN SHUI QING Team<br>
  <a href="https://lianshuiqing.com">https://lianshuiqing.com</a></p>
</body>
</html>
"""


            resend.Emails.send({
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": email,
                "subject": "You're invited to join as a Waiter",
                "html": html,
            })

            return Response({'message': 'Invitation sent successfully.'}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class DeleteWaiterApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]

    def delete(self, request, waiter_id, *args, **kwargs):
        try:
            waiter = UserAccount.objects.get(id=waiter_id, role='waiter')
            waiter.delete()
            return Response({'message': 'Waiter deleted.'}, status=200)
        except UserAccount.DoesNotExist:
            return Response({'error': 'Waiter not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ListWaitersApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]

    def get(self, request, *args, **kwargs):
        try:
            waiters = UserAccount.objects.filter(role='waiter')
            serializer = UserAccountSerializer(waiters, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class GetSingleWaiterApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]

    def get(self, request, waiter_id, *args, **kwargs):
        try:
            waiter = UserAccount.objects.get(id=waiter_id, role='waiter')
            serializer = UserAccountSerializer(waiter)
            return Response(serializer.data, status=200)
        except UserAccount.DoesNotExist:
            return Response({'error': 'Waiter not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



class ChangePasswordApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password or len(new_password) < 6:
            return Response({'error': 'New password must be at least 6 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)