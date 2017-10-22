# Continuously Learning Artificial Intelligence Rules Engine (Claire) for Smart Homes

Claire is a smart home rules engine designed to make my home truly intelligent by having my home adapt to my habits. By using deep learning techniques Claire learns my behaviors and will automatically execute automations based on my habits.

With Claire I want to eliminate the need for reaching for a remote, my phone, or program an advanced rules engines. Instead the Artificial Intelligence will learn from my actions and automatically control my devices once it is confident enough.

This document details how I've build the Claire engine to automate my home.

## My Home Automation Setup

In my home I have Z-Wave devices in two rooms, my living room and my office, that I hope to be able to automate.

I have the following devices:
- Motion detector in the living room (Motion 1)
- Light dimmer in the living room (Light 1)
- Power Switch w. power monitor for my AV and TV system in the living room (Switch 1)
- Remote in the living room (Remote 1)
- Light dimmer in the office (Light 2)
- Remote in the office (Remote 2)
- Motion detector w. light sensor in the office (not here yet) (Motion 2)
- Raspberry Pi 3 with UZB running Z/IP

I hope to be able to automate the following actuators:
- Light 1
- Light 2
- Swith 1

Based on the sensors:
- Motion 1
- Motion 2
- Switch 1 power monitor

## Phase 1: Data Gathering
In the first phase I want to setup a script to continuously log the state of my devices and save them into a database. This will allow me to later use this information to train a machine learning algorithm to learn my habits.

To get started I installed the Raspberry Pi image as detailed here: http://zwavepublic.com/developer, plugged in the Z-Wave bridge adapter and booted the Raspberry Pi.

Next I accessed the Z-Ware sample gateway software using https://raspberrypi.local/ui/pc/index.html and setup my network by installing all my devices.

Next I started building the data gathering script.

### Data Gathering Script
To start gathering data I must first decide on a data store and a data structure.

To enable me to have maximum flexibilty in data structure and data mobility and distribution I have selected to store my data in [CouchDB](http://couchdb.apache.org/). CouchDB is a highly scalable no-SQL database. I works well as both a simple single instance database on an embedded device, and in a cluster mode for large installation. Additionally CouchDB also implements a data replication protocol that could enable me to later easily replicate data from my gateway device into the cloud for advanced machine learning processing without having to change the initial data gathering script.

In terms of data structure CouchDB allows us to store JSON documents directy into the database. I build a simple python object model for my home and a few simple home automation device types, each model has a to_dict method allowing me to easily dump the entire state of my home into a dictionary that can be stored directly in CouchDB.

To get the actual status of my devices I create a python script based on the very simple [PyZWare](https://github.com/Z-WavePublic/PyZWare) API. The script will continuously read the status of my Z-Wave devices and log the status to the database on the following conditions:
- Every 1 minute
- Whenever a state has changed on any device






## Phase 2: Learning
In phase 2 I plan to use the data gathered to build a neural network that takes my current house state (sensor states, devices states, times etc.) as inputs and predicts my next house state as an output.

## Phase 3: Automation
In phase 3 I plan to put the network to work. I will integrate the neural network with the Z/IP gateway so I can continously read the current state of my home and use that to predict any changes to the state based on sensor data.
The network will predict either every few minutes or whenever a sensor triggers or state changes and execute any changes to the house state. For example it should be able to learn simple rules like: whenever the movement sensor in the hallway triggers it should turn the light on and if it's after 10pm set it to 50%.

## Phase 4: Online Learning
For the final state I will convert the neural network from using just historical data obtained in phase 1 to use the endless stream of data from my home. This online learning algorithm will enable CLAIRE to continuouslylearn evolving habits and be able to receive performance input using my Google home (e.g. OK Google! Bad automation).
