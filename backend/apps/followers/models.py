from django.conf import settings
from django.db import models

from core.models import BaseModel


class Follower(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner'
    )
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'], name='unique_together'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} follows {self.user}'

