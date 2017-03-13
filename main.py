import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import logging
import importlib.util
import os
import sys
import time 
import importlib

broker_addr = "192.168.1.10"
subsystems_dir = "subs"
log_format = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.info("Home-Assistant Helper v0 - started")

def load_subsystems():
    subsystems = [] 
    
    for entry in os.listdir(subsystems_dir):
        if os.path.isfile(subsystems_dir+"/"+entry):
            p, m = entry.rsplit('.', 1)
            mod = importlib.import_module(subsystems_dir+"."+p)
            instance = getattr(mod, "instance")
            subsystems.append(instance)

    return subsystems

def on_connect(client, userdata, flags, rc):
    for subsys in userdata:
        logging.debug("Subscribing: {}".format(subsys.topic))
        client.subscribe(subsys.topic)

def on_message(client, userdata, message):
    for subsys in userdata:
        if message.topic in str(subsys.topic):
            return subsys.on_message(client, message)

def main():
    client = mqtt.Client(userdata=load_subsystems())
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(broker_addr, 1883, 60)

            client.loop_forever()
        except Exception as e:
            logging.error(e)
            time.sleep(5)


if __name__ == '__main__':
    main()
