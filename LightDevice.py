import json
import paho.mqtt.client as mqtt
import datetime

#HOST = "localhost"
#PORT = 1883
from paho.mqtt import client



class Light_Device():

    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id,_device_type, room,host,port):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = _device_type
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(host,port, keepalive=60)
        self.client.loop_start()
        self._register_device(self._device_id, self._room_type,self._device_type)
        self._switch_status = "OFF"


    def _register_device(self, device_id, room_type ,device_type):
        #Smita implements Call to Edge server to register device
        topic= "device/REGISTER"

        # Initialize a dictionary to be sent as publish message
        message = {}

        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message["device_id"] = device_id
        message["device_type"] = device_type
        message["room_type"] = room_type

        # Publish the message
     
        print("\nPublished by " + self._device_id + " to topic device/REGISTER to register on edge server")
        self.client.publish(topic, json.dumps(message))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        #Smita adding topics subscribed by LIGHT DEVICE
        print("\nConnected with result code " + str(result_code))

        topic_register_ack="device/"+self._device_id+"/REGISTER_ACK"

        #Topics to get status on basis of device_id , device_type or room_type or ALL
        topic_deviceid="device/"+self._device_id+"/STATUS"
        topic_room_type = "device/" + self._room_type + "/STATUS"
        topic_device_type = "device/" + self._device_type + "/STATUS"
        topic_all_status = "device/ALL/STATUS"

        # Topics to SWITCH ON/OFF on  basis of device_id , device_type or room_type or ALL
        topic_deviceid_switch = "device/" + self._device_id + "/SWITCH"
        topic_room_type_switch = "device/" + self._room_type + "/SWITCH"
        topic_device_type_switch = "device/" + self._device_type + "/SWITCH"
        topic_all_switch="device/ALL/SWITCH"

        # Topics to change LIGHTINTENSITY  ["LOW", "HIGH", "MEDIUM", "OFF"] on  basis of device_id , device_type or room_type or ALL

        topic_deviceid_intensity = "device/" + self._device_id + "/LIGHTINTENSITY"
        topic_room_type_intensity = "device/" + self._room_type + "/LIGHTINTENSITY"
        topic_device_type_intensity = "device/" + self._device_type + "/LIGHTINTENSITY"
        topic_all_intensity = "device/ALL/LIGHTINTENSITY"


        print("\nLight Device "+self._device_id+" subscribing to following topics" )
        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+topic_register_ack+" :::: Topic for registration acknowledgement from edge server")
        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+topic_deviceid+"  :::: Topic for getting status on basis of device_id")
        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+topic_room_type+"  :::: Topic for getting status on basis of room_type")
        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+topic_device_type+"  :::: Topic for getting status on basis of device_type")
        print("Device id =>" +self._device_id + ":::::Topic Subscribed=>" + topic_all_status + "  :::: Topic for getting status  for all devices in home")

        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+ topic_deviceid_switch + "  :::: Topic for switching on and off on basis of device_id")
        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+ topic_room_type_switch + "  :::: Topic for switching on and off on basis of room_type")
        print("Device id =>"+self._device_id+":::::Topic Subscribed=>"+ topic_device_type_switch + "  :::: Topic for switching on and off on basis of device_type")
        print("Device id =>" +self._device_id + ":::::Topic Subscribed=>" + topic_all_switch + "  :::: Topic for switching on and off for all devices in home")

        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_deviceid_intensity + "  :::: Topic for changing light intensity on basis of device_id")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_room_type_intensity + "  :::: Topic for changing light intensity on basis of room_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_device_type_intensity + "  :::: Topic for changing light intensity on basis of device_type")
        print("Device id =>" + self._device_id + ":::::Topic Subscribed=>" + topic_all_intensity + "  :::: Topic for for changing light intensity for all devices in home")

        client.subscribe([(topic_deviceid, 1),(topic_register_ack, 0), (topic_room_type, 0), (topic_device_type, 0),(topic_deviceid_switch,0),(topic_room_type_switch,0),
                          (topic_device_type_switch,0),(topic_all_status,0),(topic_all_switch,0),(topic_deviceid_intensity,0),(topic_room_type_intensity,0),
                          (topic_device_type_intensity,0),(topic_all_intensity,0)])

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        #Smita added for further execution based on message topic received on publish

        item = {"topic": msg.topic, "payload": msg.payload}
        if item["topic"]=="device/"+self._device_id+"/REGISTER_ACK":
            s = str(item["payload"].decode("utf-8"))
            dict = json.loads(s)
            print("\n"+self._device_id+" Received a message on topic " + item["topic"]+" saying "+dict['ack_message'])

        if item["topic"] =="device/"+self._device_id+"/STATUS":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)
        elif item["topic"] =="device/"+self._room_type+"/STATUS":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)

        elif item["topic"] =="device/"+self._device_type+"/STATUS":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)
        elif item["topic"] =="device/ALL/STATUS":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self.get_consolidated_status(item)

        if item["topic"] =="device/"+self._device_id+"/SWITCH":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_switch_status(item)

        elif item["topic"] =="device/"+self._room_type+"/SWITCH":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_switch_status(item)

        elif item["topic"] =="device/"+self._device_type+"/SWITCH":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_switch_status(item)
        elif item["topic"] =="device/ALL/SWITCH":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_switch_status(item)


        if item["topic"] =="device/"+self._device_id+"/LIGHTINTENSITY":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_light_intensity(item)

        elif item["topic"] =="device/"+self._room_type+"/LIGHTINTENSITY":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_light_intensity(item)

        elif item["topic"] =="device/"+self._device_type+"/LIGHTINTENSITY":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_light_intensity(item)
        elif item["topic"] =="device/ALL/LIGHTINTENSITY":
            print("\n"+self._device_id+" Received a message on topic " + item["topic"])
            self._set_light_intensity(item)



    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._get_switch_status()

    # Setting the the switch of devices
    def _set_switch_status(self, item):
        print("\nInside switch status for "+self._device_id)
        s = str(item["payload"].decode("utf-8"))
        dict = json.loads(s)
        print("Command is "+dict['command'] )

        try:
            self._switch_status=dict['command']

            # Smita Call to Edge server to acknowledge SWITCH COMMAND ON/OFF
            topic = "device/ACKSWITCH"
            # Initialize a dictionary to be sent as publish message
            message = {}

            # Generate timestamp in YYYY-MM-DD HH:MM:SS format
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['switch_status'] = self._switch_status
            message['device_type'] = self._device_type
            message['device_id'] = self._device_id
            message['light_intensity'] = self._light_intensity
            message['command'] =dict['command']
            message['ack_message'] = "Successfull"

            # Publish the message
            print("\nPublished by " + self._device_id + " to topic device/ACKSWITCH to send device SWITCH operation success acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))

        except Exception:
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['ack_message'] = "Not Successfull"
            message['device_id'] = self._device_id
            message['command'] = dict['command']

            # Publish the message
            print(
                "\nPublished by " + self._device_id + " to topic device/ACKSWITCH to send device SWITCH operation failure acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))




    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._get_light_intensity()

    # Setting the light intensity for devices
    def _set_light_intensity(self, item):
        print("\nInside set light intensity for " + self._device_id)
        s = str(item["payload"].decode("utf-8"))
        dict = json.loads(s)
        print("Light Intensity commanded is " + dict['LIGHT_INTENSITY'])

        try:
            self._light_intensity=dict['LIGHT_INTENSITY']
            # Smita Call to Edge server to acknowledge INTENSITY COMMAND ["LOW", "HIGH", "MEDIUM", "OFF"]
            topic = "device/ACKLIGHTINTENSITY"

            # Initialize a dictionary to be sent as publish message
            message = {}

            # Generate timestamp in YYYY-MM-DD HH:MM:SS format
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['LIGHT_INTENSITY']=self._light_intensity
            message['device_id'] = self._device_id
            message['ack_message'] = "Successful"

            # Publish the message
            print("\nPublished by " + self._device_id + " to topic device/ACKLIGHTINTENSITY to send device LIGHT_INTENSITY operation success acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))

        except Exception:
            message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message['ack_message'] = "Not Successful"
            message['device_id'] = self._device_id
            message['LIGHT_INTENSITY'] = dict['LIGHT_INTENSITY']

            # Publish the message
            print(
                "\nPublished by " + self._device_id + " to topic device/ACKLIGHTINTENSITY to send device LIGHT_INTENSITY operation failure acknowledgement to edge server")
            self.client.publish(topic, json.dumps(message))


    #Smita added
    def _on_disconnect(client, userdata, result_code):
        print("\nDisconnected with result code " + str(result_code))

    #Smita added
    def get_consolidated_status(self,item):
        print("Inside consolidated_status for "+self._device_id)
        #Smita Call to Edge server to register device
        topic = "device/ACKSTATUS"
        # Initialize a dictionary to be sent as publish message
        message = {}

        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['switch_status'] = self._switch_status
        message['device_type'] = self._device_type
        message['device_id'] = self._device_id
        message['light_intensity'] = self._light_intensity

        # Publish the message
        print("\nPublished by " + self._device_id + " to topic device/ACKSTATUS to send device status to edge server")
        self.client.publish(topic, json.dumps(message))




