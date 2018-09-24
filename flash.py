from machine import Pin
pin_button = Pin(0, Pin.IN)
pin_led = Pin(14, Pin.OUT)

while True:
    stav = pin_button.value()
    pin_led.value(stav)
    
