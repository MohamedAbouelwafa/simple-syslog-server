""" Run a Syslog server
  Author: Mohamed Abouelwafa
"""

import os
import socketserver

class SyslogUDPHandler(socketserver.BaseRequestHandler):
  def handle(self):
    data = bytes.decode(self.request[0].strip())
    socket = self.request[1]
    print("\033[33m{}\033[0m: {}".format(self.client_address[0], data))

if __name__ == '__main__':
  os.system('clear')
  try:
    print('Syslog server is listening on default port 514\n')
    server = socketserver.UDPServer(('0.0.0.0', 514), SyslogUDPHandler)
    server.serve_forever(poll_interval=0.5)
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print('Shutting down ...')
