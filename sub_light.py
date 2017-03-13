import logging
import datetime
import json
import subsystem
import re

state_topic = "light/{}"
command_topic = "light/{}/set"

# tuple -> relay, impulse
lights = {
    'cozinha': (7, 1000),
    'muros_frente': (9, 1000),
    'muros_tras': (6, 1000),
    }

class Light(subsystem.Subsystem):
    def __init__(self):
        super().__init__()
        self.topic = [(self.root_topic + command_topic.format(light), 0) for light in lights.keys()] 

    def on_message(self, client, msg):
        try:
            light = re.search(command_topic.format('(.+?)'), msg.topic).group(1)
            relay, impulse = lights[light]
            client.publish(subsystem.relay_topic.format(relay), payload=str(impulse))
            client.publish(self.root_topic + state_topic.format(light), payload=msg.payload, retain=True)
        except Exception as e:
            logging.error(e)
            client.publish(msg.topic+"/error", payload=str(e), retain=True)

instance = Light()
