from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, UserFavorites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if self.context['request'].user.groups.filter(name='admin').exists():
            return data

        elif 'status' not in list(data.keys()):
            user = self.context['request'].user
            open_tasks_of_user = Advertisement.objects.filter(status='OPEN', creator=user)
            count_tasks = len(open_tasks_of_user)
            if count_tasks > 10:
                raise ValidationError('Допустимо не более 10 открытых задач на пользователя')

        return data


class FavoritesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, )
    advertisements = AdvertisementSerializer(read_only=True, )

    class Meta:
        model = UserFavorites
        fields = ('id', 'user', 'advertisements',)
