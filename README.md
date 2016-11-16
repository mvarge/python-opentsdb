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
