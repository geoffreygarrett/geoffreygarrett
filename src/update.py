import jinja2
import time
import requests
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

API_ENDPOINT = "https://ll.thespacedevs.com/2.2.0/launch/upcoming"
BASE_TIME_URL = "https://www.timeanddate.com/worldclock/fixedtime.html?iso={iso}"
CACHE_DIR = "../cache"
ISO3_JSON = "http://country.io/iso3.json"
BASE_GOOGLE_CALENDAR_URL = "https://www.google.com/calendar/render?action=TEMPLATE&text={text}&location={location}&dates={date1}%2F{date2}"

STATUS_MAP = {
    "Go": "🟩 ",
    "TBC": "🟨 ",
    "TBD": "🟧 "
}

# create cache dir if it doesnt exist
os.makedirs(CACHE_DIR, exist_ok=True)


def first_letter_lower(s):
    return s[0].lower() + s[1:]


def status_emoji(status):
    return STATUS_MAP[status]

import html

def make_google_calender_url(launch):
    return BASE_GOOGLE_CALENDAR_URL.format(
        text=html.escape(launch["name"]),
        location=html.escape(launch["pad"]["location"]["name"]),
        date1=time.strftime("%Y%m%dT%H%M%SZ", time.strptime(launch["window_start"],
                                           "%Y-%m-%dT%H:%M:%SZ")),
        date2=time.strftime("%Y%m%dT%H%M%SZ", time.strptime(launch["window_end"],
                                           "%Y-%m-%dT%H:%M:%SZ")),
    )


def make_google_calender_href_icon(launch):
    """
    create a google calendar href icon
    """
    return f'<a href="{make_google_calender_url(launch)}"><img border="0" width="15" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Google_Calendar_icon_%282020%29.svg"></a>'


def make_time_and_date_link(timestamp):
    """
    create a link to a time and date
    """
    # convert the timestamp to a string in iso format
    iso = time.strftime("%Y%m%dT%H%M%S", timestamp)
    return BASE_TIME_URL.format(iso=iso)


def get_iso3_to_iso2_country_map():
    """
    get a map from iso3 to iso2
    """
    # get the json
    r = requests.get(ISO3_JSON)
    data = r.json()

    # create a map from iso3 to iso2
    iso3_to_iso2 = {}
    for k, v in data.items():
        iso3_to_iso2[v] = k

    return iso3_to_iso2


ISO3_2_ISO2 = get_iso3_to_iso2_country_map()


def make_datetime_human_readable(timestamp):
    """
    make a timestamp human readable
    """
    # get the timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", timestamp)
    # timestamp = time.strftime("%B %d, %Y UTC", timestamp)
    return timestamp


def make_markdown_linked_time(timestamp):
    """
    create a link to a time and date
    """
    # convert the timestamp to a string in iso format
    s = make_datetime_human_readable(timestamp)
    url = make_time_and_date_link(timestamp)
    return f"[{s}]({url})"


def make_html_linked_time(timestamp):
    """
    create a link to a time and date
    """
    # convert the timestamp to a string in iso format
    s = make_datetime_human_readable(timestamp)
    url = make_time_and_date_link(timestamp)
    return f'<a href="{url}">{s}</a>'


def get_upcoming_launches(cache_time=3600):
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
    if (now - float(last_update) > cache_time) | (last_update == now):
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


def generate_next_launch(data):
    """
    generate the next launch readme
    """
    # get the template

    # render the template
    description = """
    
    """


def add_a_an(s):
    if s[0] in "aeiouAEIOU":
        return "an " + s
    else:
        return "a " + s


def parse_launch_windows_to_datetime(launches):
    for launch in launches:
        # get datetime from window_start string
        launch["datetime"] = time.strptime(launch["window_start"],
                                           "%Y-%m-%dT%H:%M:%SZ")
    return launches


def get_country_flag_svg(iso3_country_code):
    # convert iso3 to iso2
    iso2_country_code = ISO3_2_ISO2[iso3_country_code]
    return f'https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{iso2_country_code.lower()}.svg'


def parse_launches_within_a_month(launches):
    upcoming_launches = []
    t_now = time.mktime(time.localtime())
    for i, launch in enumerate(launches):
        t_launch = time.mktime(launch["datetime"])
        if (t_launch > t_now) & (t_launch < t_now + 2592000):
            upcoming_launches.append(launch)
    return upcoming_launches


def plot_launch_histogram_within_a_year(launches):
    # get the launches within a year
    launches_within_a_year = []
    t_now = time.mktime(time.localtime())
    for launch in launches:
        t_launch = time.mktime(launch["datetime"])
        if (t_launch > t_now) & (t_launch < t_now + 2592000):
            launches_within_a_year.append(launch)

    times = [time.mktime(launch["datetime"]) for launch in
             launches_within_a_year]
    # convert times array to epochs

    mpl_data = mdates.date2num(times)

    # plot the histogram
    fig, ax = plt.subplots()
    # print(launches_within_a_year)
    ax.hist(mpl_data,
            bins=30,
            # range=(t_now, t_now + 2592000),
            )
    ax.set_xlabel("Launch date")
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    # save figure
    fig.savefig("launch_histogram.png")


# get readme data
def get_readme_data():
    """
    get the readme data for the readme file generation
    """
    # get timestamp and ensure tz is UTC
    # timestamp = time.gmtime()
    # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    launches = get_upcoming_launches()["results"]
    launches = parse_launch_windows_to_datetime(launches)
    next_launch = launches[0]
    return {
        "timestamp": time.gmtime(),
        "launches": launches,
        "next_launch": next_launch,
        "make_html_linked_time": make_html_linked_time,
        "parse_launches_within_a_month": parse_launches_within_a_month,
        "get_country_flag_svg": get_country_flag_svg,
        "get_iso3_to_iso2_country_map": get_iso3_to_iso2_country_map,
        "status_emoji": status_emoji,
        "first_letter_lower": first_letter_lower,
        "add_a_an": add_a_an,
        "make_google_calender_href_icon": make_google_calender_href_icon
    }


# load template file
template_loader = jinja2.FileSystemLoader(searchpath="./templates")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("README.md.j2")

if __name__ == "__main__":
    # # load data
    data = get_readme_data()

    # render template
    output = template.render(**data)

    # write output
    with open(os.path.join("..", "README.md"), "w") as f:
        f.write(output)
