from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Invokes each time a new user is created, and creates a token for them.
    # appears to be redundant here, perhaps may be needed if a new user is created in Admin.
    """
    if created:
        Token.objects.create(user=instance)


