# simple-syslog-server
The Simple Syslog Server script is a lightweight and easy-to-use tool designed to run a Syslog Server locally on a machine. It listens on port 514 for incoming Syslog messages from various clients and provides an option to print log messages to the standard output or save them to individual log files.

## Usage

```python
python3 syslog-server.py [-h] [-save-logs] [-p <port_number>]
```

## Options
### -h
* Show the script help
### -save-logs
* Save the log messages to a file.
* Log messages will be stored in separate log files, named with the client IP address as the filename.
### -p <port_number>
* Use a specific port with the value <port_number>
* Otherwise, the default port 514 will be used
* Type: **integer**
### -filter <IP_Address>
* Filter the output on the screen by IP

Log files will be saved under the same directory where you downloaded the script.

Unfortunately not all the devices report their MAC address with the request. That’s why I made the decision to name the files with the client IP address.

The server will keep appending the new messages to the end of the log files.
This means, the files will keep all the syslog message since it gets created for the first time.

If you need a clean snapshot of the Syslogs, delete the `.log` file(s) before starting the Syslog capture.

## Runtime
When you run the server, you will be prompted with the machine local IP address and the port that the server is listening on


## Stopping the server
```
Ctrl+C
```

## Features
### Real-Time Log Display
The Syslog Server continuously displays real-time log messages from various clients. Logs are color-coded for each client, enhancing readability and enabling easy distinction between different sources.

### Log Saving Option
Using the -save-logs option, log messages can be saved to individual log files, allowing for convenient storage and future analysis. Log files are named based on the client's IP address.

### Graceful Shutdown
The script can be gracefully shut down using the keyboard interrupt (Ctrl+C). The shutdown procedure ensures that all operations are completed and resources are released properly before exiting.
