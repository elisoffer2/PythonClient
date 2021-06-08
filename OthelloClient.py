import socketio
import sys
import getopt
import OthelloClass

sio = socketio.Client()
gOpponentName = ''
gTeamName = ''

def ToArray(in_boardStr):
    OthelloObject = OthelloClass.Board()
    for i in range(0,len(in_boardStr)):
        if in_boardStr[i] == "0":
            OthelloObject.gameBoard[int(i/8)][i%8] = OthelloClass.spaceState.EMPTY
        elif in_boardStr[i] == "1":
            OthelloObject.gameBoard[int(i/8)][i%8] = OthelloClass.spaceState.BLACK
        elif in_boardStr[i] == "2":
            OthelloObject.gameBoard[int(i/8)][i%8] = OthelloClass.spaceState.WHITE
    return OthelloObject.gameBoard

def BoardToString(in_gameBoard):
    strBoard = ""
    for i in range(0,8):
        for j in range(0,8):
            if in_gameBoard[i][j] ==  OthelloClass.spaceState.EMPTY:
                strBoard = strBoard + str(0)
            elif in_gameBoard[i][j] ==  OthelloClass.spaceState.BLACK:
                strBoard = strBoard + str(1)
            elif in_gameBoard[i][j] ==  OthelloClass.spaceState.WHITE:
                strBoard = strBoard + str(2)
    return strBoard

def IsFirstMove(in_gameBoard):
    white_count = 0
    black_count = 0

    for i in range(0,8):
        for j in range(0,8):
            if (in_gameBoard[i][j] == OthelloClass.spaceState.BLACK):
                black_count = black_count + 1
            elif (in_gameBoard[i][j] == OthelloClass.spaceState.WHITE):
                white_count = white_count + 1
    
    if (white_count == 1 and black_count == 4):
        return 1
    else:
        return 0

@sio.on('connect')
def my_connect():
    # print("I'm connected!")
    argv = sys.argv[1:]
    teamName = ''

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
    gTeamName = teamName
    data = {}
    data['name'] = teamName
    sio.emit("set team", data)

@sio.on('set timeout')
def set_timeout(data):
    OthelloClass.moveTimeout = data['timeout']
    print("moveTimeout set to " + str(OthelloClass.moveTimeout) + " Seconds")

@sio.on('set opponent')
def set_opponent(data):
    # print("Set Opponnent Requested")
    gOpponentName = data["name"]
    gameID = data["game_id"]
    # print(data["game_id"])
    # print(data["name"])
    print(gTeamName)
    print(gameID)
    print(gOpponentName)
    output_file = open("GameLogs/" + gTeamName + "_" + gameID + ".txt","w")
    output_file.writelines(gTeamName + " vs. " + gOpponentName + " gameID: " + gameID +"\n")
    output_file.close()
    print("Game ID set to " + gameID + " with opponent " + gOpponentName);

@sio.on('make move')
def make_move(data):
    gameID = data["game_id"]
    boardStr = data["board"]
    turnStr = data["turn"]
    # print(gameID)
    # print(boardStr)
    # print(turnStr)

    # This is where we need to implement the othello class to know what to do
    othelloBoard = OthelloClass.Board()
    othelloBoard.setBoard(ToArray(boardStr))

    turnState = OthelloClass.spaceState.BLACK

    if (turnStr == 2):
        # print("making WHITE")
        turnState = OthelloClass.spaceState.WHITE

    output_file = open("GameLogs/" + gTeamName + "_" + gameID + ".txt","a")
    if (turnState == OthelloClass.spaceState.WHITE and IsFirstMove(ToArray(boardStr))):
        output_file.writelines("1:0000000000000000000000000001200000021000000000000000000000000000:their turn\n")
    output_file.writelines(str(turnStr) + ":" + boardStr + ":my turn\n")
    output_file.close()


    if (othelloBoard.turn != turnState):
        othelloBoard.switchTurn()
    
    # print("Current Turn: " + str(turnStr))
    # print(othelloBoard.turn)
    totalMoveCount = 0
    moveSelection = 0

    availableMoves = [[]]
    objectBoard = [[]]

    availableMoves = othelloBoard.legalMoves(othelloBoard.gameBoard, othelloBoard.turn)
    totalMoveCount = othelloBoard.moveCount(availableMoves)

    # print("Total Move Count: " + str(totalMoveCount) + " for player: " + str(turnStr))

    if (totalMoveCount != 0):
        moveSelection = othelloBoard.moveSelect(totalMoveCount)

        objectBoard = availableMoves[moveSelection-1]
        othelloBoard.setBoard(objectBoard)

        out_board = othelloBoard.gameBoard

        out_boardStr = BoardToString(out_board)

        data["board"] = out_boardStr
        data["game_id"] = gameID

        # print(gameID)
        # print(out_boardStr)
        # print(turnStr)

        output_file = open("GameLogs/" + gTeamName + "_" + gameID + ".txt","a")
        output_file.writelines(str(turnStr % 2 + 1) + ":" + out_boardStr + ":their turn\n")
        output_file.close()
        sio.emit("move", data)

    else:
        output_file = open("GameLogs/" + gTeamName + "_" + gameID + ".txt","a")
        output_file.writelines(str(turnStr % 2 + 1) + ":" + boardStr + ":their turn - I pass\n")
        output_file.close()
        sio.emit("pass", data)



@sio.on('game ended')
def game_ended(data):
        gameID = data["game_id"]
        black_count = data["black_count"]
        white_count = data["white_count"]
        print("Game " + gameID + "ended: ")
        print("Results: Black-" + str(black_count) + " White-" + str(white_count))

@sio.on('tournament ended')
def tournament_ended(data):
    pname = data["name"]
    game_count = data["game_count"]
    win_count = data["win_count"]
    tie_count = data["tie_count"]
    print("Tournament results for " + pname + " Games: " + str(game_count))
    print("Wins: " + str(win_count) + " Losses: " +
          str(game_count - win_count - tie_count) + " Ties: " + str(tie_count))
          
    sio.disconnect()

@sio.event
def disconnect():
    print("Disconnecting from the server")

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
            sys.exit(0)
        elif opt in ("-n", "--name"):
            teamName = arg
            gTeamName = teamName
        elif opt in ("-i", "--ipaddr"):
            serverIP = arg
    arguementCount = len(sys.argv)
    arguementStrings = str(sys.argv)
    data = {}
    data['name'] = teamName
    print("connecting to http://" + serverIP + ":8080")

    sio.connect("http://" + serverIP + ":8080")
    sio.wait()
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
    