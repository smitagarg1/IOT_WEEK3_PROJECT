import time
import json
from paho import mqtt

from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 7

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user


# Reading the configuration file
f = open("config.json")
config = json.loads(f.read())
f.close()

# GET HOST AND PORT
host = config["broker_host"]
port = config["broker_port"]

edge_server_1 = Edge_Server('edge_server_1', host, port)
time.sleep(WAIT_TIME)

# Creating the light_device ac_device
print("Initiate the device creation and registration process.")

print("----------------------------Question 1 Creating the Light and AC devices for their respective rooms.--------------------------------------------------")
rooms_light = ["KITCHEN", "BR1", "BR2", "Living"]
rooms_ac = ["BR1", "BR2", "Living"]

print("\n")
device_config = []
for devices in config['devices']:
    if devices['type'] == 'LIGHT':
        for n in range(devices['device_count']):
            device_id = devices['type'] + "_" + str(n)
            device_type = devices['type']
            #publish_topic = devices['publish_topic']

            light_device_1 = Light_Device(device_id,device_type, rooms_light.pop(0), host, port)
    elif devices['type'] == 'AC':
        for n in range(devices['device_count']):
            device_id = devices['type'] + "_" + str(n)
            device_type = devices['type']
            #publish_topic = devices['publish_topic']

            ac_device_1 = AC_Device(device_id,device_type, rooms_ac.pop(0), host, port)

time.sleep(10)





print("\n\n\nALL devices registered at edge server are following ")
print(edge_server_1.get_registered_device_list())

print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()