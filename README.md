# A STIB-MIVB API client library

Featuring automated OAuth2 token requests.

Does not handle errors elegantly --- use with caution, conform to the STIB-MIVB
API documentation, and respect throttling.

```python
from stib_api import StibClient

api = StibClient(
    client_id=CLIENT_ID,          # Obtained from
    client_secret=CLIENT_SECRET,  # https://opendata.stib-mivb.be/store/subscriptions
)

# Save the GTFS file to disk
api.save_gtfs('/tmp/gtfs.zip')

# Save the ESRI shapefiles to disk
api.save_shapefiles('/tmp/shapefiles.zip')

# Get vehicle position JSON (as officially documented) as a dict
positions = api.get_vehicle_positions(['1', '5'])
```
