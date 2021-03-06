import re

from shared import *

class DevicesAttached():

  def __init__(self,routerURL="http://192.168.0.1/"):
    self.routerURL = routerURL

  def splitDeviceString(self,devicesString):
    "Splits the given deviceString and returns a list of device lists"

    devices = []
    deviceList = devicesString.split('<lf>')

    for deviceString in deviceList:
      device = deviceString.split(',')
      devices.append(device)

    return devices

  def getDevicesList(self):
    "returns a list of devices attached to the router who URL constructed class"

    routerContent = getURL(self.routerURL)

    if not routerContent: return []

    pattern = re.compile(r"attach_dev = '(.*)';")
    matches = re.search(pattern, routerContent, flags=0)

    return self.splitDeviceString(matches.group(1))

  def setOwner(self,mac,owner):
    "Sets the given mac address to the given owner"

    filename = "owners.json"

    try:
      owners = loadJSON(filename)
    except IOError:
      owners = {}
      
    owners[mac] = owner
    saveJSON(filename,owners)

  def getOwner(self,mac):
    "looks up in the known mac address table to see if the owner is known"

    try:
      owners = loadJSON("owners.json")
    except IOError:
      owners = {}

    try:
      owner = owners[mac]
    except KeyError:
      owner = "other"

    return owner

  def setAttachedDevices(self):

    self.devices = []

    devicesList = self.getDevicesList()

    for device in devicesList:
      [name,mac,connection] = device
      owner = self.getOwner(mac)

      self.devices.append({
        "name" : name,
        "owner" : owner,
        "mac" : mac,
        "connection" : connection
        })

  def getAttachedDevices(self):

    self.setAttachedDevices()
    return self.devices

  def getActiveOwners(self):

    self.setAttachedDevices()

    owners = {"henry":0,"ilan":0,"steve":0}

    for device in self.devices:
      if device["owner"] in owners.keys():
        owners[device["owner"]] += 1

    return owners
