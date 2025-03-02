import socketpool
import wifi
import time
from adafruit_httpserver import Server, Response
import board
import analogio

PIN_CZUJNIK_WODA = analogio.AnalogIn(board.TX)
SSID = "SSID"
PASSWORD = "PASSWORD"
poziom_wody = 0

def getVoltage(pin):
    return (pin.value * 5) / 65536

try:
    wifi.radio.connect(SSID, PASSWORD)
    print(f"Połączono z Wi-Fi: {SSID}")
except Exception as e:
    print(f"Błąd podczas łączenia z Wi-Fi: {e}")
    raise

print(f"Adress to:  http://{wifi.radio.ipv4_address}:8080/api")


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)

@server.route("/api")
def base(request):
    global poziom_wody
    return Response(request, body=f"Poziom wody: {poziom_wody}")

while True:
    try:
        server.start(host=str(wifi.radio.ipv4_address), port=8080)
        while True: 
            server.poll() 
            time.sleep(1)
            poziom_wody = getVoltage(PIN_CZUJNIK_WODA)
    except Exception as e:
        print(f"Błąd serwera: {e}")
        server.stop()
        time.sleep(1)
        continue 
