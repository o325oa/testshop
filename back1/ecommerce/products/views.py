from rest_framework import viewsets, filters, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created', 'rating']
    ordering = ['-created']
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            
            # Обновляем рейтинг продукта
            reviews = product.reviews.all()
            product.num_reviews = len(reviews)
            product.rating = sum(review.rating for review in reviews) / product.num_reviews
            product.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]