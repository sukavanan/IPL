import pandas as pd

bat = pd.read_csv('bat_2020.csv')
bowl = pd.read_csv('bowl_2020.csv')
ven = pd.read_csv('ground.csv')

batsmen = str(list(bat['Name'].values))
bowlers = str(list(bowl['Name'].values))
venues = str(list(ven['Venue'].values))

with open('static/lists.js', 'w') as file:
        file.write(f'batsmen = {batsmen}\n')
        file.write(f'bowlers = {bowlers}\n')
        file.write(f'venues = {venues}\n')