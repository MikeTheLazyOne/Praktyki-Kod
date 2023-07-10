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
    
def start_procedure(buff):
    #os.system('sudo ip link set can0 type can bitrate 100000')
    #os.system('sudo ifconfig can0 up')

    #can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

    counter = 0
    xdata = list(range(160))
    list_to_plot = list(range(160))
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-1,1)
    line1, =ax.plot(xdata,list_to_plot)
    while(True):
        counter +=1
        if counter == 40:
            counter = 0
        time.sleep(1)
        
        for i in range(int(buff[counter].dlc/2)):
            num = reverse_twos_complement(buff[counter].data[(i*2)+0])
            dec = reverse_twos_complement(buff[counter].data[(i*2)+1])
            element = odpakowacz(num, dec)
            lista = list()
            lista.append(element)
            list_to_plot = list_to_plot[1:] + lista
        #can0.send(buff[counter])
        print(buff)
        line1.set_ydata(list_to_plot)
        fig.canvas.draw()
        fig.canvas.flush_events()
    #os.system('sudo ifconfig can0 down')

def main():
    
    tablica = np.linspace(-np.pi, np.pi, 160)
    tablica = np.sin(tablica)*1
    
    list_to_send = list()
    list_to_send_check= list()
    
    for i in tablica:
        i = round(i,2)
        list_to_send_check.append(i)
        whole, dec = str(i).split(".")
        whole = twos_complement(int(whole))
        dec = twos_complement(int(dec))
        table_tuple = (whole, dec)

        list_to_send.append(table_tuple)

    
    podzielone_listy = podziel_liste(list_to_send, 4)

    
    buff = list()
    for messages in podzielone_listy:
        pack = list()
        for data in messages:
            pack.append(int(data[0]))
            pack.append((data[1]))
        msg = can.Message(arbitration_id=0x123, data=bytearray(pack), is_extended_id=False)
        buff.append(msg)

    start_procedure(buff)

main()
    
