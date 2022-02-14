from utils import get_data_from_endpoint, parse_url_args

SFN_ENDPOINTS = {
    "news_articles": "https://api.spaceflightnewsapi.net/v3/articles",
    "blogs": "https://api.spaceflightnewsapi.net/v3/blogs",
    "reports": "https://api.spaceflightnewsapi.net/v3/reports"
}


def get_news_articles(cache_dir=None, cache_time=3600, *args, **kwargs):
    """
    Returns a list of news articles.
    """
    endpoint, md5 = parse_url_args(SFN_ENDPOINTS["news_articles"], *args,
                                   **kwargs)
    return get_data_from_endpoint(endpoint, f"news_articles_{md5}",
                                  cache_dir=cache_dir,
                                  cache_time=cache_time)


def get_blogs(cache_dir=None, cache_time=3600, *args, **kwargs):
    """
    Returns a list of news articles.
    """
    endpoint, md5 = parse_url_args(SFN_ENDPOINTS["blogs"], *args,
                                   **kwargs)
    return get_data_from_endpoint(endpoint, f"blogs_{md5}",
                                  cache_dir=cache_dir,
                                  cache_time=cache_time)


def get_reports(cache_dir=None, cache_time=3600, *args, **kwargs):
    """
    Returns a list of news articles.
    """
    endpoint, md5 = parse_url_args(SFN_ENDPOINTS["news_articles"], *args,
                                   **kwargs)
    return get_data_from_endpoint(endpoint, f"news_articles_{md5}",
                                  cache_dir=cache_dir,
                                  cache_time=cache_time)
