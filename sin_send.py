import matplotlib.pylab as plt
import numpy as np
import can, os, time

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
    whole = int(whole)
    dec = int(dec)
    
    if whole < 0:
        whole = whole*(-1)
    
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


  
def start_procedure(buff):
    #os.system('sudo ip link set can0 type can bitrate 100000')
    #os.system('sudo ifconfig can0 up')

    #can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

    counter = 0
    
    while(True):
        counter +=1
        if counter == 40:
            counter = 0
        time.sleep(1)
        
        
        #can0.send(buff[counter])
        
    #os.system('sudo ifconfig can0 down')

def main():
    
    tablica = np.linspace(-np.pi, np.pi, 160)
    tablica = np.sin(tablica)*2

    list_to_send = list()

    for value in tablica:
        list_to_send.append(coding(value))
    
    list_to_send = podziel_liste(list_to_send, 4)
    
    buff = list()
    for messages in list_to_send():
        pack = list()
        for data in messages:
            pack.append(int(data[0]))
            pack.append(int(data[1]))
        msg = can.Message(arbitration_id=0x123, data=bytearray(pack), is_extended_id=False)
        buff.append(msg)

    start_procedure(buff)

main()
    
