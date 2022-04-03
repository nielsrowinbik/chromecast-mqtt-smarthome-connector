import os

def getenv(varname, default):
    file_path = os.getenv(varname + "_FILE")

    if (file_path != None):
        val = open(file_path, "r").read()
    else:
        val = os.getenv(varname, default)

    return val

class Config:

    def __init__(self):
        self.addr = getenv('MQTT_HOST', '127.0.0.1')
        self.port = int(getenv('MQTT_PORT', 1883))
        self.user = getenv('MQTT_USER', False)
        self.password = getenv('MQTT_PASSWORD', False)
        self.cafile = getenv('MQTT_CAFILE', None)
        self.log_level = int(getenv('LOG_LEVEL', 20))

    def get_mqtt_broker_address(self):
        return self.addr

    def get_mqtt_broker_port(self):
        return self.port

    def get_mqtt_broker_use_auth(self):
        return (self.user and self.password)

    def get_mqtt_broker_username(self):
        return self.user

    def get_mqtt_broker_password(self):
        return self.password

    def get_mqtt_client_cafile(self):
        return self.cafile

    def get_log_level(self):
        return self.log_level
