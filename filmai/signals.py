from django.db.models.signals import post_save  # signalas
from django.contrib.auth.models import User  # siuntėjas
from django.dispatch import receiver  # gavėjas (dekoratorius)
from .models import Profilis


@receiver(post_save, sender=User)
def create_profile(sender,
                   instance,  # sukurtas User klasės objektas
                   created,  # boolean, kai User obj sukuriamas jis True
                   **kwargs
                   ):
    if created:
        Profilis.objects.create(user=instance)
        # print('kwargs: ', kwargs)