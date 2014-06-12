from app import app
import os
#from models import *
import json
from flask import jsonify
import models

from flask import render_template, url_for

@app.route('/')
def index(root=None):
    acq = models.Company.query.all()

    root = []

    for u in acq:
	root.append(u.root_json())

#	    root = {u.name: list(u.aq) for u in acq}

    return render_template('index.html', root=root)

@app.route('/static/crossfilter/')
def crossfilter(root=None):
    acq = models.Company.query.all()

    root = []

    for u in acq:
	root.append(u.root_json())

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    yelp_data_url = os.path.join(SITE_ROOT, "static/crossfilter/data/yelp_test_set_business.json")
    yelp_data = json.load(open(yelp_data_url))

    return render_template('index2.html', root=root, yelp_data=yelp_data)

"""
#@app.route('/acquisitions.json')
def acquisitions_json():
	acq = model.Company.query.all()
	root = {}
	root [acq.name] = acq.acquisitions
	print jsonify(root)
	return jsonify(root)
"""
"""
class Company:
	def tree_json(self):
		tree = {}
		tree["name"] = self.name
		tree["acquisitions"] = self.acquisitions
		return tree
"""
