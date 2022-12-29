from django.conf import settings
from django.db import models
from django_filters import FilterSet, DateFromToRangeFilter


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    favorite_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         through='UserFavorites',
                                         related_name='favorite_advertisement',
                                         )


class UserFavorites(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    advertisements = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
