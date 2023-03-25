import time
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


magtag = MagTag()
magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    textw_scale=1,
)

recipe = secrets["aio_username"] + "feeds/recipe"
pool = socketpool.SocketPool(wifi.radio)
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

print(f"Connecting to {secrets['ssid']}")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print(f"Connected to {secrets['ssid']}!")

def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to Adafruit IO! Listenin g for topic changes on %s" % recipe)
    # Subscribe to all changes on the recipe
    client.subscribe(recipe)


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from Adafruit IO!")


def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    print("New message on topic {0}: {1}".format(topic, message))

# Connect to WiFi
    print("Connecting to WiFi...")
    wifi.connect()
    print("Connected!")



# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=1883,
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

io = IO_MQTT(mqtt_client)
# Setup the callback methods above
io.on_connect = connected
io.on_disconnect = disconnected
io.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to Adafruit IO...")
io.connect()

recipe_val = 0

while True:
    # Poll the message queue
    mqtt_client.loop()
    wifi.reset()
    mqtt_client.reset()

    # Send a new message
    print("Sending recipe value: %d..." % recipe_val)
    mqtt_client.publish(recipe, recipe_val)
    print("Sent!")
    recipe_val += 1
    time.sleep(5)
