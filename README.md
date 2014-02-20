BeagleDash
==========

This repository is for CAN communication using Python. The platform used for testing is a BeagleBone Black running Arch Liux ARM using a MCP2562 CAN transciever on CAN interface can0.

Dependencies:
Python 3.3.x

https://bitbucket.org/hardbyte/python-can

Files:

CANtoUDP.py
Purpouse of this file is to decode the CAN data recieved on the can0 interface according to the setup in the liferacing software. Each dataslot in each dataframe for each unique frame ID is wrapped in an UPD package in order to send this to a remote client.