## THIS PROJECT IS NO LONGER MAINTAINED - LINKS IN THIS README WILL LIKELY NOT WORK

# Continuously Learning Artificial Intelligence Rules Engine (Claire) for Smart Homes

Claire is a smart home rules engine designed to make my home truly intelligent by having my home adapt to my habits. By using deep learning techniques Claire learns my behaviors and will automatically execute automations based on my habits.

With Claire I want to eliminate the need for reaching for a remote, my phone, or program an advanced rules engines. Instead the Artificial Intelligence will learn from my actions and automatically control my devices once it is confident enough.

This document details how I've build the Claire engine to automate my home.

## My Home Automation Setup

In my home I have Z-Wave devices in two rooms, my living room and my office, that I hope to be able to automate.

I have the following devices:
- Motion detector in the living room (Motion 1)
- Z-Wave enabled light bulb dimmable in the living room (Light 1)
- Power Switch w. power monitor for my AV and TV system in the living room (Switch 1)
- Remote in the living room (Remote 1)
- Light dimmer in the office (Light 2)
- Remote in the office (Remote 2)
- Motion detector w. light sensor in the office (Motion 2)
- Raspberry Pi 3 with UZB running Z/IP

I hope to be able to automate the following actuators:
- Light 1
- Light 2
- Switch 1

Based on the sensors:
- Motion 1
- Motion 2
- Switch 1 power monitor

## Solution design
The main design goal for my project is to create a simple, flexible and scalable solution. I want to make sure I split the solution into key parts that can run separately to enable me to have maximum flexibility during development and when running the project.

To accommodate this structure I have split the solution into 4 parts:
- Data Gathering
-- This part will monitor the Z-Wave network and store information about my devices and network into a database.
- Learning
-- This part will use the stored data to predict the rules and habits of my home using a machine learning algorithm.
- Automation
-- This part will use the current state of my Z-Wave sensors and the trained machine learning algorithm to predict the wanted state of my actuator devices and execute the state if its different from the current state.   
- Online learning  
-- This part will enable the systemt to learn new habits by continuously training the machine learning algorithm with the latest data from my devices.

## Phase 1: Data Gathering
In the first phase I want to setup a script to continuously log the state of my devices and save them into a database. This will allow me to later use this information to train a machine learning algorithm to learn my habits.

To get started I installed the Raspberry Pi image as detailed here: http://zwavepublic.com/developer, plugged in the Z-Wave bridge adapter and booted the Raspberry Pi.

Next I accessed the Z-Ware sample gateway software using https://raspberrypi.local/ui/pc/index.html and setup my network by installing all my devices.

Next I started building the data gathering script.

### Data Gathering Script
Before gathering data I had to decide on a data store and a data structure. 

To give me maximum flexibility in data structure, and provide scability and data mobility I selected to store my data in [CouchDB](http://couchdb.apache.org/). CouchDB is a highly scalable no-SQL database. I works well as both a simple single instance database on an embedded device, and in a cluster mode for large installation. Additionally CouchDB implements a data replication protocol that could enable me to later easily replicate data from my gateway device into the cloud for advanced machine learning processing without having to change the initial data gathering script.

In terms of data structure CouchDB allows us to store JSON documents directly into the database. I build a simple python object model for my home and a few simple home automation device types, each model has a to_dict method allowing me to easily dump the entire state of my home into a dictionary that can be stored directly in CouchDB.

To get the actual status of my devices I create a python script based on the very simple [PyZWare](https://github.com/Z-WavePublic/PyZWare) API.

The script will continuously read the status of my Z-Wave devices and save the status of my home to the database on the following conditions:
- Every 1 minute
- Whenever a state has changed on any device

The current status of my device will be saved in a JSON document in the database along with a time stamp. 

## Phase 2: Learning
In phase 2 I need to build a machine learning model that can learn the "rules" of my home and predict the wanted state of my Z-Wave devices based on the sensors in my house.

### Moving data from the Raspberry Pi to my laptop
Building and training machine learning algorithms can be very resource intensive so we do not necessarily want to do this on the Raspberry Pi. Instead I move the data of the Raspberry Pi to my laptop (this could as well be into a cloud service but for my home my laptop will do).

Since I am using CouchDB I simply use the built-in replication protocol that allows me to setup replication between the Raspberry Pi database server and my laptops database server in minutes.

### Defining the machine learning problem
I see the machine learning problems as a classic classification problem where we want to predict the state of my actuator devices based on the state of my sensor devices in my home.

As inputs to my machine learning problem I will use all the sensor data from my home as well as the time stamp. This will allow my model to react to not only sensor data, but also take the time and day into account. _For example: tripping the movement sensor in the living in the morning may need to execute a different automation than tripping it in the evening._

I use one-hot encoding to encode the timestamp as a 3 categorial values: weekday, hour and minute in 10-minute intervals.  

#### Testing and visualizing the machine learning model
To validate and test the machine learning models I measure the models classification accuracy using a hold-out validation method with a split of 80% training and 20% test data.

Additionally to better visualize the model I created a web-based interface. The web interface allows the user to set the status of the input devices and the timestamp, and then execute the model to see the state of the output device. This allows me to test the algorithms without having to hook it up to my actual devices.

I've setup a publicly available version of the version tester you can access here: http://claire.practicalai.io/. Its running the latest version of the model so you can test the model yourself.

### Picking a machine learning model
For my machine learning model I will use the Random Forest algorithm. The random forest algorithm is an easy to use machine learning algorithm that works for both classification and regression problems. The algorithm is good at isolating the signal from noise in data and has a natural resilience to overfitting.

To build my models I use the scikit learn library from python.
To install scikit learn and its dependencies for python 3 run: pip3 install numpy sklearn scipy.


#### Model 1 - One model to rule them all
My first attempt was to create one machine learning model to predict all my output devices in one go. The model would take all my input devices and the encoded timestamp as input, and output the state of all my switches and dimmers as the output.

This model did achieve a high accuracy score, but when I put the model to the test in my model visualizer I noticed that it would never turn on my power switch on.

Upon further investigation this was because the switch state is directly associated with one of the input parameters, the power monitor. Having a direct correlation between the input and output parameter meant the model was not able to properly learn when to turn the switch on.

#### Model 2 - Divide and conquer
For my second model I decided to split the problem into one machine learning problem for each actuator.

I trained one model for each of my output devices, and for each output device I created a model that took all input sensors, except if the sensor is from the output device we are trying to predict, and an encoded timestamp as input. The output of the models would be the state of that specific device.

This model worked quite well so I decided to put it into use in my home.

## Phase 3: Automation
In phase 3 I combined the data logging script with the automation models I created in step 2.

The automation script was programmed to continously monitor the Z-Wave network, if it detects any changes to the devices it will run the prediction models and adjust the status of the output devices accordingly. Additionally it will store the state of the network in the CouchDB database so you don't need to have both the datalogger and automation script running at the same time.

After putting the automation script into use, and running it for a few days, I found that the machine learning models have been able to capture the following rules into my home:

    If I am in the office in the morning turn on the lights
    When the sun rises turn off the office lights (around 10:30 to 11am)
    If I am in the office in the afternoon when the sun sets turn on the lights (approx. after 4pm)
    If I am not in the office keep the lights off
    If I am in the living room in the evening turn the light and the AV system on
    When I am in the living room in the morning keep the AV switch and TV light turned off since I am just grabbing breakfast and wont watch TV
    If I am in the living room in the evening on Sundays keep the lights and AV system on, but dim the lights since I am likely watching a movie
    When I leave the living room at night turn off the light and the AV system

I am very impressed with the number of rules the machine learning models managed to capture. Some of these rules I would never had thought to implement myself, but are nonetheless very useful.

An example is how the system learned that on Sunday nights we normally watch a movie and therefore dim the light slightly, or that when I am in the living room in the morning its to eat breakfast and not to watch TV.

The artificial intelligence rules implemented in my automation engine definitely saves me from using my remote or phone to adjust my devices.

One problem is however what happens when I deviate from the rules? What if I suddenly don't want the lights to dim on a Sunday? The last phase will handle this case.

## Phase 4: Online Learning
For the final state I will convert the neural network from using just historical data obtained in phase 1 to use the endless stream of data from my home. This online learning algorithm will enable CLAIRE to continuouslylearn evolving habits and be able to receive performance input using my Google home (e.g. OK Google! Bad automation).
