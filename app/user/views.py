from rest_framework import generics
# Import the generics we need the CreateAPIView to create our API
from user.serializers import UserSerializer
# Import the user serializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    # ! all we need to specify in our class is the serializer_class
    # ! and point to the our Serializer
