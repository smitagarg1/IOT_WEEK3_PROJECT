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
rooms_ac = ["BR1", "BR2", "Living"]

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


time.sleep(20)



edge_server_1.clear_device_status_list()
edge_server_1.get_status("device_type","LIGHT")
print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)
device_status=edge_server_1.get_device_status_list()
print("\nPrinting consolidated status of all LIGHT devices")
print(device_status)
#print("\nSmart Home Simulation stopped.")
#edge_server_1.terminate()





print("\nSleep for 30 sec..............................................................................................................")
time.sleep(30)
#edge_server_1.switch_command("device_id","LIGHT_0","ON")
print("Switch ON all LIGHT devices")
edge_server_1.switch_command("device_type","LIGHT","ON")
print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)
edge_server_1.clear_device_status_list()
edge_server_1.get_status("ALL","ALL")
print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)
device_status=edge_server_1.get_device_status_list()
print("\nPrinting consolidated status of all devices in home . ")
print(device_status)

print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)
print("SET LIGHT INTENSITY all LIGHT devices")
_INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]
dict={}
dict['commandkey']="LIGHT_INTENSITY"
dict['commandvalue']="MEDIUM"
edge_server_1.set("device_id","LIGHT_0",dict)
print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)

edge_server_1.clear_device_status_list()
edge_server_1.get_status("device_type","LIGHT")
time.sleep(20)
device_status=edge_server_1.get_device_status_list()
print("\nPrinting consolidated status of all devices in home . ")
print(device_status)



time.sleep(20)

print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)
print("CHANGE AC TEMPERATURE")
dict={}
dict['commandkey']="TEMPERATURE"
dict['commandvalue']="34"
edge_server_1.set("device_id","AC_0",dict)
print("\nSleep for 20 sec..............................................................................................................")
time.sleep(20)

edge_server_1.clear_device_status_list()
edge_server_1.get_status("device_type","AC")
time.sleep(20)
device_status=edge_server_1.get_device_status_list()
print("\nPrinting consolidated status of all devices in home .It ends here ")
print(device_status)



print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()