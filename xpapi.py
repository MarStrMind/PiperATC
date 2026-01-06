import requests
import json
import time

class mst_xplane_api:
    def __init__(self):
        self._apiroot = "http://localhost:8086/api/v2/"

    def xp_request(self, method, ep):
        hdr = { "Accept": "application/json", "Content-Type": "application/json" }

        rsp = None
        if method == "get":
            rsp = requests.get(self._apiroot + ep, headers=hdr)
        if method == "post":
            rsp = requests.post(self._apiroot + ep, headers=hdr)

        if rsp.status_code == 200:
            return rsp.json()
        else:
            print("[ERR] X-Plane not running, unable to establish connection. Bye.")
            exit()
    
    def find_dataref_id(self, dataref, data):
        drid = -1
        for d in data:
            if d["name"] == dataref:
                drid = d["id"]
                break
        return drid
    
    def get_value_from_dref_id(self, drid):
        val = self.xp_request("get", "datarefs/"+str(drid)+"/value")
        return val
    

#xp = mst_xplane_api()
#drefs = xp.xp_request("get", "datarefs")
#drid = xp.find_dataref_id("sim/cockpit/radios/com1_freq_hz", drefs["data"])
#print(drid)
#freq = xp.get_value_from_dref_id("2469364471024")
#print(freq["data"])

#hdg = xp.get_value_from_dref_id("1898163290664")
#print(hdg["data"])

#drid = xp.find_dataref_id("sim/cockpit/autopilot/heading", drefs["data"])
#print(drid)
#print(tmp["data"][0])