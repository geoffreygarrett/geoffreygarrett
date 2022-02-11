import jinja2
import time 
import requests
import json
import os 

API_ENDPOINT = "https://ll.thespacedevs.com/2.2.0/launch/upcoming"
CACHE_DIR = "../cache"

# create cache dir if it doesnt exist
os.makedirs(CACHE_DIR, exist_ok=True)

def get_upcoming_launches():
    """
    get the upcoming launches from the space dev api
    """
    # check if launches are cached
    # cache launches by the time
    # if cache is older than 1 hour, update cache

    # get the current time
    now = time.time()

    # get the time of the last update from filename
    # if the file does not exist, create it
    try:
        with open(os.path.join(CACHE_DIR, "last_update.txt"), "r") as f:
            last_update = f.read()
    except FileNotFoundError:
        last_update = now
    
    # if the cache is older than 1 hour, update cache
    if (now - float(last_update) > 3600) | (last_update == now):
        # get the data from the api
        r = requests.get(API_ENDPOINT)
        data = r.json()

        # write the data to the cache
        with open(os.path.join(CACHE_DIR, "launch_cache.json"), "w") as f:
            json.dump(data, f)

        # update the last update time
        with open(os.path.join(CACHE_DIR, "last_update.txt"), "w") as f:
            f.write(str(now))
    
    # read the cache
    with open(os.path.join(CACHE_DIR, "launch_cache.json"), "r") as f:
        data = json.load(f)

    # return the data
    return data
    
# get readme data
def get_readme_data():
    """
    get the readme data for the readme file generation
    """
    # get timestamp and ensure tz is UTC
    timestamp = time.gmtime()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    launches = get_upcoming_launches()["results"]
    next_launch = launches[0]
    launches = launches[1:6]
    return {
        "timestamp": timestamp,
        "launches": launches,
        "next_launch": next_launch,
    }



# load template file
template_loader = jinja2.FileSystemLoader(searchpath="./templates")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("README.md.j2")

if __name__ == "__main__":
    # load data
    data = get_readme_data()

    # render template
    output = template.render(**data)
    print(output)
    # write output
    with open(os.path.join("..", "README.md"), "w") as f:
        f.write(output)
