from pcf8574 import PCF8574, binaire_octet
from machine import I2C, Pin
from time import sleep

flag = False # drapeau pour interruption pcf8574

def flag_i2c ( pin ):
    global flag
    flag = True

def erreur_en_cm(erreur :int)->float:
    dico = {1:7.5, 3:5.5, 2:3.9, 6:2.15, 4:0, 12:-2.15, 8:-3.9, 24:-5.5, 16:-7.5}
    if erreur in dico.keys():
        return dico[erreur]
    elif erreur == 7 or erreur == 5:
        return 100
    elif erreur == 20 or erreur == 28:
        return -100
    
def liste_erreur(erreur : float, liste : list)->list:
    if len(liste) == 10:
        liste.pop(0)
    liste.append(erreur)
    return liste
    


if __name__ == "__main__":

    i2c = I2C(1, scl=Pin(21), sda=Pin(22), freq=400000)
    pcf = PCF8574(i2c, 0x20)
    int_i2c = Pin ( 5, Pin.IN )
    int_i2c.irq(trigger = Pin.IRQ_FALLING, handler=flag_i2c)

    while True:
        if flag == True :
            sorties = pcf.port
            print(binaire_octet(sorties))
            flag = False
            print(erreur_en_cm(binaire_octet(sorties)[0]))