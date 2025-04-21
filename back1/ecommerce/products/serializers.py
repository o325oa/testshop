from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'category', 
            'name', 
            'slug', 
            'description',
            'price', 
            'available', 
            'stock', 
            'created',
            'updated',
            'image',
            'rating',
            'num_reviews'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created']
        read_only_fields = ['user', 'created']