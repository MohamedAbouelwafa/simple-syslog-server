""" Simple Syslog Server

  This script will run a simple Syslog Server locally on the machine.
  The Syslog Server listens on port 514 for incoming Syslog messages from different clients.

  By default, the Syslog Server will print the log messages to stdout.

  Usage:
    python3 syslog-server.py [-save-logs]

  Options:
    -save-logs: Save the log messages to a file with the client IP address as the filename

  Author:
    Mohamed Abouelwafa
    v1.0: 20231102
"""

import os
import socketserver
import argparse


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

    # If -save-logs command line argument is provided
    # Write the log message to a log file with the client IP address as the filename
    if args.save_logs:
      with open(f"{ip_address}.log", "a") as f:
        f.write(data + "\n")


  def get_new_color(self) -> str:
    """ Get a new color for a new client
    """
    color = self.colors[len(self.client_colors) % len(self.colors)]
    return color


if __name__ == '__main__':
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='Simple Syslog Server')
  parser.add_argument('-save-logs', action='store_true', help='Save the log messages to a file')
  args = parser.parse_args()

  os.system('clear')
  try:
    print('Syslog server is listening on default port: 514\n')
    server = socketserver.UDPServer(('0.0.0.0', 514), SyslogHandler)
    server.serve_forever(poll_interval=0.5)
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    # Press Ctrl+C to exit
    print('Shutting down ...')
