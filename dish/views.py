from .models import Dish
from .serializers import DishSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, permissions
from rest_framework.views import APIView
from users.models import UserAccount
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary
from os import getenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.http import JsonResponse
from .models import Dish
from .serializers import DishSerializer

cloudinary.config( 
  cloud_name = getenv('CLOUD_NAME'), 
  api_key = getenv('CLOUD_API_KEY'), 
  api_secret = getenv('CLOUD_API_SECRET'),
#   secure = True
)
   
import cloudinary.uploader
import cloudinary.api

# Import the CloudinaryImage and CloudinaryVideo methods for the simplified syntax used in this guide
from cloudinary import CloudinaryImage
import random

class AddDishApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = UserAccount.objects.get(id=request.user.id)

            name = request.data.get('name')
            description = request.data.get('description')
            history = request.data.get('history')
            preparation = request.data.get('preparation')
            category = request.data.get('category')
            price = request.data.get('price')
            image = request.data.get('image')
            tags = request.data.get('tags', [])  # list of strings

            if not all([name, category, price]):
                return JsonResponse({'error': 'Name, category, and price are required.'}, status=400)

            data = {
                'name': name,
                'description': description,
                'history': history,
                'preparation': preparation,
                'category': category,
                'price': price,
                'image': image,
                'tags': tags,
                'owner': request.user.id  # Optional if you have an owner field
            }

            serializer = DishSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
   
    def get(self, request, *args, **kwargs):
            try:
                dishes = Dish.objects.all()
                serializer = DishSerializer(dishes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
                
        

class GetDishApiView(APIView):
    permission_classes = [permissions.AllowAny]        
    def get(self, request, *args, **kwargs):
        try:
            dishes = Dish.objects.all()
            serializer = DishSerializer(dishes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class GetSingleDishApiView(APIView):
    permission_classes = [permissions.AllowAny]        

    def get(self, request, *args, **kwargs):
        dish_id = kwargs.get('id')
        if not dish_id:
            return JsonResponse({'error': 'Dish ID is required.'}, status=400)

        try:
            dish = Dish.objects.get(id=dish_id)
            serializer = DishSerializer(dish)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Dish.DoesNotExist:
            return JsonResponse({'error': 'Dish not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)        
        
class EditDeleteDishApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]        
      
    def put(self, request, dish_id=None, *args, **kwargs):
        try:
            dish = Dish.objects.get(id=dish_id)
            serializer = DishSerializer(dish, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Dish.DoesNotExist:
            return JsonResponse({'error': 'Dish not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # 🔹 Delete a dish by ID
    def delete(self, request, id=None, *args, **kwargs):
        print(request)
        try:
            dish = Dish.objects.get(id=id)
            dish.delete()
            return Response({'message': 'Dish deleted successfully'}, status=status.HTTP_200_OK)
        except Dish.DoesNotExist:
            return JsonResponse({'error': 'Dish not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)        



def upload_logo(image_path):
  try:
        # Upload the image to Cloudinary
      
        response = cloudinary.uploader.upload(image_path)
        
        # The response contains the URL of the uploaded image
        print(response)
        print("Image uploaded successfully.")
        print("URL: ", response['secure_url'])
        
        return response
  except Exception as e:
        print("Error uploading image: ", str(e))
        return None


class FileApiView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)  # Ensure this is set
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = request.FILES['file']
        uploaded_logo = upload_logo(file_obj)  
        
        return Response({
            'message': 'File uploaded successfully',
            'file': uploaded_logo['secure_url'],  # Return URL to access the file if needed
            'public_id': uploaded_logo['public_id']  # Return URL to access the file if needed
        }, status=status.HTTP_201_CREATED)
    
    # 5. Delete
    # def delete(self, request, data_store_id, *args, **kwargs):
        
    #     user = UserAccount.objects.get(id = request.user.id)
        
       
    #     data_store_instance = self.get_object(data_store_id, request.user.id)
    #     if not data_store_instance:
    #         return Response(
    #             {"res": "Object with data_store id does not exists"}, 
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     data_store_instance.delete()
    #     return Response(
    #         {"res": "Object deleted!"},
    #         status=status.HTTP_200_OK
    #     )