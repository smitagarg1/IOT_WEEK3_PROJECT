
import json
import paho.mqtt.client as mqtt
import datetime

#HOST = "localhost"
#PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id,_device_type, room,host,port):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = _device_type
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(host,port, keepalive=60)
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        # Smita Call to Edge server to register device
        device = {}
        device['device_id'] = device_id
        device['device_type'] = device_type
        device['room_type'] = room_type
        device['publish_topic'] = "device/REGISTER"


        # Initialize a dictionary to be sent as publish message
        message = {}

        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message["device_id"] = device_id
        message["device_type"] = device_type
        message["room_type"] = room_type

        # Publish the message
        print("Published by LIGHT DEVICE " + self._device_id + " to topic device/REGISTER to register " + device_id)
        print()
        self.client.publish(device["publish_topic"], json.dumps(message))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        pass

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg): 
        pass

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        pass

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        pass

    # Getting the temperature for the devices
    def _get_temperature(self):
        pass        

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        pass

    # Smita added
    def _on_disconnect(client, userdata, result_code):
        print("Disconnected with result code " + str(result_code))