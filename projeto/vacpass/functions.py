import vacpass

def calcula_dict2(cartao):
    vacinas_user = vacpass.models.ControleVencimento.objects.filter(cartao=cartao).order_by('dose')
    dose_dict = {}
    for vac in vacinas_user:

        data_validade = vac.validade()
        vacina_nome = vac.dose.vacina.nome
        if vacina_nome in dose_dict:
            dose_dict[vacina_nome].append([vac.dose, vac.data.strftime("%d/%m/%y"), data_validade.strftime("%d/%m/%y"),
                                           vac.dose.vacina.num_doses()])
        else:
            dose_dict[vacina_nome] = [[vac.dose, vac.data.strftime("%d/%m/%y"), data_validade.strftime("%d/%m/%y"),
                                       vac.dose.vacina.num_doses()]]

    return dose_dict

# Calculo das novas vacinas de um usuario
def calcula_novas_vacinas2(dose_dict=False):
    if not dose_dict:
        pass

    vacinas = []
    all_vac = vacpass.models.Vacina.objects.all()

    for v in all_vac:
        if not (v.nome in dose_dict):
            vacinas.append(v)

    return vacinas