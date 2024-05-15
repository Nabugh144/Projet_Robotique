from machine import Pin, PWM
from time import sleep, sleep_ms

class Moteur : # Moteur
    def __init__ ( self, direct, vit, ctrl ):
        self.dir = Pin(direct, Pin.OUT)
        self.dir.off()
        
        self.vit = PWM ( Pin(vit) )
        self.vit.duty(0)
        
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
            self.dir.off()
        else :
            self.dir.on()


if __name__ == "__main__":
    
    motd = Moteur (27,26,25)
    motg = Moteur (34,35,16)
    motd.reculer()
    motd.modif_vit(700)
    motg.modif_vit(1023-700)
    sleep(1)
    print(motd.cptr)
    print(motg.cptr)