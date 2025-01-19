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

def running_light(duration=10):
    start_time = utime.time()
    while utime.time() - start_time < duration:
        for i in range(NUM_LEDS):
            clear_strip()
            led_strip[i] = (255, 255, 255)  # Rouge
            led_strip.write()
            utime.sleep_ms(50)
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

# Establish WebSocket connection
ws = setup_connection()

try:
    while True:
        msg = ws.receive()
        print("Message reçu :", msg)
            
        if msg == "assembly_start":
            print("Animation started")
            running_light()  # Lance l'animation pendant 10 secondes
            ws.send("assembly_play")
            
        elif msg == "ping":
            ws.send("Assemblage - pong")
            
        utime.sleep_ms(50)

except KeyboardInterrupt:
    print("Bye")
finally:
    if ws:
        ws.close()
    clear_strip()