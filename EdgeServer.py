
import json
import time
import paho.mqtt.client as mqtt
import datetime
#HOST = "localhost"    #smita commenting as host port will be picked up from config file
#PORT = 1883		   #smita commenting as host port will be picked up from config file
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
        self._device_status = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        print("Connected with result code " + str(result_code))
        print()
        client.subscribe([("device/REGISTER",0),("device/ACKSTATUS",0)])

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        item={"topic":msg.topic, "payload":msg.payload}

        if item['topic'] == "device/REGISTER":
            print()
            print("Received by Edge Server a messsage on topic " + item['topic'] + " to register following device")
            self.set_registered_device_list(item)
        elif item['topic'] == "device/ACKSTATUS":
            self.receive_status(item)


    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list


    #Smita added
    def set_registered_device_list(self,item):
        s=str(item['payload'].decode("utf-8"))
        dict = json.loads(s)
        #print(dict)
        dict2={}
        device_id=dict['device_id']
        device_type=dict['device_type']
        dict2['device_id']=device_id
        dict2['device']=dict
        self._registered_list.append(dict2)
        print(str(dict2))
        print()

        device = {}

        device['publish_topic'] = "device/"+device_type+"/REGISTER_ACK"
        device['device_id'] = device_id
        device['device_type'] = device_type
        device['ack_message'] = device_id + " registered successfully"

        message = {}
        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['device_id'] = device_id
        message['device_type'] = device_type
        message['ack_message'] = device_id + " registered successfully"


        # Publish the message
        self.client.publish(device["publish_topic"], json.dumps(message))
        print("Published by Edge Server to topic device/"+device_type+"/REGISTER_ACK to acknowledge successfull device registration")
        print("No of registered device now " + str(len(self._registered_list)))


    # Getting the status for the connected devices
    def get_status(self,key,value):
        # Smita publish to Call to devices to get their status .
        device = {}
        topic="device/" + value+ "/STATUS"
        device["publish_topic"] = topic

        message = {}
        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Publish the message
        self.client.publish(device["publish_topic"], json.dumps(message))
        print("Published to " + topic + " to get status of devices on basis of " + key)

    # Sending Switch on and off for the connected devices
    def switch_command(self, key, value,command):
        # Smita publish
        device = {}
        topic = "device/" + value + "/SWITCH"
        device['publish_topic'] = topic
        device['command'] = command

        message = {}
        # Generate timestamp in YYYY-MM-DD HH:MM:SS format
        message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['command'] = command

        # Publish the message
        self.client.publish(device["publish_topic"], json.dumps(message))
        print("Published to " + topic + " to get status of devices on basis of " + key)


    #Smita added
    def receive_status(self,item):
        s = str(item["payload"].decode("utf-8"))
        dict = json.loads(s)

        self._device_status.append(dict)


    #Smita added
    def get_device_status_list(self):
        return self._device_status



    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self):
        pass

    def _on_disconnect(client, userdata, result_code):
        print("Disconnected with result code " + str(result_code))


