from network import WLAN
import urequests as requests
import machine
import time
from dht import DHT
from machine import Pin

TOKEN = "BBFF-askQt4AaljJTSepC03sFIQXptfCZbE" #Put here your TOKEN
DELAY = 60  # Delay in seconds

th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0) # DHT sensor is connected to port 23
time.sleep(2)  # wait 2 seconds

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)

# Assign your Wi-Fi credentials
wlan.connect("Vannala 2.4GHz", auth=(WLAN.WPA2, "m202h202i"), timeout=5000)

while not wlan.isconnected ():
    machine.idle()
print("Connected to Wifi\n")

# Builds the json to send the request
def build_json(variable1, value1, variable2, value2):
    try:
        lat = 6.217
        lng = -75.567
        data = {variable1: {"value": value1},
                variable2: {"value": value2}}
        return data
    except:
        return None

# Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
def post_var(device, value1, value2):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json("Temp", value1, "RM", value2)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass



while True:
    result = th.read()
    if result.is_valid():
        temp = result.temperature # Data values
        rm = result.humidity # Data values
        post_var("pycomTemp", temp, rm)
        time.sleep(DELAY)
    else:
        time.sleep(1)
