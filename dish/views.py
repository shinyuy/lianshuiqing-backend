from .models import Dish
from .serializers import DishSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, permissions
    
class DishListCreateView(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
class DishListCreateView(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set any defaults or override logic here if needed
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Custom create logic if you want to inspect the incoming data.
        Expected input from frontend (JSON or multipart/form-data if image):
        {
            "name": "Grilled Chicken",
            "description": "Served with spicy sauce",
            "price": 5500.00,
            "category": "main",
            "is_available": true,
            "branch": 1,
            "image": (uploaded image file if using multipart)
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        Retrieve details of a single dish by ID.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Full update of a dish (all fields).
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partial update of a dish (only some fields).
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete a dish by ID.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Dish deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
