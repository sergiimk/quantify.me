import json
import requests

response = requests.get(
    'http://localhost:9200'
    '/location/_search',
    json={
        'aggs': {
            'by_country': {
                'terms': {'field': 'country.keyword'},
            }
        },
        'size': 0,
    })

print(json.dumps(response.json(), indent=2))
