from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwnerOrReadOnly  # Импортируем ваш кастомный класс

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Используем кастомный permission-класс
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
