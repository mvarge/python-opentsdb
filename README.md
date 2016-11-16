# python-opentsdb
Python OpenTSDB API for sending points

## About
This program was developed for sending points to an OpenTSDB API. It supports both TCP and UDP, and the protocol is dynamically defined during the module initialization.

## Use

1. Import and Create an OpenTSDB object.
2. Create a point.
3. Customize your point: Metric name, metric value, custom tags, etc.
4. Add your point to your OpenTSDB object.
5. Send it.

## Examples

```
$ python
Python 2.7.5 (default, Nov 20 2015, 02:00:19) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from opentsdb import OpenTSDB
>>> opentsdb = OpenTSDB(url="http://foo.bar/api/put", ksid="foobarksid")
>>> point = opentsdb.point()
>>> point.metric = 'ps.test'
>>> point.value = 20
>>> point.tag(foo='bar')
>>> opentsdb.add(point)
>>> point.value = 13
>>> point.tags['foo'] = 'other_bar'
>>> opentsdb.add(point)
>>> opentsdb.send()
Sending: [{"timestamp": 1479293415774, "metric": "ps.test", "value": 13.0, "tags": {"host": "centos7", "foo": "other_bar", "ksid": "foobarksid"}}, {"timestamp": 1479293415774, "metric": "ps.test", "value": 13.0, "tags": {"host": "centos7", "foo": "other_bar", "ksid": "foobarksid"}}]
```

If you want to use UDP instead TCP the only difference applies during the OpenTSDB object initialization:

```
$ python
Python 2.7.5 (default, Nov 20 2015, 02:00:19) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from opentsdb import OpenTSDB
>>> opentsdb = OpenTSDB(ip='1.2.3.4', port=4243, ksid="foobarksid")
>>> point = opentsdb.point()
>>> point.metric = 'ps.test'
>>> point.value = 13
>>> opentsdb.add(point)
>>> opentsdb.send()
Sending: {'timestamp': 1479293551456, 'metric': 'ps.test', 'value': 13.0, 'tags': {'host': 'centos7', 'ksid': 'foobarksid'}}
```

If you choose to send multiple points at the same time you can either use a bigger payload using TCP or multiple sockets using UDP. Again, the module will take care of this step for you:

```
>>> point.value = 13
>>> opentsdb.add(point)
>>> point.value = 15
>>> opentsdb.add(point)
>>> point.value = 18
>>> opentsdb.add(point)
>>>
>>> opentsdb.send() # TCP (Single payload via POST)
Sending: [{"timestamp": 1479294132374, "metric": "ps.test", "value": 18.0, "tags": {"host": "centos7", "ksid": "foobarksid"}}, {"timestamp": 1479294132374, "metric": "ps.test", "value": 18.0, "tags": {"host": "centos7", "ksid": "foobarksid"}}, {"timestamp": 1479294132374, "metric": "ps.test", "value": 18.0, "tags": {"host": "centos7", "ksid": "foobarksid"}}]
>>> opentsdb.send() # UDP (Multiple UDP sockets)
Sending: {'timestamp': 1479294014351, 'metric': 'ps.test', 'value': 18.0, 'tags': {'host': 'centos7', 'ksid': 'foobarksid'}}
Sending: {'timestamp': 1479294014351, 'metric': 'ps.test', 'value': 18.0, 'tags': {'host': 'centos7', 'ksid': 'foobarksid'}}
Sending: {'timestamp': 1479294014351, 'metric': 'ps.test', 'value': 18.0, 'tags': {'host': 'centos7', 'ksid': 'foobarksid'}}
```

## Author

Marcelo Varge
(marcelo.varge@gmail.com)
