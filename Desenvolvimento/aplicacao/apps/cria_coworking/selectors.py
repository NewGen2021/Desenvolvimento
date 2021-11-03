import cria_coworking.models as m

def is_adm_duplicated(cpf_cnpj):
    return m.Administrador.objects.filter(
        cnpj = cpf_cnpj
    ).exists()