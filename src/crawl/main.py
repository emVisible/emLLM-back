from crawler import run
import os
import sys

import dotenv

base_path = dotenv.get_key(".env", "BASE_PATH")
data_path = f"{base_path}/data"


def main():
    city = sys.argv[1]
    amount = int(sys.argv[2])
    if not os.path.exists(f"{data_path}/{city}.csv"):
        os.system(f"cd {data_path} && touch {city}.json {city}.csv {city}_more.json")
        run(city=city, amount=amount)
    else:
        raise Exception("该地区已采集")


if __name__ == "__main__":
    main()