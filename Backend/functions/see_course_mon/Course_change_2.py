from Backend.functions.translate.TranslateMenu import translations


def changemoney(lang):
    while True:
        data = translations[lang]
        coice_user = int(input(data['LoginCardMOney']))
        print(data['Money'])
        print(data['Card'])
        if coice_user == 1:
            money_rate(lang)
        elif coice_user == 2:
            card_rate(lang)
            
def money_rate(lang):
    pass

def card_rate(lang):
    pass