import requests
import ShellyPy
import base64
import time
from datetime import datetime

POWERFOX_API_URL = "https://backend.powerfox.energy/api/2.0/my/main/current"
POWERFOX_EMAIL = "YOURMAIL"
POWERFOX_PASSWORD = "YOURPASSWORD"

SHELLY_IP = "YOURIP"

shelly = ShellyPy.Shelly(SHELLY_IP)

def is_shelly_reachable(shelly):
    try:
        # Versuche, den Status des Shelly-Geräts abzurufen
        status = shelly.status()
        if status:
            print(f"Shelly ist erreichbar: {SHELLY_IP}")
            return True
        else:
            print(f"Shelly ist nicht erreichbar: {SHELLY_IP}")
            return False
    except Exception as e:
        print(f"Fehler bei der Verbindung mit Shelly: {e}")
        return False

def is_shelly_on(shelly):
    try:
        # Prüfen, ob der Shelly eingeschaltet ist
        status = shelly.relay(0)
        return status['output']
    except Exception as e:
        print(f"Fehler bei der Überprüfung des Shelly-Status: {e}")
        return False

while True:
    credentials = f"{POWERFOX_EMAIL}:{POWERFOX_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
        
    response = requests.get(POWERFOX_API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Hole den Wert des Feldes "Watt"
        power = data.get("Watt", 0)
        
        # Prüfen, ob der Shelly eingeschaltet ist
        if is_shelly_on(shelly):
            print("Shelly ist eingeschaltet, -3000 Watt zum Verbrauch hinzufügen.")
            power += -3000  # -3000 Watt hinzufügen

        print(f"Aktuelle Leistung nach Anpassung: {power} Watt")
        
        # Prüfe ob der Wert negativ ist und die Einspeisung mindestens 3000 Watt beträgt
        if power <= -3000:
            print("Einspeisung ist größer als 3000 Watt")
            # Shelly einschalten, wenn erreichbar
            if is_shelly_reachable(shelly):
                shelly.relay(0, turn=True)
                print("Shelly wird eingeschaltet.")
        else:
            print("Einspeisung ist kleiner als 3000 Watt oder es wird Strom bezogen")
            # Shelly ausschalten, wenn erreichbar
            if is_shelly_reachable(shelly):
                shelly.relay(0, turn=False)
                print("Shelly wird ausgeschaltet.")
    else:
        print(f"Fehler beim Abrufen der Powerfox-Daten: {response.status_code}")
    
    # 10 Minuten warten
    time.sleep(600)
