import sys

def verify_card_number(card_number):

    total=0
    card_number = card_number.replace('.', '')
    if len(card_number) != 16:
        return False
    
    # for i in range(0,16,2):
    #     acum=int(card_number[i])*2
    # if (acum > 9):
    #     acum=acum-9
    # total=total+acum
    # for i in range(1,17,2):
    #     total=total+int(card_number[i])
    # if ((total%10) != 0 or total > 150):
    #     return False
    
    return True
