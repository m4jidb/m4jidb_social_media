from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField


class User(AbstractUser):
    """
    User model that extends the AbstractUser model from Django's auth system.
    Additional fields include phone, bio, birthday, address, country, state, city, and deleted_reason.
    """
    # User's phone number
    phone = models.CharField(max_length=11, null=True, blank=True)

    # User's biography
    bio = models.TextField(blank=True)

    # User's birthday
    birthday = models.DateField(null=True, blank=True)

    # User's address
    address = models.TextField(blank=True)

    # User's country
    country = models.CharField(max_length=200, blank=True)

    # User's state
    state = models.CharField(max_length=200, blank=True)

    # User's city
    city = models.CharField(max_length=200, blank=True)

    # Reason for user deletion
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
        # Order users by date joined
        ordering = ['-date_joined']

        # Indexes for faster query performance
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

        # Verbose name for admin site
        verbose_name = "User"
        verbose_name_plural = "Users"


class ProfileImage(models.Model):
    """
    ProfileImage model that represents a user's profile image.
    """
    # Foreign key to a User model
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_images")

    # Resized image field
    image_file = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        quality=75,
        upload_to='profile_img/',
        blank=True,
    )

    # Alt text for image
    alt = models.CharField(max_length=250, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order images by creation date
        ordering = ['-created_at']

        # Index for faster query performance
        indexes = [
            models.Index(fields=['-created_at'])
        ]

        # Verbose name for admin site
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
