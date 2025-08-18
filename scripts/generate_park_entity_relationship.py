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

names = []
with open('park_by_entity_meta.json', 'r', encoding='UTF-8') as j:
    for js in j.readlines():
        names.append(json.loads(js).get('entity_name'))
print(names)

# Get info and structure it from themeparks
for park in park_name:
    park_meta = requests.get(f'https://api.themeparks.wiki/preview/parks/{park}').json()
    entity_data = requests.get(f'https://api.themeparks.wiki/preview/parks/{park}/waittime').json()
    for entity in entity_data:
        if not entity.get('name') in names:
            continue
        print(entity)
        detail = requests.post('https://places.googleapis.com/v1/places:searchText',
                          json={"textQuery": f"{entity.get('name')}, {park_meta.get('name')}, US"},
                          headers={"Content-Type": "application/json",
                                   "X-Goog-Api-Key": 'API_KEY',
                                   "X-Goog-FieldMask": "places.displayName,places.rating"}).json()
        print(detail)
        try:
            rating = detail.get('places')[0]['rating']
        except Exception:
            rating = -1
        temp_meta = {
            "entity_name": entity.get('name'),
            "type": entity.get('meta').get('type'),
            "longitude": entity.get('meta').get('longitude'),
            "latitude": entity.get('meta').get('latitude'),
            "entity_id": entity.get('meta').get('entityId'),
            "rating":rating,
        }
        park_metadata_dict[park].append({**park_meta, **temp_meta})
    print(park, park_metadata_dict[park], sep = ' ---> ')

# save into a json
with open('park_by_entity_meta_new.json', 'w', encoding='UTF-8') as j:
    for key in park_metadata_dict.keys():
        for entity in park_metadata_dict[key]:
            json.dump(entity, j, ensure_ascii=False)
            j.write('\n')
