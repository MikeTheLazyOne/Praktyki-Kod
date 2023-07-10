import numpy as np

def isNegative(x):
    if x[0] == '-':
        return True
    else:
        return False
    
def isSmall(x):
    if x[0] == '0':
        return True
    else:
        return False
def logic(x, y):
    if len(y) == 1:
        y = y + '0'
    if isNegative(x) == True and isSmall(y) == False:
        y = '1' + y
    elif isNegative(x) == True and isSmall(y) == True:
        Imp = y[-1]
        y = '21' + Imp
    elif isNegative == False and isSmall == True:
        y = '2' + y
    else:
        y = y
    return x, y

def coding(x):
    x = x.round(2)
    whole, dec = str(x).split(".")
    whole, dec = logic(whole, dec)
    return (int(whole), int(dec))
    
def decoding(x):
    # ToDo
    pass

tablica = np.linspace(-np.pi, np.pi, 160)
tablica = np.sin(tablica)

list_to_send = list()
print(f"Co z tobą jest nie tak {tablica[5]}")
for value in tablica:
    list_to_send.append(coding(value))
print(list_to_send)