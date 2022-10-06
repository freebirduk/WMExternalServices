import abc


class IWeatherUndergroundApiService(abc.ABC):
    @abc.abstractmethod
    def get_hourly_observations_for_date(self, date):
        pass

    @abc.abstractmethod
    def start_wu_api_session(self):
        pass

    @abc.abstractmethod
    def stop_wu_api_session(self):
        pass
