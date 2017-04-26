from django.contrib import messages
from django.contrib.auth import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def login_action(sender, user, request, **kwargs):
    messages.info(request, "Usuario autenticado com sucesso")