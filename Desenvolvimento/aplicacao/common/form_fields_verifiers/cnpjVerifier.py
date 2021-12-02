"""
    * Métodos focados na verificação de CNPJ válido
    * Favor manter em ordem alfabética
"""

def formatCNPJ(cnpj):
    return cnpj.replace('.', '').replace('/', '').replace('-', '')


def getIntListDigits(cnpj):
    digits = []
    for digit in cnpj:
        digits.append(int(digit))
    return digits


def getVerifierDigit(weightDigits):
    digitSum = sum(weightDigits)
    remainder = digitSum % 11
    verifierDigit = 11 - remainder
    if remainder < 2:
        verifierDigit = 0
    return verifierDigit


def getVerifierDigit1(digits):
    weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weightDigits = digits[0:12]
    for i in range(len(weightDigits)):
        weightDigits[i] = weight[i] * weightDigits[i]
    return getVerifierDigit(weightDigits)


def getVerifierDigit2(digits, verifierDigit1):
    weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weightDigits = digits[0:12]
    weightDigits.append(verifierDigit1)
    for i in range(len(weightDigits)):
        weightDigits[i] = weight[i] * weightDigits[i]
    return getVerifierDigit(weightDigits)


def isCNPJinValidFormat(cnpj):
    if len(cnpj) != 14:
        return False
    if cnpj.isdigit() is False:
        return False
    return True


def isCNPJValid(cnpj):
    cnpj = formatCNPJ(cnpj)
    if isCNPJinValidFormat(cnpj) is False:
        return False
    intDigits = getIntListDigits(cnpj)
    verifierDigit1 = getVerifierDigit1(intDigits)
    verifierDigit2 = getVerifierDigit2(intDigits, verifierDigit1)
    isCNPJValid = intDigits[12] == verifierDigit1 and intDigits[13] == verifierDigit2
    return isCNPJValid

