import logging
import datetime
import json
import subsystem
import re

state_topic = "switch/{}"
command_topic = "switch/{}/set"

# tuple -> relay, impulse
switches = {
    'toalheiros': (105, 1000),
    'rega': (10, 1000),
    }

class Switch(subsystem.Subsystem):
    def __init__(self):
        super().__init__()
        self.topic = [(self.root_topic + command_topic.format(switch), 0) for switch in switches.keys()] 

    def on_message(self, client, msg):
        try:
            switch = re.search(command_topic.format('(.+?)'), msg.topic).group(1)
            if not self.state.get(switch, 'OFF') == msg.payload:
                relay, impulse = switches[switch]
                client.publish(subsystem.relay_topic.format(relay), payload=str(impulse))
                client.publish(self.root_topic + state_topic.format(switch), payload=msg.payload, retain=True)
                self.state[switch] = msg.payload 
        except Exception as e:
            logging.error(e)
            client.publish(msg.topic+"/error", payload=str(e), retain=True)

instance = Switch()
