from flask import Flask
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

player_list = pd.read_csv("Player_List.csv")

@app.route('/find/<string:ptype>/<string:pname>', methods=['GET'])
def find_player(ptype, pname):
    players = player_list[player_list['Type'] == ptype.lower()]
    players = players[players['Name'].str.lower().str.contains(pname.lower())]

    response = dict()
    index = 0
    for player in players.values:
        response[index] = dict()
        response[index]['Name'] = player[0]
        response[index]['Type'] = player[1]
        response[index]['Foreigner'] = (player[2] == 1)

        index += 1

    return response
