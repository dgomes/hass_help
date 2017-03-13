import logging
import datetime
import json
import subsystem
import re

state_topic = "switch/{}"
command_topic = "switch/{}/set"

# tuple -> relay, impulse
lights = {
    'cozinha': (7, 1000),
    'muros_frente': (9, 1000),
    'muros_tras': (6, 1000),
    }

class Switch(subsystem.Subsystem):
    def __init__(self):
        super().__init__()
        self.topic = [(self.root_topic + command_topic.format(switch), 0) for switch in lights.keys()] 

    def on_message(self, client, msg):
        try:
            switch = re.search(command_topic.format('(.+?)'), msg.topic).group(1)
            relay, impulse = lights[switch]
            client.publish(subsystem.relay_topic.format(relay), payload=str(impulse))
            client.publish(self.root_topic + state_topic.format(switch), payload=msg.payload, retain=True)
        except Exception as e:
            logging.error(e)
            client.publish(msg.topic+"/error", payload=str(e), retain=True)

instance = Switch()
