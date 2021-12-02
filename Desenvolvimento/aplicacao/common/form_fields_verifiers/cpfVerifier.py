"""
    * Métodos focados na verificação de CPF válido
    * Favor manter em ordem alfabética
"""

def formatCpf(cpf):
    if len(cpf) == 11:
        return cpf
    else:
        return cpf.replace('.', '').replace('-', '')


def getIntListDigits(cpf):
    digitos = []
    for digito in cpf:
        digitos.append(int(digito))
    return digitos


def getVerifier1(digitos):
    digitosPeso = digitos[0:9]
    for i in range(9):
        peso = i + 1
        digitosPeso[i] = digitosPeso[i] * peso
    return retornaVerificador(digitosPeso)


def getVerifier2(digitos, verifier1):
    digitosPeso = digitos[0:9]
    digitosPeso.append(verifier1)
    for i in range(10):
        peso = i
        digitosPeso[i] = digitosPeso[i] * peso
    return retornaVerificador(digitosPeso)


def isCPFinValidFormat(cpf):
    if len(cpf) != 11:
        return False
    if cpf.isdigit() is False:
        return False
    return True


def isCpfValid(cpf):
    cpf = formatCpf(cpf)
    if isCPFinValidFormat(cpf) is False:
        return False
    digitos = getIntListDigits(cpf)
    verifierDigit1 = getVerifier1(digitos)
    verifierDigit2 = getVerifier2(digitos, verifierDigit1)
    isCpfValid = digitos[9] == verifierDigit1 and digitos[10] == verifierDigit2
    return isCpfValid


def retornaVerificador(digitosPeso):
    somaDigitos = sum(digitosPeso)
    resto = somaDigitos % 11
    if resto == 10:
        resto = 0
    return resto
