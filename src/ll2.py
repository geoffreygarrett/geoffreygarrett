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


def get_launches(*args, **kwargs):
    """
    Returns a list of upcoming launches.
    """
    endpoint, md5 = parse_url_args(LL2_ENDPOINTS["launches"], *args, **kwargs)
    return get_data_from_endpoint(endpoint, f"launches_{md5}")


def get_events(*args, **kwargs):
    """
    Returns a list of upcoming events.
    """
    endpoint, md5 = parse_url_args(LL2_ENDPOINTS["events"], *args, **kwargs)
    return get_data_from_endpoint(endpoint, f"events_{md5}")


def get_astronauts(*args, **kwargs):
    """
    Returns a list of astronauts.
    """
    endpoint, md5 = parse_url_args(LL2_ENDPOINTS["astronauts"], *args, **kwargs)
    return get_data_from_endpoint(endpoint, f"astronauts_{md5}")
