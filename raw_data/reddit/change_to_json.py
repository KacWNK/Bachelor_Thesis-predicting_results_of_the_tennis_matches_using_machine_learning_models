import json
import pandas as pd
with open("tournaments.json", "r") as f:
    tournaments = json.load(f)

tournaments = {key.lower(): value for key, value in tournaments.items()}
with open('tournaments.json', 'w') as outfile:
    outfile.write(json.dumps(tournaments, indent=4))