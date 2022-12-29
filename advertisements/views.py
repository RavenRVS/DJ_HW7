from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, UserFavorites
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer, FavoritesSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['creator', 'status']
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        return []

    @action(detail=True, methods=['post'])
    def add_favorites(self, request, pk=None):
        advertisement = self.get_object()
        user = request.user
        if user == advertisement.creator:
            UserFavorites.objects.update_or_create(advertisements=advertisement, user=user)
        else:
            raise ValidationError('Нельзя добавить в избранное свое объявление')
        return Response({'status': f'favorite set for advertisement ID:{advertisement.pk}'})

    @action(detail=False)
    def favorites(self, request):
        qs = super().get_queryset()
        if request.user.is_anonymous:
            raise ValidationError('Авторизуйтесь для отображения избранного')
        else:
            qs = qs.filter(favorite_by=self.request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            qs = qs.filter(Q(status='OPEN') | Q(status='CLOSED'))
        else:
            qs = qs.filter(Q(status='OPEN') | Q(status='CLOSED') | Q(creator=self.request.user))
        return qs
