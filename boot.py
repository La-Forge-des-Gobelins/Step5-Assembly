from machine import Pin
import utime
from neopixel import NeoPixel
from WSclient import WSclient
from WebSocketClient import WebSocketClient

NUM_LEDS = 250
NEOPIXEL_PIN = Pin(19)
led_strip = NeoPixel(NEOPIXEL_PIN, NUM_LEDS)

# Initialize WebSocket client
ws_client = WSclient("Cudy-EFFC", "33954721", "ws://192.168.10.250:8080/step5")

def clear_strip():
    for i in range(NUM_LEDS):
        led_strip[i] = (0, 0, 0)
    led_strip.write()

def running_light(duration):
    # Nombre de LEDs à allumer en même temps
    led_group = 4
    # Calculer le délai entre chaque déplacement pour atteindre la durée totale souhaitée
    steps = NUM_LEDS - led_group + 1  # Nombre total de positions possibles
    delay_ms = (duration * 1000) / steps
    
    for i in range(steps):
        clear_strip()
        # Allumer les 4 LEDs consécutives
        for j in range(led_group):
            if i + j < NUM_LEDS:  # Vérifier qu'on ne dépasse pas la fin de la bande
                led_strip[i + j] = (255, 255, 255)
        led_strip.write()
        utime.sleep_ms(int(delay_ms))
    clear_strip()

def setup_connection():
    try:
        if ws_client.connect_wifi():
            ws = WebSocketClient(ws_client.WEBSOCKET_URL)
            if ws.connect():
                print("WebSocket connection established")
                ws.send("connect")
                running_light(2)
                return ws
        print("Failed to establish connection")
        return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Initialize WebSocket connection
print("Initializing WebSocket connection...")
ws = None
while ws is None:
    ws = setup_connection()
    if ws is None:
        print("Connection failed. Retrying in 5 seconds...")
        utime.sleep(5)

print("WebSocket connected successfully!")

try:
    while True:
        if ws:
            try:
                msg = ws.receive()
                print("Message reçu :", msg)
                
                if msg == "Start":
                    print("Animation started")
                    running_light(5)  # Lance l'animation pendant 10 secondes
                    ws.send("assembly_play")
                    
                elif msg == "ping":
                    ws.send("Assemblage - pong")
                    
            except Exception as e:
                print(f"WebSocket error: {e}")
                ws = None
                
        if ws is None:
            print("Connection lost. Attempting to reconnect...")
            ws = setup_connection()
            if ws is None:
                print("Reconnection failed. Retrying in 5 seconds...")
                utime.sleep(5)
                continue
                
        utime.sleep_ms(50)
        
except KeyboardInterrupt:
    print("Bye")
finally:
    if ws:
        ws.close()
    clear_strip()
