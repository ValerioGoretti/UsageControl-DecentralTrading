
__version__ = "0.1"
__all__ = ["DTpod_service"]
__author__ = "bones7456"
__home_page__ = "http://li2z.cn/"
import html
import xmlrpc
from DTsubscription_oracle import DTsubscription_oracle
import os
from DTauthenticator import DTauthenticator
import posixpath
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.server
import urllib
import cgi
import shutil
import mimetypes
import re
try:
    from io import StringIO
except ImportError:
    from io import StringIO
from DTaddresses import *
"""
Class that implements the pod's web service.
The class allows the pod to deliver on demand data through the HTTP protocol
"""
class DTpod_service(BaseHTTPRequestHandler):
                
    server_version = "SimpleHTTPWithUpload/" + __version__
    authenticator=DTauthenticator()
    """
    Initializer of the class
    """
    def __init__(self, pod_pk,*args):
        self.pod_pk=pod_pk
        self.subscription_oracle=DTsubscription_oracle(DTSUBSCRIPTION,self.pod_pk)
        BaseHTTPRequestHandler.__init__(self, *args)

    """
    Handling of GET requests. 
    Can only be internallt invoked by the do_POST() function.
    Deliver the resource in the HTTP response.
    """
    def do_GET(self,auth_token=None,claim=None,id_subscription=None): 
        if auth_token==claim==id_subscription==None:
            self.send_error(400, "Bad request")
            return None
        if not self.authenticator.authenticate(self.path,auth_token,claim):
            self.send_error(400, "Authentication failed, bad request")
            return None
        if not self.subscription_oracle.pull_subscription_verification(int(id_subscription),claim):
            self.send_error(400, "Subscription not verified, bad request")
            return None
        f = self.send_head()     
        result=f.read()
        if f:            
            if type(result)==type("a"):
                self.wfile.write(bytes(result,'utf-8'))
            else:
                self.wfile.write(result)
            f.close()
    """
    Handling of POST requests. 
    After the extraction of the POST body parameters from the request, it invokes the do_GET() function.
    """  
    def do_POST(self):
        claim=None
        auth_token=None
        try:
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        except Exception:
            self.send_error(400,"Bad Request")
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = self.headers.get('content-length')
            fields = cgi.parse_multipart(self.rfile, pdict)
            try:
                auth_token = fields.get('auth_token')[0]
                claim=fields.get("claim")[0]
                id_subscrption=fields.get("id_subscription")[0]
            except Exception:
                auth_token=None
                claim=None

        self.do_GET(auth_token,claim,id_subscrption)
        
   
      
    """
    Sets the head of the HTTP response.
    """ 
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            else:
                self.send_error(404,"Pod resource not found")
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "Pod resource not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.end_headers()
        return f
    """
    Standardizes the URL path pointing to the requested resource.
    """     
    def translate_path(self, path):
     
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.server.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
    """
    Defines the type of the requested resource.
    """ 
    def guess_type(self, path):

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

"""
Wrapper class used to create Stoppable instances of HTTP servers.
"""      
class StoppableHTTPServer(HTTPServer):

    stopped = False
    allow_reuse_address = True
    """
    Class initializer.
    """  
    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.base_path=args[2]

    """
    Puts the server on listening of HTTP requests.
    """
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()
    """
    Stops the requests listening.
    """
    def force_stop(self):
        print("Stopping server...")
        self.server_close()
        self.stopped = True


