#!/usr/bin/env python

import time
import sys
import ast

#Endpoint for AWS IOT Thing
pi_iot_endpoints = {
	'endpoint':'ail7uw8ny2r8u.iot.ap-southeast-2.amazonaws.com',
	'tls_port':'8883',
	'websocket_port':'443',
}

#Certificates for AWS IOT Thing
iot_certificate_path = 'certs/'
rootCAKey 	= iot_certificate_path + "iot-rootCa.key"
private_key 	= iot_certificate_path + "673ce89fbf-private.pem.key"
certificate 	= iot_certificate_path + "673ce89fbf-certificate.pem.crt"

topic = "myTopicisthis"

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
# For TLS mutual authentication
myMQTTClient.configureEndpoint(pi_iot_endpoints["endpoint"], pi_iot_endpoints["tls_port"])
myMQTTClient.configureCredentials(rootCAKey, private_key, certificate)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


# Custom MQTT message callback
def customCallback(client, userdata, message):
#        print("Received a new message: ")
#        print(message.payload)
#        print("from topic: ")
#        print(message.topic)
#        print("--------------\n\n")

	output_var = message.payload
	output_var_dict = ast.literal_eval(output_var)
	output_var_int = int(output_var_dict["state"])

	#check state first to reset state of pin
	current_state = GPIO.input(21)
	
	GPIO.output(21, output_var_int)         # set GPIO24 to 1/GPIO.HIGH/True
        time.sleep(0.5)                 # wait half a second
        #GPIO.output(21, current_state)


#Initialise Rpi GPIO 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Set channel 21 as an output
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)

# Connect and subscribe to AWS IoT
myMQTTClient.connect()

# Publish to the same topic in a loop forever
loopCount = 0

try:  
    while loopCount < 20:

	# subscribe to AWS IoT
	myMQTTClient.subscribe(topic, 1, customCallback)
	
	print "count is " + str(loopCount)
        loopCount += 1
	time.sleep(1)

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program  

except: 
    print "Unexpected error:", sys.exc_info()[0]
    raise
	
