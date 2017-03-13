import logging
import datetime
import json
import subsystem

energy_topic = "energy/kwh"
meter = ["heatpump", "global", None, None]
class Energy(subsystem.Subsystem):
    def __init__(self):
        super().__init__()
        self.topic = "devices/m-duino/emontx"
        self.prev = None
        self.last = None

    def on_message(self, client, message):
        cur = datetime.datetime.now()
        energy = json.loads(message.payload.decode("utf-8") )

        if self.prev != None:
            elapsed = (cur - self.prev)
            logging.debug("elasped: {} seconds".format(elapsed.total_seconds()))
            elapsed = elapsed.total_seconds() / 3600
        self.prev = cur

        if self.last != None:
            consumption = dict()
            for i in range(len(energy['ct'])):
                if meter[i] != None:
                    kwh = (energy['ct'][i]+self.last[i])/2000 * float(elapsed)
                    logging.debug("{}: {:.10f} kWh".format(meter[i], kwh))
                    consumption[meter[i]] = "{:.10f}".format(kwh)
            client.publish(self.root_topic + energy_topic, payload = json.dumps(consumption))
        self.last = energy['ct']

instance = Energy()
