from rest_framework import generics
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# Import ObtainAuthToken
from rest_framework.settings import api_settings
# Import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # + If you need to access the values of REST framework's API settings in
    # +     your project, you should use the api_settings object. For example.
    # + The api_settings object will check for any user-defined settings, and
    # +     otherwise fall back to the default values. Any setting that uses
    # +     string import paths to refer to a class will automatically import
    # +     and return the referenced class, instead of the string literal.
