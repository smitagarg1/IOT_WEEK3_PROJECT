
import json
import paho.mqtt.client as mqtt
import datetime
from paho.mqtt import client
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
        # Smita implements Call to Edge server to register device
        topic = "device/REGISTER"

        # Initialize a dictionary to be sent as publish message
        message = {}

        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message["device_id"] = device_id
        message["device_type"] = device_type
        message["room_type"] = room_type

        # Publish the message
        print("\n")
        print("\n######################Published by " + self._device_id + " to topic device/REGISTER to register on edge server##########################")
        print("\n")
        self.client.publish(topic, json.dumps(message))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        # Smita adding topics subscribed by AC DEVICE
        print("\nConnected with result code " + str(result_code))

        topic_register_ack = "device/" + self._device_id + "/REGISTER_ACK"

        # Topics to get status on basis of device_id , device_type or room_type or ALL
        topic_deviceid = "device/" + self._device_id + "/STATUS"
        topic_room_type = "device/" + self._room_type + "/STATUS"
        topic_device_type = "device/" + self._device_type + "/STATUS"
        topic_all_status = "device/ALL/STATUS"

        # Topics to SWITCH ON/OFF on  basis of device_id , device_type or room_type or ALL
        topic_deviceid_switch = "device/" + self._device_id + "/SWITCH"
        topic_room_type_switch = "device/" + self._room_type + "/SWITCH"
        topic_device_type_switch = "device/" + self._device_type + "/SWITCH"
        topic_all_switch = "device/ALL/SWITCH"

        # Topics to change TEMPERATURE   on  basis of device_id , device_type or room_type or ALL

        topic_deviceid_temp = "device/" + self._device_id + "/TEMPERATURE"
        topic_room_type_temp = "device/" + self._room_type + "/TEMPERATURE"
        topic_device_type_temp = "device/" + self._device_type + "/TEMPERATURE"
        topic_all_temp = "device/ALL/TEMPERATURE"

        print("\nAC Device " + self._device_id + " subscribing to following topics:::::::::::::")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_register_ack + " :::: Topic for registration acknowledgement from edge server")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_deviceid + "  :::: Topic for getting status on basis of device_id")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_room_type + "  :::: Topic for getting status on basis of room_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_device_type + "  :::: Topic for getting status on basis of device_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_all_status + "  :::: Topic for getting status  for all devices in home")

        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_deviceid_switch + "  :::: Topic for switching on and off on basis of device_id")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_room_type_switch + "  :::: Topic for switching on and off on basis of room_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_device_type_switch + "  :::: Topic for switching on and off on basis of device_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_all_switch + "  :::: Topic for switching on and off for all devices in home")

        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_deviceid_temp + "  :::: Topic for changing temperature on basis of device_id")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_room_type_temp + "  :::: Topic for changing temperature on basis of room_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_device_type_temp + "  :::: Topic for changing temperature on basis of device_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_all_temp + "  :::: Topic for for changing temperature for all devices in home")

        client.subscribe([(topic_deviceid, 1), (topic_register_ack, 0), (topic_room_type, 0), (topic_device_type, 0),
                          (topic_deviceid_switch, 0), (topic_room_type_switch, 0),
                          (topic_device_type_switch, 0), (topic_all_status, 0), (topic_all_switch, 0),
                          (topic_deviceid_temp, 0), (topic_room_type_temp, 0),
                          (topic_device_type_temp, 0), (topic_all_temp, 0)])

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        # Smita added for further execution based on message topic received on publish

        item = {"topic": msg.topic, "payload": msg.payload}
        if item["topic"] == "device/" + self._device_id + "/REGISTER_ACK":
            s = str(item["payload"].decode("utf-8"))
            dict = json.loads(s)
            print("\n" + self._device_id + " Received a message on topic " + item["topic"] + " saying " + dict[
                'ack_message'])

        if item["topic"] == "device/" + self._device_id + "/STATUS":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)
        elif item["topic"] == "device/" + self._room_type + "/STATUS":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)

        elif item["topic"] == "device/" + self._device_type + "/STATUS":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)
        elif item["topic"] == "device/ALL/STATUS":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)

        if item["topic"] == "device/" + self._device_id + "/SWITCH":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_switch_status(item)

        elif item["topic"] == "device/" + self._room_type + "/SWITCH":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_switch_status(item)

        elif item["topic"] == "device/" + self._device_type + "/SWITCH":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_switch_status(item)
        elif item["topic"] == "device/ALL/SWITCH":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_switch_status(item)

        if item["topic"] == "device/" + self._device_id + "/TEMPERATURE":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_temperature(item)

        elif item["topic"] == "device/" + self._room_type + "/TEMPERATURE":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_temperature(item)

        elif item["topic"] == "device/" + self._device_type + "/TEMPERATURE":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_temperature(item)
        elif item["topic"] == "device/ALL/TEMPERATURE":
            print("\n" + self._device_id + " Received a message on topic " + item["topic"])
            self._set_temperature(item)

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        return self._get_switch_status()


    # Setting the the switch of devices
    def _set_switch_status(self, item):
        print("\nInside switch status for " + self._device_id)
        s = str(item["payload"].decode("utf-8"))
        dict = json.loads(s)
        print("\nCommand is " + dict['command'])

        try:
            self._switch_status = dict['command']

            # Smita Call to Edge server to acknowledge SWITCH COMMAND ON/OFF
            topic = "device/ACKSWITCH"
            # Initialize a dictionary to be sent as publish message
            message = {}

            # Generate timestamp in YYYY-MM-DD HH:MM:SS format
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['switch_status'] = self._switch_status
            message['device_type'] = self._device_type
            message['device_id'] = self._device_id
            message['temperature'] = self._temperature
            message['command'] = dict['command']
            message['ack_message'] = "Successful"

            # Publish the message
            print("\nPublished by " + self._device_id + " to topic device/ACKSWITCH to send device SWITCH operation success acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))

        except Exception:
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['ack_message'] = "Not Successful"
            message['device_id'] = self._device_id
            message['command'] = dict['command']

            # Publish the message
            print("\nPublished by " + self._device_id + " to topic device/ACKSWITCH to send device SWITCH operation failure acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._get_temperature()

    # Setting up the temperature of the devices
    def _set_temperature(self, item):

        print("\nInside set temperature for " + self._device_id)
        s = str(item["payload"].decode("utf-8"))
        dict = json.loads(s)
        print("Temperature commanded to set is " + dict['TEMPERATURE'])

        try:
            self._temperature=dict['TEMPERATURE']
            # Smita Call to Edge server to acknowledge TEMPERATURE COMMAND
            topic = "device/ACKTEMPERATURE"

            # Initialize a dictionary to be sent as publish message
            message = {}

            # Generate timestamp in YYYY-MM-DD HH:MM:SS format
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['TEMPERATURE']=self._temperature
            message['device_id'] = self._device_id
            message['ack_message'] = "Successful"

            # Publish the message
            print("\nPublished by " + self._device_id + " to topic device/ACKTEMPERATURE to send device TEMPERATURE operation success acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))

        except Exception:
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['ack_message'] = "Not Successful"
            message['device_id'] = self._device_id
            message['TEMPERATURE'] = dict['TEMPERATURE']

            # Publish the message
            print("\nPublished by " + self._device_id + " to topic device/ACKTEMPERATURE to send device TEMPERATURE operation failure acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))


    # Smita added
    def _on_disconnect(client, userdata, result_code):
        print("Disconnected with result code " + str(result_code))

    # Smita added
    def get_consolidated_status(self, item):
        print("Inside consolidated_status for " + self._device_id)
        # Smita Call to Edge server to register device
        topic = "device/ACKSTATUS"
        # Initialize a dictionary to be sent as publish message
        message = {}

        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['switch_status'] = self._switch_status
        message['device_type'] = self._device_type
        message['device_id'] = self._device_id
        message['room_type'] = self._room_type
        message['temperature'] = self._temperature

        # Publish the message
        print("\nPublished by " + self._device_id + " to topic device/ACKSTATUS to send device status to edge server")
        self.client.publish(topic, json.dumps(message))