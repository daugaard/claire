import unittest

from lib import *

class ModelsTest(unittest.TestCase):
    def helper_create_home_with_devices(self):
        h = Home()


    def test_can_create_home(self):
        home_id = 0x123AE3
        name = "Test Home"
        h = Home(home_id, name)

        self.assertTrue(h!=None)
        self.assertEqual(home_id, h.home_id)
        self.assertEqual(name, h.name)

    def test_can_generate_json_state_from_home(self):
        home_id = 0x123AE3
        name = "Test Home"
        h = Home(home_id, name)

        d = h.to_dict()
        self.assertEqual(d['name'], name)
        self.assertEqual(d['home_id'], home_id)
        self.assertTrue(d['time'] != None)


    def test_can_generate_json_state_from_home_with_device(self):
        home_id = 0x123AE3
        name = "Test Home"
        h = Home(home_id, name)

        device_id = 23
        device_name = "Device 1"
        state = 255
        bd = BasicDevice(device_id=device_id,state=state, name=device_name)
        h.devices.append(bd)

        d = h.to_dict()

        self.assertEqual(d['name'], name)
        self.assertEqual(d['home_id'], home_id)
        self.assertTrue(d['time'] != None)

        self.assertEqual(len(d['devices']),1)
        self.assertEqual(d['devices'][0]['state'], state)
        self.assertEqual(d['devices'][0]['name'], device_name)
        self.assertEqual(d['devices'][0]['device_id'], device_id)

    def test_can_generate_json_state_from_home_with_devices(self):
        home_id = 0x123AE3
        name = "Test Home"
        h = Home(home_id, name)

        device_id = 23
        device_name = "Device 1"
        state = 255
        bd = BasicDevice(device_id=device_id,state=state, name=device_name)
        h.devices.append(bd)

        device_id_2 = 25
        device_name_2 = "Device 2"
        state_2 = 0
        bd2 = BasicDevice(device_id=device_id_2,state=state_2, name=device_name_2)
        h.devices.append(bd2)

        d = h.to_dict()

        self.assertEqual(d['name'], name)
        self.assertEqual(d['home_id'], home_id)
        self.assertTrue(d['time'] != None)

        self.assertEqual(len(d['devices']),2)
        self.assertEqual(d['devices'][0]['state'], state)
        self.assertEqual(d['devices'][0]['name'], device_name)
        self.assertEqual(d['devices'][0]['device_id'], device_id)

        self.assertEqual(d['devices'][1]['state'], state_2)
        self.assertEqual(d['devices'][1]['name'], device_name_2)
        self.assertEqual(d['devices'][1]['device_id'], device_id_2)

    def test_can_create_basic_device(self):
        device_id = 23
        name = "Device 1"
        state = 255

        d = BasicDevice(device_id=device_id,state=state, name=name)
        self.assertEqual(device_id, d.device_id)
        self.assertEqual(state, d.state)
        self.assertEqual(name, d.name)
