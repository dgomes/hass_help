import logging

relay_topic = "devices/m-duino/relay/{}/set"

class Subsystem():
    def __init__(self):
        self.topic = "#"
        self.root_topic = "hass_helper/"
        self.state = {}
        logging.info("Loading {}".format(self.__class__.__name__))

    def on_message(self, client, message):
        logging.info("Not implemented!")
        pass
