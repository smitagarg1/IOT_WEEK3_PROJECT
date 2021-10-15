
import json
import time
import paho.mqtt.client as mqtt
import datetime
#HOST = "localhost"
#PORT = 1883
WAIT_TIME = 0.25





class Edge_Server:
    
    def __init__(self, instance_name,host,port):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        print("Connected with result code " + str(result_code))
        client.subscribe("device/REGISTER")
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
       # print(msg.topic, str(msg.payload), "retain", msg.retain, "qos", msg.qos, str(userdata))
        item={"topic":msg.topic, "payload":msg.payload}
      #  print("Received a messsage on " + item["topic"] + " and registering the device "+ item["payload"])
        print("Received by Edge Server a messsage on topic " + item["topic"]+" to register following device")

        if item["topic"]== "device/REGISTER":
            self.set_registered_device_list(item)

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list


    #Smita added
    def set_registered_device_list(self,item):
        s=str(item["payload"].decode("utf-8"))
        dict = json.loads(s)
        #print(dict)
        dict2={}
        device_id=dict["device_id"]
        dict2["device_id"]=device_id
        dict2["device"]=dict
        self._registered_list.append(dict2)
        print(str(dict2))
        print()


    # Getting the status for the connected devices
    def get_status(self,key,value):
        # Smita Call to Edge server to register device
        if key == "device_id":
            item=self.get_device_for_device_id(value)
            room_type=item["room_type"]
            device_type=item["device_type"]

        topic = "device/" + room_type + "/" + device_type + "/status"

        device = {}
        device['publish_topic'] = topic


        message = {}
        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message["key"] = key
        message["value"] = value
        # Publish the message
        self.client.publish(device["publish_topic"], json.dumps(message))
        print("Published to " + topic+" to get status")

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self):
        pass

    def _on_disconnect(client, userdata, result_code):
        print("Disconnected with result code " + str(result_code))


    #Smita added
    def get_device_for_device_id(self,device_id):
        device={}
        device_list=self.get_registered_device_list()
        for item in device_list:
            if item["device_id"] == device_id:
                device= item["device"]



        return device