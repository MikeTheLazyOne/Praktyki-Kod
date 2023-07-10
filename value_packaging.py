import numpy as np
import matplotlib.pyplot as plt


def isNegative(x):
    if x[0] == '-':
        return True
    else:
        return False
    
def isSmall(x):
    if type(x)==str:
        if x[0] == '0':
            return True
        else:
            return False
    elif type(x)== float:
        if x < 0.1:
            return True
        else:
            return False
def logic(x, y):
    if len(y) == 1:
        y = y + '0'
    if (isNegative(x) == True and isSmall(y) == False):
        y = '1' + y
    elif (isNegative(x) == True and isSmall(y) == True):
        Imp = y[-1]
        y = '21' + Imp
    elif (isNegative(x) == False and isSmall(y) == True):
        y = '2' + y  
    else:
        y = y
    return x, y

def coding(x):
    x = x.round(2)
    
    whole, dec = str(x).split(".")
    whole, dec = logic(whole, dec)
    if x == -1:
        print(f"1st: x = {x}, whole = {whole}, dec = {dec}")
    whole = int(whole)
    dec = int(dec)
    if x == -1:
        print(f"2nd: x = {x}, whole = {whole}, dec = {dec}")
    
    if whole < 0:
        whole = whole*(-1)
    if x == -1:
        print(f"3rd: x = {x}, whole = {whole}, dec = {dec}")
    
    return (whole, dec)

def float_maker(x, y):
    x = str(x)
    y = str(y)
    num = (x+"."+y)
    
    return float(num)


def decoding(x, y):
    num = float()
    if type(x) != int:
        x = int(x, 2)

    if type(y) != int:
        y = int(y, 2)
    
    if (y >= 0 and y < 100):
        num = float_maker(x, y)
        return num
    elif (y >= 100 and y < 200):
        
        y = y - 100
        num = float_maker(x, y)
        return (num*(-1))
    elif (y >= 200 and y < 210):
        
        y = y - 200
        x = str(x)
        y = str(y)
        num = (x+".0"+y)
        num = float(num)
        return num
    elif (y>= 210 and y < 220):
        
        y = y - 210
        x = str(x)
        y = str(y)
        num = (x+".0"+y)
        num = float(num)
        return (num*(-1))
    #print(f"decoding: x = {x}, y = {y}")
    print("You are in ShitHole")

def podziel_liste(lista, rozmiar):
    return[lista[i:i+rozmiar] for i in range(0,len(lista), rozmiar)]



tablica = np.linspace(-np.pi, np.pi, 160)
tablica = np.sin(tablica)*2

list_to_send = list()

for value in tablica:
    list_to_send.append(coding(value))
list_to_check = list_to_send
list_to_send = podziel_liste(list_to_send, 4)
list_check = list()
for elem in list_to_send:
    for data in elem:
        #print(type(data[0]))
        
        num = decoding(data[0], data[1])
        list_check.append(num)

for i in range(len(list_check)-130):
    #print(f"{list_check[i+30]} = {list_to_check[i+30]} = {tablica[i+30]}")
    pass



plt.plot(list_check)
plt.show()