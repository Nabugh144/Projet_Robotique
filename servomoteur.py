from machine import Pin, PWM

class Servomoteur():
    
    def __init__(self, pin):
        if isinstance(pin,int):
            self.pin = pin
            self.freq = 50
            self.duty = 30
            self.var = PWM(self.pin, self.freq, self.duty)
            self.ouvert = True
    
    def fermer(self):
        if self.ouvert:
            self.var.duty = 130
            self.ouvert = False
            
    def ouvrir(self):
        if self.ouvert == False:
            self.var.duty = 130
            self.ouvert = True