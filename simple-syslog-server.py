""" Simple Syslog Server

  This script will run a simple Syslog Server locally on the machine.
  The Syslog Server listens on port 514 for incoming Syslog messages from different clients.

  By default, the Syslog Server will print the log messages to stdout.

  Usage:
    python3 syslog-server.py [-save-logs] [-p PORT] [-filter IP_ADDRESS]

  Options:
    -save-logs: Save the log messages to a file with the client IP address as the filename
    -p PORT: Use a different port other than the default port 514
    -filter IP_ADDRESS: Filter the output on the screen by IP

  Author:
    Mohamed Abouelwafa
    v1.0: 20231102
    v1.1: 20240306
"""

import os
import socketserver
import argparse
import socket

# Used to assign a different color for each client
colors = ['\033[33m', '\033[36m', '\033[32m', '\033[35m', '\033[34m', '\033[31m', ]
client_colors = {}

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
      if args.save_logs:
        self.print_to_file(ip_address, data)

    elif not filter_ip:
      # If no filter is provided, print all the log messages
      self.print_to_stdout(ip_address, data)
      if args.save_logs:
        self.print_to_file(ip_address, data)


  def print_to_stdout(self, ip_address, data):
    """ Print the log message to stdout
    """
    print("{}{}\033[0m: {}".format(client_colors[ip_address], ip_address, data))


  def print_to_file(self, ip_address, data):
    """ Write the log message to a log file with the client IP address as the filename
    """
    with open(f"{ip_address}.log", "a") as f:
      f.write(data + "\n")


  def get_new_color(self) -> str:
    """ Get a new color for a new client
    """
    color = colors[len(client_colors) % len(colors)]
    return color


if __name__ == '__main__':
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='Simple Syslog Server')
  parser.add_argument('-filter', action='store', help='Filter the output on the screen by IP')
  parser.add_argument('-save-logs', action='store_true', help='Save the log messages to a file')
  parser.add_argument('-p', action='store', type=int,
                      help='Use a different port other than the default port 514')
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
      print("filtering for IP: {}\033[0m".format(client_colors[filter_ip]))
    server = socketserver.UDPServer(('0.0.0.0', port), SyslogHandler)
    server.serve_forever(poll_interval=0.5)

  except (IOError, SystemExit) as e:
    print(str(e))

  except KeyboardInterrupt:
    # Press Ctrl+C to exit
    print('Shutting down ...')
