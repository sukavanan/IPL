from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import tensorflow as tf

import create_lists
venues = ['Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Jaipur', 'Kolkata', 'Mohali', 'Mumbai', 'Ahmedabad', 'Cuttack', 'Dharamsala', 'Kochi', 'Indore', 'Pune', 'Visakhapatnam', 'Ranchi', 'Raipur', 'Abu Dhabi', 'Brabourne', 'Sharjah', 'Dubai (DSC)', 'Rajkot', 'Kanpur']

app = Flask(__name__, static_folder='static', static_url_path='')

def find_person(given_name, df, col_name='Name'):
    ind = []
    names = list(df[col_name])
    for name in names:
        if given_name.lower() in name.lower():
            ind.append(names.index(name))
    
    if len(ind) > 1:
        for indexxx in ind:
            print(indexxx, df.iloc[[indexxx]][col_name].values[0])
        index = ind[0]
    elif len(ind) == 1:
        index = ind[0]
    else:
        print(f'{given_name} not found')
        return (-1, None)
        
    return (index, df.iloc[[index]].copy())

@app.route('/')
def index_page():
    return render_template('auction.html')

@app.route('/add-data', methods=['POST'])
def add_data():
    data = dict(request.form)
    print(data)
    
    bat = pd.read_csv('bat_2020.csv')
    bowl = pd.read_csv('bowl_2020.csv')
    ground = pd.read_csv('ground.csv')
    match = pd.read_csv('results.csv')

    row = {}
    innings = int(data['innings'])
    target = 0
    if 'playoffs' not in data.keys():
        knockout = 0
    else:
        knockout = 1
    row['knockout'] = knockout
    
    row['overs'] = 20

    if innings == 2:
        target = float(data['runrate'])
    
    else:
        venue = (-1, None)
        while venue[0] == -1:
            venue_name = data['venue']
            venue = find_person(venue_name, ground, 'Venue')
        venue_index = venue[0]
        grnd = venue[1]
        
        target = grnd['Avg_rr'].values[0]

    row['target'] = target
    venue = data['venue']

    total_wickets_lost = 0 
    for i in range(1, 12):
        player = (-1, None)
        while player[0] == -1:
            name = data[f'batsman-{i}-name']
            player = find_person(name,bat)
        target_index = player[0]        
        player = player[1]
        foreign = player['Foreign'].values[0]
        
        if player['Debut'].values[0] == 1:
            avg = player['Form_Score1_Runs'].values[0]
            sr = (player['Form_Score1_Runs'].values[0] / player['Form_Score1_Balls'].values[0])*100
            fs = player['Form_Score'].values[0]
            exp = player['Innings'].values[0]
        
        else:
            if player['Outs'].values[0] != 0:
                avg = player['Avg'].values[0]
                fs = player['Form_Score'].values[0]
                exp = player['Innings'].values[0]
                if player['Balls Faced'].values[0] != 0:
                    sr = player['SR'].values[0]
                else:
                    sr = 0
            else:
                avg = player['Runs Scored'].values[0]
                fs = player['Form_Score'].values[0]
                exp = player['Innings'].values[0]
                if player['Balls Faced'].values[0] != 0:
                    sr = player['SR'].values[0]
                else:
                    sr = 0

        row[f'avg_{i}'] = avg
        row[f'sr_{i}'] = sr
        row[f'form_{i}'] = fs
        row[f'exp_{i}'] = exp
        row[f'foreign_{i}'] = foreign

    balls = 120
    avg = 0
    sr = 0
    eco = 0
    fs = 0
    exp = 0

    pace_balls = 0
    spin_balls = 0
    foreign_bowled = 0

    for j in range(1, int(data['bowlers-used']) + 1):
        player = (-1, None)
        while player[0] == -1:
            name = data[f'bowler-{j}-name']
            player = find_person(name,bowl)
        target_index = player[0]
        player = player[1]
        
        bowled = int(data[f'bowler-{j}-balls'])

        if int(player['Foreign'].values[0]) == 1:
            foreign_bowled += bowled
        
        if player['Bowler_type'].values[0] == 'S':
            spin_balls += bowled
        else:
            pace_balls += bowled
        
        if player['Debut'].values[0] == 1:
            if player['Form_Figure1_Wickets'].values[0] == 0:
                if player['Form_Figure1_Runs'].values[0] <= ((player['Form_Figure1_Runs'].values[0] / player['Form_Figure1_Balls'].values[0]) * 24):
                    avg += ((player['Form_Figure1_Runs'].values[0] / player['Form_Figure1_Balls'].values[0]) * 25) * (bowled / balls)
                else:
                    avg += player['Form_Figure1_Runs'].values[0] * (bowled / balls)
                if player['Form_Figure1_Balls'].values[0] <= 24:
                    sr += 25 * (bowled / balls)
                else:
                    sr += player['Form_Figure1_Balls'].values[0] * (bowled / balls)
            else:
                avg += (player['Form_Figure1_Runs'].values[0] / player['Form_Figure1_Wickets'].values[0]) * (bowled / balls)
                sr += (player['Form_Figure1_Runs'].values[0] / player['Form_Figure1_Balls'].values[0]) * (bowled / balls)
            
            eco += ((player['Form_Figure1_Runs'].values[0] / player['Form_Figure1_Balls'].values[0]) * 6) * (bowled / balls)
            exp += 0
            fs += player['Form_Score'].values[0] * (bowled / balls)  
        
        else:
            if player['Wickets Taken'].values[0] == 0:
                if player['Runs Given'].values[0] <= (player['Eco'].values[0] * 4):
                    avg += (player['Eco'].values[0] * (25 / 24) * 4) * (bowled / balls)
                else:
                    avg += player['Runs Given'].values[0] * (bowled / balls)
                if player['Balls Bowled'].values[0] <= 24:
                    sr += 25 * (bowled / balls)
                else:
                    sr += player['Balls Bowled'].values[0] * (bowled / balls)
            else:
                avg += player['Avg'].values[0] * (bowled / balls)
                sr += player['SR'].values[0] * (bowled / balls)
                
            eco += player['Eco'].values[0] * (bowled / balls)
            exp += player['Innings'].values[0] * (bowled / balls)
            fs += player['Form_Score'].values[0] * (bowled / balls)        

    row['bowl_avg'] = avg
    row['bowl_sr'] = sr
    row['bowl_eco'] = eco
    row['bowl_form'] = fs
    row['bowl_exp'] = exp
    row['pace_balls'] = pace_balls / balls
    row['spin_balls'] = spin_balls / balls
    row['foreign_bowl'] = foreign_bowled / balls
    row['target_score'] = 20 * target

    for ven in venues:
        if venue == ven:
            row[f'venue_{ven}'] = 1
        else:
            row[f'venue_{ven}'] = 0
    
    match = match.append(row, ignore_index=True)
    match.to_csv('auction_match.csv', index=False)
    
    score_model = tf.keras.models.load_model('./models/score.h5')
    wickets_model = tf.keras.models.load_model('./models/wickets.h5')

    x = match.iloc[[-1]].values[0]
    x = x.reshape(1, x.shape[0])
    score = score_model.predict(x)[0][0]
    wickets = wickets_model.predict(x)[0][0]

    score = int(round(score))
    wickets = int(round(wickets))

    # if wickets > 10:
    #     wickets = 10
    
    # if wickets < 0:
    #     wickets = 0

    print('Score:', score)
    print('Wickets:', wickets)

    output_df = pd.read_csv('auction_outputs.csv')
    
    out_row = {}
    out_row['score'] = score
    out_row['wickets_lost'] = wickets

    output_df = output_df.append(out_row, ignore_index=True)
    output_df.to_csv('auction_outputs.csv', index=False)
    
    return render_template('output.html', score=score, wickets=wickets)

@app.route('/output')
def output_page():
    score = 100
    wickets = 10
    return render_template('output.html', score=score, wickets=wickets)

if __name__ == '__main__':
    app.run(debug=True)