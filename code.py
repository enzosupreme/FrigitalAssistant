import time
import os
import traceback
from adafruit_magtag.magtag import MagTag
from secrets import secrets
import ssl
import gc
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
import adafruit_datetime
import adafruit_display_text
from adafruit_display_text import label
import board
from adafruit_bitmap_font import bitmap_font
import displayio
from adafruit_display_shapes.rect import Rect
from digitalio import DigitalInOut, Direction, Pull

magtag = MagTag(rotation=180)
feeder = "hello"
magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 10) - 2,
        (magtag.graphics.display.height // 10) - 20,
    ),
    text_scale=1,
    text_wrap=19,
    text_maxlen=1028,
    line_spacing=1.25,
    text_anchor_point=(0,0),
    )
magtag.set_text(feeder)
a = magtag.peripherals.button_a_pressed
b = magtag.peripherals.button_b_pressed
c = magtag.peripherals.button_c_pressed
d = magtag.peripherals.button_d_pressed

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
recipe = secrets["aio_username"] + "/feeds/recipe"


def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to Adafruit IO! Listening for topic changes on %s" % recipe)
    # Subscribe to all changes on the feed.

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from Adafruit IO!")


def on_message(client, feed_id, payload):
    x = (payload)
    print(x)

    magtag.set_text(x)


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=secrets["port"],
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_subscribe = subscribe
mqtt_client.on_message = on_message


# Connect the client to the MQTT broker.
print("Connecting to Adafruit IO...")
mqtt_client.connect()
rec_val = 0
mqtt_client.subscribe(recipe)
pub = "Frigital Assistant                    \nA)Breakfast\n  B)Lunch \n      C)Dinner\n    D)Wisdom"
mqtt_client.publish(recipe, pub)

while True:
    if magtag.peripherals.button_a_pressed:
        mqtt_client.publish(recipe, "Breakfast")
    if magtag.peripherals.button_b_pressed:
        mqtt_client.publish(recipe, "Lunch")
    if magtag.peripherals.button_c_pressed:
        mqtt_client.publish(recipe, "Dinner")
    if magtag.peripherals.button_d_pressed:
        mqtt_client.publish(recipe, "Wisdom")
    mqtt_client.loop()
    time.sleep(0.1)
