import time
import os
import requests
from typing import Dict, Any
import hashlib
import json


def parse_url_args(endpoint, *args, **kwargs):
    md5 = dict_hash({"args": args, **kwargs})
    if args:
        endpoint = endpoint + "/" + "/".join(args)

    if kwargs:
        endpoint = endpoint + "/" + "/".join(
            [f"?{k}={v}" for k, v in kwargs.items()])
    return endpoint, md5


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def get_data_from_endpoint(api_endpoint, name, cache_dir=None, cache_time=3600, **kwargs):
    """
    get the upcoming launches from the space dev api
    """
    # if cache is older than cache_time, update cache

    # get the current time
    now = time.time()

    # get the time of the last update from filename
    # if the file does not exist, create it
    if cache_dir is None:
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache")
    try:
        with open(os.path.join(cache_dir, f"{name}_updated.txt"), "r") as f:
            last_update = f.read()
    except FileNotFoundError:
        last_update = now

    # if the cache is older than cache_time, update cache
    if (now - float(last_update) > cache_time) | (last_update == now):
        # get the data from the api
        r = requests.get(api_endpoint, **kwargs)
        print(r)
        data = r.json()

        # write the data to the cache
        with open(os.path.join(cache_dir, f"{name}_cache.json"), "w") as f:
            json.dump(data, f)

        # update the last update time
        with open(os.path.join(cache_dir, f"{name}_updated.txt"), "w") as f:
            f.write(str(now))

    # read the cache
    with open(os.path.join(cache_dir, f"{name}_cache.json"), "r") as f:
        data = json.load(f)

    # return the data
    return data
