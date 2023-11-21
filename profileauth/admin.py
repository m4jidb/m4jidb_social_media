from django import forms
from django.forms import SelectDateWidget
from django.contrib import admin
from .models import User, ProfileImage
from django.contrib.auth.admin import UserAdmin
from social.models import Post


class UserAdminForm(forms.ModelForm):
    birthday = forms.DateField(widget=SelectDateWidget(years=range(1900, 2024)))

    class Meta:
        model = User
        fields = '__all__'


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 1


class UserPostInline(admin.StackedInline):
    model = Post
    extra = 1
    fields = ('title', 'content', 'status', 'slug', 'published_at', 'category', 'tags', 'likes')
    show_change_link = True


@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserAdminForm
    list_display = ['id', 'username', 'email', 'phone']
    list_display_links = ['id', 'username', 'email', 'phone']
    list_filter = ['date_joined']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-date_joined']
    fieldsets = (
        ('Personal info', {'fields': (
            'username', 'password', 'first_name', 'last_name', 'phone', 'email', 'bio', 'birthday', 'address',
            'country', 'state', 'city', 'deleted_reason'
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),
        ('Important dates', {'fields': (
            'last_login', 'date_joined'
        )}),
    )
    date_hierarchy = 'date_joined'
    raw_id_fields = ['groups', 'user_permissions']
    inlines = [ProfileImageInline, UserPostInline]
