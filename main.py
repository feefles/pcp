#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #
# import webapp2
# import penncoursereview
# import requests

PCR_AUTH_TOKEN = 'qL_UuCVxRBUmjWbkCdI554grLjRMPY'
username = 'UPENN_OD_emtz_1000643'
password = 'o448e5mnbutjcji5ufofo630ur'


# class MainHandler(webapp2.RequestHandler):
#     def get(self):
# #         r = requests.get("http://api.penncoursereview.com/v1/courses/13021/reviews?token=qL_UuCVxRBUmjWbkCdI554grLjRMPY")
# #         # data = json.loads(r.text) # data is a dictionary now

# # #         self.response.write(data.values())

# #         self.response.write(r.text)
#         self.response.write('hello world')

from flask import Flask, jsonify, request
import json, requests, yaml
import penncoursereview
from penn import registrar

import profHash

app = Flask(__name__)
app.config['DEBUG'] = True

baseURL = "http://api.penncoursereview.com/v1/"

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/req', methods=['GET'])
@crossdomain(origin='*')
def hello():
    c = request.args["class"]
    history = penncoursereview.CourseHistory(c)
    difficulty = 0
    quality = 0
    rProf = 0
    try:
        r = requests.get(baseURL + history["reviews"]["path"] + "?token="+ PCR_AUTH_TOKEN)
        data =  yaml.load(r.text)
        i = 0
        j = 0
        for section in data["result"]["values"]:
            difficulty+=float(section["ratings"]["rDifficulty"])
            quality+=float(section["ratings"]["rCourseQuality"])
            i+=1
        difficulty = difficulty / i
        quality = quality / i
    except ValueError:
        print 'caught error'
    finally:
        if len(request.args["prof"]) > 0:
            prof = profHash.profHash[request.args["prof"]]
            profReviews = requests.get(baseURL + 'instructors/' + prof[0]["id"] + '/reviews?token=' + PCR_AUTH_TOKEN)
            profReviews = yaml.load(profReviews.text)
            for section in profReviews["result"]["values"]:
                rProf += float(section["ratings"]["rInstructorQuality"])
                j+=1
            rProf = rProf / j
            print rProf
    return json.dumps({'difficulty': difficulty, 'quality': quality, 'prof': rProf})

@app.route('/scheduler', methods=['GET'])
@crossdomain(origin='*')
def schedule():
    # c = request.args['class'].split('-')
    c = [x.strip() for x in request.args['class'].split('-')]
    reg = registrar.Registrar(username, password)
    section = reg.section(c[0], c[1], c[2])
    return json.dumps(section["meetings"])


@app.route('/')
def landing():
    return 'hello world'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


