from machine import Pin
import utime
from neopixel import NeoPixel
from WSclient import WSclient
from WebSocketClient import WebSocketClient

NUM_LEDS = 150
NEOPIXEL_PIN = Pin(13)
led_strip = NeoPixel(NEOPIXEL_PIN, NUM_LEDS)


# Initialize WebSocket client
ws_client = WSclient("Cudy-EFFC", "33954721", "ws://192.168.10.31:8080/step5")
# ws_client = WSclient("Potatoes 2.4Ghz", "Hakunamatata7342!", "ws://192.168.2.241:8080/step5")



# Attempt to connect WiFi and WebSocket
def setup_connection():
    try:
        if ws_client.connect_wifi():
            ws = WebSocketClient(ws_client.WEBSOCKET_URL)
            if ws.connect():
                print("WebSocket connection established")
                ws.send("connect")
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
            
        if msg == "Assemblage":
            print("ready")
            
        elif msg == "ping":
            ws.send("Assemblage - pong")
            
                
        utime.sleep_ms(50)  # Short delay to prevent excessive polling

except KeyboardInterrupt:
    print("Bye")
finally:
    # Ensure WebSocket is closed
    if ws:
        ws.close()
