import dotenv
from time import sleep

base_path = dotenv.get_key(".env", "BASE_PATH")


def get_path(city: str, suffix: str):
    if suffix == ".json":
        return f"{base_path}/data/crawl/{city}.json"
    elif suffix == ".csv":
        return f"{base_path}/data/crawl/{city}.csv"
    elif suffix == "more":
        return f"{base_path}/data/crawl/{city}_more.json"
    else:
        raise Exception("Error: file suffix is not expected.")


def log_wrap(text: str):
    def outer(func):
        def inner(*args, **kwargs):
            print(f"[Crawl] {text}")
            return func(*args, **kwargs)

        return inner

    return outer


def log(text: str):
    print(f"[Crawl] {text}")


def global_sleep():
    sleep(3)
