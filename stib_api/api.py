from .session import StibSession


class StibClient:
    endpoints = {
        'token': 'token',
        'operation': 'OperationMonitoring/1.0/VehiclePositionByLine',
        'gtfs': 'Files/2.0/Gtfs',
        'shapefiles': 'Files/2.0/Shapefiles',
    }

    def __init__(self, client_id, client_secret, base=None):
        self.base = base or 'https://opendata-api.stib-mivb.be/'
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = None
        #self._init_session()

    def get_endpoint(self, endpoint):
        return self.base + self.endpoints[endpoint]

    @property
    def session(self):
        if not self._session:
            self._session = self._make_session()
        return self._session

    def _make_session(self):
        session = StibSession(self.base, self.client_id, self.client_secret)
        session.authenticate()
        return session

    def get_vehicle_positions(self, lines):
        url = self.get_endpoint('operation') + '/' + '%2C'.join(lines)
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception(
                'Got response {}  when fetching {}'
                .format(response.status_code, url)
            )
        return response.json()

    def save_shapefiles(self, dest, in_memory=True):
        self._get_to_file(self.get_endpoint('shapefiles'), dest,
                          in_memory=in_memory)

    def save_gtfs(self, dest, in_memory=False):
        self._get_to_file(self.get_endpoint('gtfs'), dest, in_memory=in_memory)

    def _get_to_file(self, url, dest, in_memory=False):
        with self.session.get(url, stream=not in_memory) as response:
            if response.status_code != 200:
                raise Exception(
                    'Got response {} when fetching {}'
                    .format(response.status_code, url)
                )
            with open(dest, 'wb') as fh:
                if in_memory:
                    fh.write(response.content)
                else:
                    # We need a large enough chunk size to have decent speed.
                    for chunk in response.iter_content(chunk_size=4*1024*1024):
                        fh.write(chunk)
