import logging
import datetime
import json
import subsystem
import re

state_topic = "covers/{}"
command_topic = "covers/{}/set"

# tuple -> up, down, time_up, time_down
covers = {
    'sala_grande': (8, 3, 17000, 15000),
    'sala_pequena': (5, 4, 17000, 15000),
    'frente': (2, 1, 15000, 15000),
    'suite': (102,103,20000, 18000),
    'david': (101,106, 9000, 8000),
    'helena': (104,107, 20000, 14000)
    }

class Cover(subsystem.Subsystem):
    def __init__(self):
        super().__init__()
        self.topic = [(self.root_topic + command_topic.format(cover), 0) for cover in covers.keys()] 
    
    def on_message(self, client, msg):
        try: 
            cover = re.search(command_topic.format('(.+?)'), msg.topic).group(1)
            up,down,time_up,time_down = covers[cover]
                
            if "OPEN" in str(msg.payload):
                logging.info("{} OPEN".format(cover))
                client.publish(subsystem.relay_topic.format(up), payload=time_up)
                state = "100"
            elif "CLOSE" in str(msg.payload):
                logging.info("{} CLOSE".format(cover))
                client.publish(subsystem.relay_topic.format(down), payload=time_down)
                state = "0"
            elif "STOP" in str(msg.payload):
                logging.info("{} STOP".format(cover))
                client.publish(subsystem.relay_topic.format(up), payload="false")
                client.publish(subsystem.relay_topic.format(down), payload="false")
                state = "50"
            client.publish(self.root_topic + state_topic.format(cover), payload=state, retain=True)
        except Exception as e:
            logging.error(e)
            client.publish(msg.topic+"/error", payload=str(e), retain=True)

instance = Cover()
