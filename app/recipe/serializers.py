from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients objects"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    # = References - Getting IDs
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )
    # https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
    # many equals True, because this is a many to many field
    #    allow many
    # queryset to list all ingredients
    #    this will list only the Ids
    # to retrive the full object, we will create a detail API for that
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags',
                  'time_minutes', 'price', 'link'
        )
        read_only_fields = ('id',)
        # ! Good practice to prevent the user from updating the ID


class RecipeDetailSerializer(RecipeSerializer):
    # + we are using the RecipeSerializer as base, because we are
    # + going to user most of the fields and we just need to override
    # + the fields that we need
    """Serializer a recipe detail"""
    ingredients = IngredientSerializer(
        many=True,
        read_only=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
