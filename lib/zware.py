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

import requests
import urllib
from requests import Session
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import sys
from . import zwareGlobals

""" web api wrapper """
def zw_api(uri, parm=''):
        try:
                r = zwareGlobals.zwareSession.post(zwareGlobals.zwareUrl + uri, data=parm, verify=False)
        except:
                assert False, print(sys.exc_info()[0])
        assert r.status_code == 200, r.status_code
        try:
                x = ET.fromstring(r.text)
        except:
                return r.text
        e = x.find('./error')
        assert e == None, e.text
        return x


""" Network operations """
def zw_net_wait():
	while int(zw_api('zwnet_get_operation').find('./zwnet/operation').get('curr_op')):
		pass


def zw_net_comp(op):
	while op != int(zw_api('zwnet_get_operation').find('./zwnet/operation').get('prev_op')):
		pass


def zw_init(url='https://127.0.0.1/', user='test_user', pswd='test_password'):
        zwareGlobals.zwareSession = requests.session()
        zwareGlobals.zwareUrl = url
        zwareGlobals.zwareSession.headers.update({'Content-Type':'application/x-www-form-urlencoded'}) # apache requires this
        zw_api('register/login.php', 'usrname='+ user + '&passwd=' + pswd)
        zwareGlobals.zwareUrl += 'cgi/zcgi/networks//'
        return zw_api('zw_version')

def zw_add_remove(cmd):
	return zw_api('zwnet_add','cmd='+str(cmd))

""" Interfaces """

def zwif_api(dev, ifd, cmd=1, arg=''):
	return zw_api('zwif_' + dev, 'cmd=' + str(cmd) + '&ifd=' + str(ifd) + arg)

def zwif_api_ret(dev, ifd, cmd=1, arg=''):
	r = zwif_api(dev, ifd, cmd, arg)
	if cmd == 2 or cmd == 3:
		return r.find('./zwif/' + dev)
	return r

def zwif_basic_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('basic', ifd, cmd, arg)

def zwif_switch_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('switch', ifd, cmd, arg)

def zwif_level_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('level', ifd, cmd, arg)

def zwif_doorlock_api(ifd, cmd=1, arg=''):
	r = zwif_api('dlck', ifd, cmd, arg)
	if cmd == 2 or cmd == 3:
		return r.find('./zwif/dlck_op')
	elif cmd == 5 or cmd == 6:
		return r.find('./zwif/dlck_cfg')
	return r

def zwif_usercode_api(ifd, cmd=1, arg=''):
	r = zwif_api('usrcod', ifd, cmd, arg)
	if cmd == 1 or cmd == 2:
		return r.find('./zwif/usrcod')
	elif cmd == 4:
		return r.find('./zwif/usrcod_sup')
	return r

def zwif_thermo_list_api(dev, ifd, cmd=1, arg=''):
	r = zwif_api_ret('thrmo_' + dev, ifd, cmd, arg)
	if cmd == 5 or cmd == 6:
		return r.find('./zwif/thrmo_' + dev + '_sup')
	return r

def zwif_thermo_mode_api(ifd, cmd=1, arg=''):
	return zwif_thermo_list_api('md', ifd, cmd, arg)

def zwif_thermo_state_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('thrmo_op_sta', ifd, cmd, arg)

def zwif_thermo_setpoint_api(ifd, cmd=1, arg=''):
	return zwif_thermo_list_api('setp', ifd, cmd, arg)

def zwif_thermo_fan_mode_api(ifd, cmd=1, arg=''):
	return zwif_thermo_list_api('fan_md', ifd, cmd, arg)

def zwif_thermo_fan_state_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('thrmo_fan_sta', ifd, cmd, arg)

def zwif_meter_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('meter', ifd, cmd, arg)

def zwif_bsensor_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('bsensor', ifd, cmd, arg)

def zwif_sensor_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('sensor', ifd, cmd, arg)

def zwif_battery_api(ifd, cmd=1, arg=''):
	return zwif_api_ret('battery', ifd, cmd, arg)

def zwif_av_api(ifd, cmd=1, arg=''):
	r = zwif_api('av', ifd, cmd, arg)
	if cmd == 2 or cmd == 3:
		return r.find('./zwif/av_caps')
	return r

# Extensions needed for CLAIRE

def zwif_multilevel_status(ifd):
    return zwif_api('level', ifd, 3)
