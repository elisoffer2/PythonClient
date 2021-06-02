import socketio
import sys
import getopt
import OthelloClass

sio = socketio.Client()
gOpponentName = ''

@sio.event
def connect():
    print("I'm connected!")
    data = {}
    data['name'] = "TeamName"
    sio.emit("set team", data)
    print("Team Name Emitted")

@sio.on('set timeout')
def set_timeout(data):
    moveTimeout = data['timeout']
    print("moveTimeout set to " + str(moveTimeout) + " Seconds")

@sio.on('set opponent')
def set_opponent(data):
    gOpponentName = data["name"]
    gameID = data["game_id"]
    print(data["game_id"])
    print(data["name"])
    print("Game ID set to " + gameID + " with opponent " + gOpponentName);

@sio.on('make move')
def make_move(data):
    gameID = data["game_id"]
    boardStr = data["board"]
    turnStr = data["turn"]
    print(gameID)
    print(boardStr)
    print(turnStr)

    # This is where we need to implement the othello class to know what to do
    data["board"] = "0100002101002021222221112222220121212221212122212201020120011111"
    # end othello class with the next move (can I make a python wrapper?)

    sio.emit("move", data)


@sio.on('game ended')
def game_ended(data):
        gameID = data["game_id"]
        blackCount = data["black_count"]
        white_count = data["white_count"]
        print("Game ended: B-" + str(black_count) + " W-" + str(white_count));

@sio.on('tournament ended')
def tournament_ended(data):
    pname = data["name"]
    game_count = data["game_count"]
    win_count = data["win_count"]
    tie_count = data["tie_count"]
    print("Tournament results for " + pname + " Games: " + str(game_count))
    print(" Wins: " + str(win_count) + " Ties: " + str(tie_count))

@sio.event
def disconnect():
    print('disconnected from server')
    sys.exit()

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
    print("connecting to http://" + serverIP + ":8080")

    sio.connect("http://" + serverIP + ":8080")
    sio.wait()


if __name__ == "__main__":
    main(sys.argv[1:])
    