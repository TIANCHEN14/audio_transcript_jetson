import paho.mqtt.client as mqtt

# define broker ip address
broker_address = "10.14.105.52"
port = 1883

# define topic
topic = "NASCAR_Radio"
message = "We are good"

# MQTT clients creation
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker_address , port = port)
client.publish(topic , message)

# Disconnet from the broker
client.disconnect()


