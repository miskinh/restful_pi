import os
from flask import Flask, request
from flask.ext.cors import CORS
from flask.ext.restful import Api, Resource, reqparse

from devicesAttached import getAttachedDevices

class Devices(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		
	def get(self):
		"List outputs"
		
		return getAttachedDevices()

"""
class LightID(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

	def put(self,lightID):
		"Update given output"

		light = request.get_json()
		print light
		success = lightsGPIO.setLight(light)
			
		return True
"""