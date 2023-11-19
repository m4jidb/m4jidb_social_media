from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField


class User(AbstractUser):
    """
    User model that extends the AbstractUser model from Django's auth system.
    """
    phone = models.CharField(max_length=11, null=True, blank=True, unique=True)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    deleted_reason = models.TextField(null=True, blank=True)

    @property
    def full_name(self) -> str:
        """Returns the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    @property
    def location(self) -> str:
        """Returns the location of the user."""
        return f"{self.city}, {self.state}, {self.country}"

    def __repr__(self) -> str:
        """Returns a string representation of the user."""
        return f"<User: {self.username}>"

    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
        verbose_name = "User"
        verbose_name_plural = "Users"


class ProfileImage(models.Model):
    """
    ProfileImage model that represents a user's profile image.
    """
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_images")
    image_file = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        quality=75,
        upload_to='profile_img/',
        blank=True,
    )
    alt = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = "ProfileImage"
        verbose_name_plural = "ProfileImages"

    def delete(self, *args, **kwargs):
        """Deletes the image file before deleting the model instance."""
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        """Returns a string representation of the profile image."""
        return self.alt if self.alt else "None"
