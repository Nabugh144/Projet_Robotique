from pcf8574 import PCF8574, binaire_octet
from machine import I2C, Pin
from time import sleep

flag = False # drapeau pour interruption pcf8574

def flag_i2c ( pin ):
    global flag
    flag = True

i2c = I2C(1, scl=Pin(21), sda=Pin(22), freq=400000)
pcf = PCF8574(i2c, 0x20)
int_i2c = Pin ( 5, Pin.IN )
int_i2c.irq(trigger = Pin.IRQ_FALLING, handler=flag_i2c)

while True:
    if flag == True :
        sorties = pcf.port
        print(binaire_octet( sorties ))
        flag = False
    
