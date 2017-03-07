import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import logging
import importlib.util
import os
import sys
import time

broker_addr = "192.168.1.10"
log_format = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.info("Home-Assistant Helper v0 - started")

def load_subsystems():
    subsystems = [] 
    
    for entry in os.scandir('.'):
        if entry.is_file() and entry.name.startswith("sub."):
            mod_name = os.path.split(entry.name)[-1][4:][:-3]
            spec = importlib.util.spec_from_file_location(mod_name, entry.name)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            subsystems.append(mod) 

    return subsystems

def on_connect(client, userdata, flags, rc):
    for subsys in userdata:
        logging.debug("Subscribing: {}".format(subsys.instance.topic))
        client.subscribe(subsys.instance.topic)

def on_message(client, userdata, message):
    for subsys in userdata:
        if message.topic in str(subsys.instance.topic):
            return subsys.instance.on_message(client, message)

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
