#!/usr/bin/python3
""" Simple Syslog Server

  This script will run a simple Syslog Server locally on the machine.
  The Syslog Server listens on port 514, by default, for incoming Syslog messages from different clients.

  By default, the Syslog Server will print the log messages to stdout.

  Usage:
    python3 syslog-server.py [-save-logs] [-p PORT] [-filter IP_ADDRESS]

  Options:
    -save-logs: Save the log messages to a file with the client IP address as the filename
    -p PORT: Use a different port other than the default port 514
    -filter IP_ADDRESS: Filter the output on the screen by IP
    -backup-count: The number of backup log files to keep (default is 20)

  Author:
    Mohamed Abouelwafa

  Version history:
    v1.0: 20231102
    v1.1: 20240306
    v2.0: 20240426  Use logging module to save logs to files with rotating file handler
"""


import os
import socketserver
import argparse
import socket
import logging
from logging.handlers import RotatingFileHandler

# Used to assign a different color for each client
colors = ['\033[33m', '\033[36m', '\033[32m', '\033[35m', '\033[34m', '\033[31m', ]
client_colors = {}
client_loggers = {}

class SyslogHandler(socketserver.BaseRequestHandler):

  def handle(self):
    """ Handle incoming messages
    """
    data = bytes.decode(self.request[0].strip())
    ip_address = self.client_address[0]
    if ip_address not in client_colors:
      client_colors[ip_address] = self.get_new_color()

    # Print the log message to stdout
    if filter_ip and filter_ip == ip_address:
      # Only print the log message if the IP address matches the filter
      self.print_to_stdout(ip_address, data)

    elif not filter_ip:
      # If no filter is provided, print all the log messages
      self.print_to_stdout(ip_address, data)

    if args.save_logs:
      backup_count = args.backup_count if args.backup_count else 20
      self.setup_logger(ip_address, backup_count)
      client_loggers[ip_address].info(data)


  def print_to_stdout(self, ip_address, data):
    """ Print the log message to stdout
    """
    print("{}{}\033[0m: {}".format(client_colors[ip_address], ip_address, data))


  def setup_logger(self, ip_address, backup_count=20):
    """ Setup a logger for each client IP address
    """
    if ip_address not in client_loggers:
      logger = logging.getLogger(ip_address)
      logger.setLevel(logging.INFO)
      handler = RotatingFileHandler(f"{ip_address}.log", maxBytes=10 * 1024 * 1024, backupCount=backup_count)
      logger.addHandler(handler)
      client_loggers[ip_address] = logger


  def get_new_color(self) -> str:
    """ Get a new color for a new client
    """
    color = colors[len(client_colors) % len(colors)]
    return color


if __name__ == '__main__':
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='Simple Syslog Server')
  parser.add_argument('-p', action='store', type=int,
                      help='Use a different port other than the default port 514')
  parser.add_argument('-filter', action='store', help='Filter the output on the screen by IP')
  parser.add_argument('-save-logs', action='store_true', help='Save the log messages to a file')
  parser.add_argument('-backup-count', action='store', help='The number of backup files to keep')
  args = parser.parse_args()

  # Default port
  port = args.p if args.p else 514
  # Local IP address
  local_ip = ''
  # Filter IP
  filter_ip = args.filter

  os.system('clear')
  # Get the machine local IP address
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # connecting to a remote address
    local_ip = s.getsockname()[0]
    s.close()
  except Exception as e:
    pass

  try:
    print('Syslog server: {} listening on port: {}\n'.format(local_ip, port))
    if filter_ip:
      print("filtering for IP: {}\n".format(filter_ip))
    server = socketserver.UDPServer(('0.0.0.0', port), SyslogHandler)
    server.serve_forever(poll_interval=0.5)

  except (IOError, SystemExit) as e:
    print(str(e))

  except KeyboardInterrupt:
    # Press Ctrl+C to exit
    print('Shutting down ...')
