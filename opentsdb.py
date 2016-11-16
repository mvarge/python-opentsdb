import time
import socket
import json
import requests

# DEFAULT OPTIONS
TIMEOUT = 5

class OpenTSDB(object):

    def __init__(self, **kwargs):
        """This class constructor is intended to be dynamic. The type of
        protocol used for transmiting the data is defined based on what
        arguments have you passed here, for instance:
        o = OpenTSDB(url="http://foobar/api/put", ksid="ts_foobarID") # TCP
        o = OpenTSDB(ip="1.2.3.4", port=4243, ksid="ts_foobarID") # UDP
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if hasattr(self, 'url'):
            self._type = 'tcp'
            self._session = requests.Session()
            self._session.headers = {"Content-Type": "application/json"}
            setattr(self.__class__, 'send', tcp)
        if hasattr(self, 'ip'):
            self._type = 'udp'
            socket.setdefaulttimeout(TIMEOUT)
            self._sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            setattr(self.__class__, 'send', udp)
        self._payload = []

    def point(self):
        """Returns a point object"""
        return Point()

    def add(self, point):
        """Adds a point to your payload"""
        if not isinstance(point, Point):
            return
        point.timestamp = get_timestamp()
        point.value = assert_digit(point.value)
        point.tags['ksid'] = self.ksid
        self._payload.append(point.transform())


class Point(object):

    def __init__(self):
        """Generic class for dynamic point construction"""
        for attr, value in SKEL.items():
            setattr(self, attr, value)

    def transform(self):
        """Simply returns itself as a dict"""
        return self.__dict__

    def tag(self, **kwargs):
        """Use this for defining custom tags for your point"""
        self.tags.update(kwargs)


def tcp(self):
    """TCP sender class based on requests"""
    payload = json.dumps(self._payload)
    print("Sending: {0}".format(payload))
    r = self._session.post(self.url, data=payload, timeout=TIMEOUT)

def udp(self):
    """UDP sender class based on socket"""
    for point in self._payload:
        print("Sending: {0}".format(point))
        self._sock.sendto(json.dumps(point), (str(self.ip), int(self.port)))

def assert_digit(value):
    try:
        return float(value)
    except ValueError:
        return value

def get_timestamp():
    return int(round(time.time() * 1000))

SKEL = {
    "metric": '',
    "timestamp": '',
    "value": '',
    "tags": {
        "host": socket.gethostname(),
        },
    }
