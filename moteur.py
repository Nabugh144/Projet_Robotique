from machine import Pin, PWM
from time import sleep, sleep_ms

class Moteur : # Moteur
    def __init__ ( self, direct, vit, ctrl ):
        self.dir = Pin(direct, Pin.OUT)
        self.dir.off()
        
        self.vit = PWM ( Pin(vit) )
        self.vit.duty(400)
        self.vit.freq(200)
        
        self.ctrl = Pin(ctrl, Pin.IN)
        self.ctrl.irq(trigger = Pin.IRQ_RISING, handler=self.irq_increment_cptr)
        self.cptr = 0
    
    def irq_increment_cptr(self, pin):
        self.cptr += 1
    
    @property
    def vitesse (self):
        return self.vit.duty()
    
    def modif_vit (self,speed):   ######
        if self.dir.value():
            self.vit.duty(speed)
        else :
            self.vit.duty(1023 - speed)
            
    def stop (self) :
        self.vit.duty(0)
        
    def reculer ( self ):
        if self.dir.value() :
            self.dir.off() # avance
        else :
            self.dir.on() # recule


if __name__ == "__main__":
    
    bp = Pin(13,Pin.IN)
    
    running = False
    while running == False:
        appui = bp.value()
        if appui == 1:
            running = True
    
    motd = Moteur (27,26,35)
    motg = Moteur (16,25,34)
    motg.reculer()
    sleep(1)
    print(motd.cptr)
    print(motg.cptr)