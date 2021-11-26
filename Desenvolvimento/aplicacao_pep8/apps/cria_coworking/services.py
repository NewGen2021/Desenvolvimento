def getDicionarioAdministradorForm(request) -> dict:
    data = {}
    fields = ["nome", "senha", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    for field in fields:
        data[field] = request.POST[field]
    return data