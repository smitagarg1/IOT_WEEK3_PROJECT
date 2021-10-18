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


time.sleep(15)
print()
print("\n...........Wait for 15 secs...................................................................................................")

print("\n######################Question 2b SWITCHING ON/OFF of device_id,device_type,room_type or ALL.############################################")

print("\n######SWITCH 'ON' COMMAND on basis of device_id LIGHT_0##################################################################")
edge_server_1.switch_command("device_id","LIGHT_0","ON")
print("\n...........Wait for 10 secs...................................................................................................")
time.sleep(10)


print("\n######SWITCH 'ON' COMMAND on basis of device_type AC##################################################################")
print("Switch ON all AC devices")
edge_server_1.switch_command("device_type","AC","ON")
print("\nSleep for 10 sec..............................................................................................................")
time.sleep(15)

print("\n######SWITCH 'ON' COMMAND on basis of room_type BR1##################################################################")
print("Switch ON all devices in room BR1")
edge_server_1.switch_command("room_type","BR1","ON")
print("\nSleep for 10 sec..............................................................................................................")
time.sleep(10)


#print("\n######SWITCH 'ON' COMMAND on basis of ALL##################################################################")
#print("Switch ON all devices in room BR1")
#edge_server_1.switch_command("ALL","ALL","ON")
#print("\nSleep for 10 sec..............................................................................................................")
#time.sleep(10)


print("\n\n#############Device status of ALL devices after SWITCH COMMAND#################################################################")
print("LIGHT_0(device_id call), AC_0,AC_1(device_type call),LIGHT_1,AC_0(room_type call) should be ON ")
print("Only LIGHT_2 should be OFF ")
edge_server_1.clear_device_status_list()
edge_server_1.get_status("ALL","ALL")
print("\nSleep for 10 sec..............................................................................................................")
time.sleep(10)
device_status=edge_server_1.get_device_status_list()
print("\nPrinting consolidated status of all devices in home . ")
print(device_status)


time.sleep(10)
print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()