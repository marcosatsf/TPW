import requests
import json
from collections import defaultdict
import locale

park_name = [
    "WaltDisneyWorldMagicKingdom",
    "WaltDisneyWorldEpcot",
    "WaltDisneyWorldHollywoodStudios",
    "WaltDisneyWorldAnimalKingdom",
    "UniversalStudios",
    "UniversalIslandsOfAdventure",
    "UniversalStudiosFlorida"
]

park_metadata_dict = defaultdict(list)

# Get info and structure it from themeparks
for park in park_name:
    park_meta = requests.get(f'https://api.themeparks.wiki/preview/parks/{park}').json()
    entity_data = requests.get(f'https://api.themeparks.wiki/preview/parks/{park}/waittime').json()
    for entity in entity_data:
        temp_meta = {
            "entity_name": entity.get('name'),
            "type": entity.get('meta').get('type'),
            "longitude": entity.get('meta').get('longitude'),
            "latitude": entity.get('meta').get('latitude'),
            "entity_id": entity.get('meta').get('entityId'),
        }
        park_metadata_dict[park].append({**park_meta, **temp_meta})
    print(park, park_metadata_dict[park], sep = ' ---> ')

# save into a json
with open('park_by_entity_meta.json', 'w', encoding='UTF-8') as j:
    for key in park_metadata_dict.keys():
        for entity in park_metadata_dict[key]:
            json.dump(entity, j, ensure_ascii=False)
            j.write('\n')
