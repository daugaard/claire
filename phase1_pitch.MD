# Continuously Learning Artificial Intelligence Rules Engine  for Smart Homes
One of the limitations of current smart home apps, hubs and gateways are the way you control your home. Today you typically pull out your phone or communicate through Alexa or Google Home to activate preprogrammed scenes and devices.

What if instead your smart home could learn from your actions and sensors, and automatically execute automation based on prior experience?

__*Introducing the Continuously Learning Artificial Intelligence Rules Engine (CLAIRE)*__

CLAIRE is a smart home rules engine designed to make your home truly intelligent by having your home adapt to your habits. By using deep learning techniques CLAIRE learns your behavior and will automatically execute automations based on your habits.

CLAIRE wants to eliminate the need for reaching for your phone, or program an advanced rules engines, to do routine tasks like turning the light on when you enter a room or automatically adjust the temperature when you come home.

I plan to implement the project in 4 phases.
## Phase 1: Data Gathering
In this phase I plan to use the Z/IP gateway to setup a data logging device that will log the status of my home automation devices every few minutes and whenever a sensor state changes.

## Phase 2: Learning
In phase 2 I plan to use the data gathered to build a neural network that takes my current house state (sensor states, devices states, times etc.) as inputs and predicts my next house state as an output.

## Phase 3: Automation
In phase 3 I plan to put the network to work. I will integrate the neural network with the Z/IP gateway so I can continously read the current state of my home and use that to predict any changes to the state based on sensor data.
The network will predict either every few minutes or whenever a sensor triggers or state changes and execute any changes to the house state. For example it should be able to learn simple rules like: whenever the movement sensor in the hallway triggers it should turn the light on and if it's after 10pm set it to 50%.

## Phase 4: Online Learning
For the final state I will convert the neural network from using just historical data obtained in phase 1 to use the endless stream of data from my home. This online learning algorithm will enable CLAIRE to continuouslylearn evolving habits and be able to receive performance input using my Google home (e.g. OK Google! Bad automation).
