from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions'
    )

    def clean(self):
        super().clean()
        # Ensure only employees or owners are required to have a restaurant association
        if not self.is_superuser and (self.is_owner or self.is_employee) and self.restaurant is None:
            raise ValidationError(
                "Non-superuser must be associated with a restaurant.")

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.full_clean()  # Ensure validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
