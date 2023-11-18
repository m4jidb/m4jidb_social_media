from django import template

register = template.Library()


@register.filter
def last_image(user):
    return user.profile_images.order_by('-created_at').first()
