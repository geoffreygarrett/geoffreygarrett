from utils import get_data_from_endpoint, parse_url_args

LL2_ENDPOINTS = {
    "launches": "https://ll.thespacedevs.com/2.2.0/launch/",
    "events": "https://ll.thespacedevs.com/2.2.0/event/",
    "astronauts": "https://ll.thespacedevs.com/2.2.0/astronaut/",
    "space_stations": "https://ll.thespacedevs.com/2.2.0/spacestation/",
    "expeditions": "https://ll.thespacedevs.com/2.2.0/expedition/",
    "dockings": "https://ll.thespacedevs.com/2.2.0/docking_event/",
    "launche_vehicles": "https://ll.thespacedevs.com/2.2.0/launcher/",
}


class LaunchLibrary2:
    LAUNCHES = "https://ll.thespacedevs.com/2.2.0/launch"
    EVENTS = "https://ll.thespacedevs.com/2.2.0/event"
    ASTRONAUTS = "https://ll.thespacedevs.com/2.2.0/astronaut"
    SPACE_STATIONS = "https://ll.thespacedevs.com/2.2.0/spacestation"
    EXPEDITIONS = "https://ll.thespacedevs.com/2.2.0/expedition"
    DOCKINGS = "https://ll.thespacedevs.com/2.2.0/docking_event"
    LAUNCH_VEHICLES = "https://ll.thespacedevs.com/2.2.0/launcher"

    def __init__(self, **kwargs):
        pass

    def get_launches(self, *args, **kwargs):
        """
        Returns a list of upcoming launches.
        """
        cache_dir = kwargs.pop("cache_dir", None)
        cache_time = kwargs.pop("cache_time", 3600 // 2)
        endpoint, md5 = parse_url_args(self.LAUNCHES, *args, **kwargs)
        return get_data_from_endpoint(endpoint, f"launches_{md5}",
                                      cache_dir=cache_dir,
                                      cache_time=cache_time)

    def get_events(self, *args, **kwargs):
        """
        Returns a list of upcoming events.
        """
        cache_dir = kwargs.pop("cache_dir", None)
        cache_time = kwargs.pop("cache_time", 3600 // 2)
        endpoint, md5 = parse_url_args(self.EVENTS, *args, **kwargs)
        return get_data_from_endpoint(endpoint, f"events_{md5}",
                                      cache_dir=cache_dir,
                                      cache_time=cache_time)

    def get_astronauts(self, *args, **kwargs):
        """
        Returns a list of astronauts.
        """
        cache_dir = kwargs.pop("cache_dir", None)
        cache_time = kwargs.pop("cache_time", 3600 // 2)
        endpoint, md5 = parse_url_args(self.ASTRONAUTS, *args, **kwargs)
        return get_data_from_endpoint(endpoint, f"astronauts_{md5}",
                                      cache_dir=cache_dir,
                                      cache_time=cache_time)
