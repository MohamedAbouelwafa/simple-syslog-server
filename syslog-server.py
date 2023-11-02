""" Run a Syslog server
  Author: Mohamed Abouelwafa
"""

import os
import socketserver


class SyslogHandler(socketserver.BaseRequestHandler):
  # Used to assign a different color for each client
  colors = ['\033[33m', '\033[36m', '\033[32m', '\033[35m', '\033[34m', '\033[31m', ]
  client_colors = {}


  def handle(self):
    """ Handle incoming messages
    """
    data = bytes.decode(self.request[0].strip())
    ip_address = self.client_address[0]
    if ip_address not in self.client_colors:
        self.client_colors[ip_address] = self.get_new_color()

    # Print the log message to stdout
    print("{}{}\033[0m: {}".format(self.client_colors[ip_address], ip_address, data))


  def get_new_color(self) -> str:
    """ Get a new color for a new client
    """
    color = self.colors[len(self.client_colors) % len(self.colors)]
    return color


if __name__ == '__main__':
  os.system('clear')
  try:
    print('Syslog server is listening on default port: 514\n')
    server = socketserver.UDPServer(('0.0.0.0', 514), SyslogHandler)
    server.serve_forever(poll_interval=0.5)
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print('Shutting down ...')
