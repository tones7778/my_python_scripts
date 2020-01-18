import paho.mqtt.client as mqtt
import time
import argparse
# options to send one time message to the broker.
# options to read from a csv file and send line items ever 1 sec.

parser = argparse.ArgumentParser(description="Send a message to the HA mqtt broker. Select i and m to send a onetime message.")
parser.version = '1.0'
parser.add_argument('-f', action='store', help='-f myloggile.log to send each line of a log file to the broker.')
parser.add_argument('-m', action='store', help='-m "this is a message" to send a one time message to the broker.')

args = parser.parse_args()


def send_log_lines(log_file):
    #log_file_path = 'cidcall.log'
    with open(log_file, "r") as file:
        for line in file:
            print(line)
            send_message(line)
            time.sleep(1.5)

def send_message(message):
    broker = '192.168.2.8'
    port = 1883
    timeout = 60
    topic = 'hello/world'
    client = mqtt.Client()
    client.connect(broker, port, timeout)
    client.publish(topic, message)
    client.disconnect()

def print_something():
    print("this is the function print something.")


if __name__ == '__main__':
    if args.m:
        print('Sending a onetime message .....')
        print(args.m)
        send_message(args.m)
    elif args.f:
        print('sending bulk message.....')
        send_log_lines(args.f)
    else:
        print('Nothing to send.')
