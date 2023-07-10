import os, time, can
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

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




os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

#msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
msg = can0.recv(1)
counter = 0
tok = time.time()

list_to_plot = list(range(160))


xdata = list(range(160))

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(-1,1)
line1, =ax.plot(xdata,list_to_plot)

while (True):
    
    msg = can0.recv(1)
    
  
    
    if msg is None:
        tik = time.time()
        print(f'Timeout occurred, no message.Time since last message:{tik-tok}')
    else:
        tok = time.time()
        #num_of_data = int(msg.dlc/2)
        for i in range(int(msg.dlc/2)):
            
            num = decoding(msg.data[(i*2)+0],msg.data[(i*2)+1])
            
            
            lista = list()
            lista.append(num)
            list_to_plot = list_to_plot[1:] + lista
        print(msg)
                
    line1.set_ydata(list_to_plot)
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    
    
    
    
    if msg == None:
        counter += 1
    else:
        counter = 0
    
    
   
    
os.system('sudo ifconfig can0 down')