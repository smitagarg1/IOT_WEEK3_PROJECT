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

# Creating the light_device
print("Intitate the device creation and registration process.")


print("\nCreating the Light devices for their respective rooms.")
rooms_light = ["KITCHEN", "BR1", "BR2", "Living"]
device_config = []
for devices in config['devices']:
    if devices['type'] == 'LIGHT':
        for n in range(devices['device_count']):
            device_id = devices['type'] + "_" + str(n)
            device_type = devices['type']
            publish_frequency = devices['publish_frequency']
            std_val = devices['std_val']
            #publish_topic = devices['publish_topic']

            light_device_1 = Light_Device(device_id,device_type, rooms_light.pop(0), host, port)


time.sleep(7)




edge_server_1.get_status("device_id","LIGHT_0")
time.sleep(10)
device_status=edge_server_1.get_device_status_list()
print(device_status)
#print("\nSmart Home Simulation stopped.")
#edge_server_1.terminate()




time.sleep(10)