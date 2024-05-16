from calcul_erreur import liste_erreur, erreur_en_cm, flag_i2c
from hcsr04 import HCSR04
from pid import PID
from pcf8574 import PCF8574,binaire_octet
from machine import I2C, Pin
from moteur import Moteur
from time import ticks_ms, ticks_diff

i2c = I2C(1, scl=Pin(21), sda=Pin(22), freq=400000)
pcf = PCF8574(i2c, 0x20)
int_i2c = Pin ( 5, Pin.IN )
int_i2c.irq(trigger = Pin.IRQ_FALLING, handler=flag_i2c)

capt_dist = HCSR04(12,14)

flag = False

bp = Pin(13,Pin.IN)

motg = Moteur(34,35,16)
motd = Moteur(27,26,25)

liste_erreur = []

t0 = tick_ms()

def demi_tour ():
    motg.stop()
    motd.stop()
    motd.reculer()
    motd.cptr = 0
    motg.cptr = 0
    motg.modif_vit(1023)
    motd.modif_vit(1023)
    while motd.cptr <= nb_impulsion_d: # nb_impulsion_d à remplacer par le bon nombre
        if motg.cptr <= nb_impulsion_g :
            motg.stop()
        else :
            pass
    while motg.cptr <= nb_impulsion_g: # nb_impulsion_g à remplacer par le bon nombre
        pass
    motg.stop()
    motd.stop()

running = False
while running == False:
    if bp.value() == 1:
        running = True

sleep(4)

while running == True:

    dt = ticks_diff(tick_ms(), t0)

    # avancer
    motg.modif_vit(400)
    motd.modif_vit(400)

    distance = capt_dist.distance_mm()
    
    if bp.value() == 1 :
        running = False
    elif distance <= 40:
        demi_tour()
    
    if dt >= 200 :
        if flag == True :
            sorties = pcf.port
            liste_erreur = liste_erreur(erreur_en_cm(binaire_octet(sorties)[0]),liste_erreur)
            correction = PID(liste_erreur)
            motg.modif(motg.vitesse-correction)
            motd.modif(motd.vitesse+correction)
            flag = False
        elif flag == False :
            liste_erreur = liste_erreur(liste_erreur[-1],liste_erreur)
        t0 = tick_ms()