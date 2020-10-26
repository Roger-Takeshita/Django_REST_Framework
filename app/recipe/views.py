from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    # + ListModelMixin adds the option to list the items
    # + CreateModelMixing adds the option to create  an item
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # + Overrite the get_queryset - ListModelMixins
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
        # referencing the queryset above

    # + Overrite the perform_create - ListModelMixins
    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)
        # - we set the user to the authenticated user
        # - use the serializer to format properly and save
