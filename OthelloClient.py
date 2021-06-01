import socketio
import sys
import getopt

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')


def main(argv):
    teamName = ''
    serverIP = ''

    try:
        opts, args = getopt.getopt(argv,"hn:i:",["teamName=","serverIP="])
    except getopt.GetoptError:
        print("python OthelloClient.py -n <Team Name> -i <Server IP Address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("python OthelloClient.py -n <Team Name> -i <Server IP Address>")
            sys.exit()
        elif opt in ("-n", "--name"):
            teamName = arg
        elif opt in ("-i", "--ipaddr"):
            serverIP = arg
    print("Team Name is", teamName)
    print("IP Address is", serverIP)
    arguementCount = len(sys.argv)
    arguementStrings = str(sys.argv)
    print("http://" + serverIP + ":8080")

    sio.connect("http://" + serverIP + ":8080")
    sio.wait()


if __name__ == "__main__":
    main(sys.argv[1:])
    