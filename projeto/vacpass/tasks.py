from celery import Celery
from django.core.mail import send_mail
from projeto import settings

from vacpass.models import Usuario

app = Celery()


def gerar_texto_proximidade_vencimento(sujeito, vacinas):
    formatador_tabela = "{:<40} {:<8} {:<4}\n"
    texto = "Honorável {},\n\n".format(sujeito)
    texto += "Viemos atravéz desse lhe avisar que as seguintes vacinas em seu cartão VacPass estão por vencer:\n"
    texto += formatador_tabela.format("Vacina", "Dose", "Dias para o vencimento")
    for v in vacinas:
        texto += formatador_tabela.format(str(v.vacina()), str(v.dose.dose), str(v.dias_para_renovacao().days))
    texto += "Sugerimos que voce renove essas vacinas o quanto antes, e ressaltamos que você está correndo risco de " \
             "morte se não o fizer\n\nAtenciosamente,\nVacPass"

    return texto


@app.task
def avisa_proximidade_vacinas():
    usuarios_avisados = []
    for u in Usuario.objects.all():
        c = u.cartao
        vacinas_por_vencer = [v for v in c.controlevencimento_set.all() if not v.avisado and v.dias_para_renovacao().days < 30]
        if vacinas_por_vencer:
            texto = gerar_texto_proximidade_vencimento(u.django_user.first_name, vacinas_por_vencer)
            assunto = 'VacPass - Aviso de proximidade de vencimento de vacina'
            send_mail(assunto, texto, settings.EMAIL_HOST_USER, [u.django_user.email])
            usuarios_avisados.append(u.django_user.email)
            for v in vacinas_por_vencer:
                v.avisado = True
                v.save()

    return usuarios_avisados
