
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import user_logged_in
from django.db.models.signals import pre_save
from django.dispatch import receiver

from vacpass.models import ControleVencimento, DoseVacina


@receiver(user_logged_in)
def login_action(sender, user, request, **kwargs):
    messages.info(request, "Usuario autenticado com sucesso")
    c = user.usuario.cartao
    for v in c.controlevencimento_set.all():
        dias = v.dias_para_renovacao().days
        if dias < 0:
            messages.warning(request, "A vacina {} - Dose número {} venceu".format(v.vacina(), v.dose.dose))
        elif dias == 1:
            messages.warning(request, "A vacina {} - Dose número {} vencerá amanha".format(v.vacina(), v.dose.dose))
        elif dias < ControleVencimento.dias_para_notificacao:
            messages.warning(request, "A vacina {} - Dose número {} vencerá em {} dias".format(v.vacina(), v.dose.dose, dias))


@receiver(pre_save, sender=ControleVencimento)
def novo_controle_vencimento_action(sender, instance, *args, **kwargs):
    if not ControleVencimento.objects.filter(id=instance.id).exists() and instance.dias_para_renovacao().days < 0:
        instance.avisado = True


@receiver(pre_save, sender=DoseVacina)
def auto_increment_dose(sender, instance, *args, **kwargs):
    if not DoseVacina.objects.filter(id=instance.id):
        qs = DoseVacina.objects.filter(vacina=instance.vacina)
        proxima_dose = qs.latest('dose').dose + 1 if qs.exists() else 0
        instance.dose = proxima_dose
