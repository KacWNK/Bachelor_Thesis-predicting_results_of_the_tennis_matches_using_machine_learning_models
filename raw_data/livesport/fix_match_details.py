import json
with open('match_details_2025.json', 'r') as file:
    match_details = json.load(file)
for match_link in match_details:
    if not match_details[match_link]['match_summary']['player1']['is_winner']:
        if 'sets_score' in match_details[match_link]['match_summary']:
            temp = match_details[match_link]['match_summary']['sets_score']['Wsets']
            match_details[match_link]['match_summary']['sets_score']['Wsets'] = match_details[match_link]['match_summary']['sets_score']['Lsets']
            match_details[match_link]['match_summary']['sets_score']['Lsets'] = temp

with open('match_details_2025.json', 'w') as file:
    json.dump(match_details, file, indent=4)  # Use indent=4 for pretty formatting