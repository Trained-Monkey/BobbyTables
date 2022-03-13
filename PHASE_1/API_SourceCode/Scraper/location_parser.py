import os
import json
from textwrap import indent

with open(os.path.join(os.path.dirname(__file__), 'countries_states_cities.json'), encoding='utf-8') as f:
            location_data = json.load(f)

json_objects = []

for country_obj in location_data:
    country_name = country_obj['name']
    new_obj = {
        "name": country_name,
        "states": []
    }

    country_states = country_obj['states']
    for state_obj in country_states:
        state_name = state_obj['name']
        state = {
            "name": state_name,
            "cities": []
        }

        country_cities = state_obj['cities']
        for city_obj in country_cities:
            city_name = city_obj['name']
            state['cities'].append(city_name)

        new_obj['states'].append(state)

    json_objects.append(new_obj)

with open ("temp.txt", "w", encoding='utf-8') as output:
    json.dump(json_objects, output, indent = 4, ensure_ascii=False)
