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


# class MainHandler(webapp2.RequestHandler):
#     def get(self):
# #         r = requests.get("http://api.penncoursereview.com/v1/courses/13021/reviews?token=qL_UuCVxRBUmjWbkCdI554grLjRMPY")
# #         # data = json.loads(r.text) # data is a dictionary now

# # #         self.response.write(data.values())

# #         self.response.write(r.text)
#         self.response.write('hello world')

from flask import Flask
import json, requests
import penncoursereview

app = Flask(__name__)
app.config['DEBUG'] = True



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    # print 'hello world'
    # r = requests.get("http://api.penncoursereview.com/v1/courses/13021/reviews?token=qL_UuCVxRBUmjWbkCdI554grLjRMPY")
    # data = json.loads(r.text)
    # z =  data["result"]["values"][0]["ratings"]["rDifficulty"]
    # return json.dumps(data['result']['values'][0]['ratings'])
    cis120 = penncoursereview.CourseHistory("CIS-120")
    print cis120["reviews"]["path"]
    # print 
    return 'hello world'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
