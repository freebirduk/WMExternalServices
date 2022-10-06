import requests
from datetime import date
from src.WMExternalServices.IWeatherUndergroundApiService import IWeatherUndergroundApiService
from requests.adapters import HTTPAdapter, Retry
from WuApiException import WuApiException


# Service to handle retrieval of observations from the Weather Underground API.
class WeatherUndergroundApiService(IWeatherUndergroundApiService):
    _api_key = ""
    _api_session = None
    _station_id = ""
    _weather_underground_url = "https://api.weather.com/v2/pws/history/"

    def __init__(self, station_id, api_key):
        self.__validate_constructor_parameters(station_id, api_key)

        self._api_key = api_key
        self._station_id = station_id

    # Retrieves a full set of observations for a specific date.
    def get_hourly_observations_for_date(self, date_required: date):

        # Configure the api call
        _api_url = "{}hourly?stationId={}&format=json&units=m&numericPrecision=decimal&date={}&apiKey={}" \
            .format(self._weather_underground_url,
                    self._station_id,
                    date_required.strftime("%Y%m%d"),
                    self._api_key)

        # Make the api call and check response
        _api_response = self._api_session.get(_api_url)

        match _api_response.status_code:
            case requests.codes.ok:
                return _api_response.json()
            case 204:  # No content
                return None
            case _:
                raise WuApiException("Weather Underground API returned {} '{}'".format(_api_response.status_code,
                                                                                       _api_response.reason))

    # Prepares the Weather Underground API for querying
    def start_wu_api_session(self):

        self._api_session = requests.session()
        _retry_data = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        self._api_session.mount("https://", HTTPAdapter(max_retries=_retry_data))

    # Closes the Weather Underground API session
    def stop_wu_api_session(self):

        self._api_session.close()

    @staticmethod
    def __validate_constructor_parameters(station_id, api_key):
        if not station_id and not station_id.isspace():
            raise WuApiException("Station Id not provided to Weather Underground API service")

        if not api_key or api_key.isspace():
            raise WuApiException("API Key not provided to Weather Underground API service")
