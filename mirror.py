#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 Paulo Jerônimo
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

__author__='Augusto Ícaro(icaro_morpheus@gmail.com, contact@augustoicaro.com), Shinichi Katayama, Paulo Jerônimo (paulojeronimo@gmail.com)'

# This code is a reduction / adaptation of mirrorrr project 
# (http://code.google.com/p/mirrorrr/ by Brett Slatkin) 
# held specifically to achieve the goals to build a proxy for files in an 
# account published in the DropBox. 
# If you want a full proxy to run on GAE, use the mirrorr.

# Set up your Dropbox user number here:
DROPBOX_USER = ''

# Set up your Dropbox user number here:
GITHUB_USER = ''

# Specify a default page to display when a directory is accessed
DIRECTORY_INDEX = 'index.html'

# Directory list that are redirected to the index.html in folder.
# For example, access to http://example.com/dir is translated to
# http://example.com/dir/index.html
# Directory path must begin with a leading slash.
DIRECTORIES = frozenset([
  '/3.0.5/examples',
  '/teste',
])

# Directory list that are redirected to the index.html in folder.
# For example, access to http://example.com/dir is translated to
# http://example.com/dir/index.html
# Directory path must begin with a leading slash.
DIRECTORIESGITHUB = frozenset([
  '/pathfinder_combat',
  '/pfcombat',
])

# Directory list that are redirected to typed url in folder.
# For example, access to http://example.com/dir/image.jpg is translated to
# http://example.com/dir/image.jpg
# Directory path must begin with a leading slash.
DIRECTORIESDROPBOX= frozenset([
  '/release',
])

# Directory list that are redirected the main page to index.html
# For example, access to http://example.com/ is translated to
# http://example.com/index.html
ROOT = frozenset([
  '/',
  '',
])

#Set default address to case you use 2 or more sites to redirect
address = DROPBOX_PREFIX + DROPBOX_USER
DROPBOX_PREFIX ='/dl.dropbox.com/u/'
GITHUB_POSFIX ='github.io'
DROPBOX = DROPBOX_PREFIX + DROPBOX_USER
GITHUB = GITHUB_USER + GITHUB_POSFIX
#Variables for structure of typed url
FOLDER = ""
SUBFOLDER = ""
REMAINDER = ""
DEBUG = False
HTTP_PREFIX = "http://"
IGNORE_HEADERS = frozenset([
  'set-cookie',
  'expires',
  'cache-control',
  # Ignore hop-by-hop headers
  'connection',
  'keep-alive',
  'proxy-authenticate',
  'proxy-authorization',
  'te',
  'trailers',
  'transfer-encoding',
  'upgrade',
])

import logging
import wsgiref.handlers

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.runtime import apiproxy_errors

class MirroredContent(object):
  def __init__(self, original_address, translated_address,
               status, headers, data, base_url):
    self.original_address = original_address
    self.translated_address = translated_address
    self.status = status
    self.headers = headers
    self.data = data
    self.base_url = base_url

  @staticmethod
  def fetch_and_store(base_url, translated_address, mirrored_url):
    """Fetch a page.
    
    Args:
      base_url: The hostname of the page that's being mirrored.
      translated_address: The URL of the mirrored page on this site.
      mirrored_url: The URL of the original page. Hostname should match
        the base_url.
    
    Returns:
      A new MirroredContent object, if the page was successfully retrieved.
      None if any errors occurred or the content could not be retrieved.
    """
    logging.debug("Fetching '%s'", mirrored_url)
    try:
      response = urlfetch.fetch(mirrored_url)
    except (urlfetch.Error, apiproxy_errors.Error):
      logging.exception("Could not fetch URL")
      return None

    adjusted_headers = {}
    for key, value in response.headers.iteritems():
      adjusted_key = key.lower()
      if adjusted_key not in IGNORE_HEADERS:
        adjusted_headers[adjusted_key] = value

    return MirroredContent(
      base_url=base_url,
      original_address=mirrored_url,
      translated_address=translated_address,
      status=response.status_code,
      headers=adjusted_headers,
      data=response.content)
      
#You MUST change the fuction get for your needs and get_directory if necessary
class MirrorHandler(webapp.RequestHandler):
  def get_directory_path(self):
    logging.debug('Typed url = "%s"', self.request.url)
    slash = self.request.url.find("/", len(self.request.scheme + "://"))
    logging.debug('Start = %d - Slash = "%d"',len(self.request.scheme + "://"), slash)
    #Slash for folder
    if slash != -1:
      slash2 = self.request.url.find("/", slash+1)
      logging.debug('Slash2 = "%d"', slash2)
    #slash for subfolder
    if slash2 != -1:
      slash3 = self.request.url.find("/", slash2+1)
      logging.debug('Slash3 = "%d"', slash3)
      global FOLDER
      FOLDER = self.request.url[slash:slash2]
      if FOLDER != "":
        global REMAINDER
        REMAINDER = self.request.url[slash2:]
      if slash3 != -1:
        global SUBFOLDER
        SUBFOLDER = self.request.url[slash2:slash3]
        if SUBFOLDER != "":
    if SUBFOLDER == FOLDER:
            slash_aux = self.request.url.find("/", slash3+1)
	    SUBFOLDER = self.request.url[slash3:slash_aux]
            global REMAINDER
            REMAINDER = self.request.url[slash_aux:]
          else:
            global REMAINDER
            REMAINDER = self.request.url[slash3:]
    if slash == -1:
      return ""
    return self.request.url[slash:]

  def get_relative_url(self, directory_path):
    if directory_path == "":
      return "/"
     
    return address + directory_path

  def get(self, base_url):
    logging.debug('User-Agent = "%s", Referrer = "%s"',
                  self.request.user_agent,
                  self.request.referer)
    logging.debug('Base_url = "%s", url = "%s"', base_url, self.request.url)
    global FOLDER
    FOLDER = ""
    global SUBFOLDER
    SUBFOLDER = ""
    global REMAINDER
    REMAINDER = ""
    directory_path = self.get_directory_path()
    if REMAINDER == "/":
      REMAINDER = ""
    logging.debug('Directory_path = "%s"', directory_path)
    logging.debug('Folder = "%s"', FOLDER)
    logging.debug('SubFolder = "%s"', SUBFOLDER)
    logging.debug('Remainder = "%s"', REMAINDER)
    if FOLDER in DIRECTORIES:
      logging.debug('Directory_path in DIRECTORIES') 
      global address
      address =  DROPBOX
      directory_path = directory_path + SUBFOLDER + REMAINDER + '/' + DIRECTORY_INDEX
    elif ((FOLDER in DIRECTORIESGITHUB or directory_path in DIRECTORIESGITHUB) and SUBFOLDER == "" ) and REMAINDER == "":
      logging.debug('Directory_path in DIRECTORIESGITHUB WITH INDEX')
      global address
      address = GITHUB
      directory_path = "/pathfinder_combat" + SUBFOLDER + REMAINDER + '/' + DIRECTORY_INDEX
    elif FOLDER in DIRECTORIESGITHUB and (SUBFOLDER != "" or REMAINDER != ""):
      if SUBFOLDER in DIRECTORIESDROPBOX:
        logging.debug('Directory_path in DIRECTORIESGITHUB ON DROPBOX')
        global address
        address = DROPBOX
      else:
        logging.debug('Directory_path in DIRECTORIESGITHUB')
        global address
        address = GITHUB
        directory_path = "/pathfinder_combat" + SUBFOLDER + REMAINDER
    elif directory_path in ROOT:
      logging.debug('Directory_path in ROOT') 
      global address
      address =  "/dl.dropbox.com/u/11608077"
      directory_path = directory_path + DIRECTORY_INDEX
    else:
      logging.debug('Directory_path is NOTHING') 
      global address
      address =  DROPBOX
    translated_address = self.get_relative_url(directory_path)[1:]  # remove leading /
    logging.debug('Translated_address = "%s"', translated_address)
    content = MirroredContent.fetch_and_store(base_url, translated_address,
      HTTP_PREFIX + translated_address)
    if content is None:
      return self.error(404)
    for key, value in content.headers.iteritems():
      self.response.headers[key] = value
    self.response.out.write(content.data)


app = webapp.WSGIApplication([
  (r"/([^/]*).*", MirrorHandler)
], debug=DEBUG)


def main():
  wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
  main()
