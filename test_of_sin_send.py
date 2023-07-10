import matplotlib.pylab as plt
import numpy as np
import can, os, time


def twos_complement(x):
    
    if x < 0 and x > -127:
        x = ~x
        x = x+129
        return x
    elif (x < -127):
        print("Error invalid value")
        return 0
    elif(x < 128 and x >= 0):
        return x
    
def reverse_twos_complement(x):
    if type(x) != int:
        x = int(x, 2)
    if x >128:
        x = x-129
        x = ~x
    return x

def podziel_liste(lista, rozmiar):
    return[lista[i:i+rozmiar] for i in range(0,len(lista), rozmiar)]
def odpakowacz(x, y):
    x =str(x)
    y = str(y)
    num = x +"."+y
    return float(num)
#-----------------------------------------------------------------------------------------------------------# 
tested_value = '04'
test_value = int(tested_value)
print(test_value)

tablica = np.linspace(-np.pi, np.pi, 160)
tablica = np.sin(tablica)*1


list_to_send = list()
list_to_send_check= list()
    
for i in tablica:
    i = round(i,2)
    list_to_send_check.append(i)
    whole, dec = str(i).split(".")
    #print(f"dec = {dec}")
    whole = twos_complement(int(whole))
    dec = twos_complement(int(dec))
    table_tuple = (whole, dec)

    list_to_send.append(table_tuple)

    
podzielone_listy = podziel_liste(list_to_send, 4)
magiczna_lista = list()
for lists in podzielone_listy:
        for tuples in lists:
            whole = reverse_twos_complement(tuples[0])
            dec = reverse_twos_complement(tuples[1])
            num = odpakowacz(whole, dec)
            magiczna_lista.append(num)  
plt.plot(magiczna_lista)
plt.show()  
buff = list()
for messages in podzielone_listy:
    pack = list()
    for data in messages:
        pack.append(int(data[0]))
        pack.append((data[1]))
    msg = can.Message(arbitration_id=0x123, data=bytearray(pack), is_extended_id=False)
    buff.append(msg)
