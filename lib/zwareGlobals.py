# Copyright 2016 Sigma Designs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); # you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software # distributed under the License is distributed on an "AS IS" BASIS, # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and # limitations under the License.
#

#This file is used to track global variables in PyZWare
BINARY_SWITCH_INTERFACE = 37
BINARY_SENSOR_INTERFACE = 48
MULTILEVEL_SENSOR_INTERFACE = 49
device_interface_list = [BINARY_SWITCH_INTERFACE,BINARY_SENSOR_INTERFACE,MULTILEVEL_SENSOR_INTERFACE]
device_dictionary_list = {}
for interface in device_interface_list:
	device_dictionary_list[interface] = {}
	device_dictionary_list[interface]['defaultState'] = -1
	device_dictionary_list[interface]['foundDevice'] = 0
	device_dictionary_list[interface]['tempFoundDevice'] = 0	
	device_dictionary_list[interface]['previouslyFoundDevice'] = 0
	device_dictionary_list[interface]['ifdDevice'] = 0
runPollingThread = True
debugData = None
binarySwitchButton = None
zwareSession = None
zwareUrl = ""
