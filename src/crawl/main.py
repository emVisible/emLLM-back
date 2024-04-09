from crawler import run
import os
import sys

import dotenv

base_path = dotenv.get_key(".env", "BASE_PATH")
data_path = f"{base_path}/data"


def main():
    city = sys.argv[1]
    amount = int(sys.argv[2])
    map_name = sys.argv[3]
    if not os.path.exists(f"{data_path}/{city}.csv"):
        os.system(f"cd {data_path} && touch {map_name}.json {map_name}.csv {map_name}_more.json")
        run(city=city, amount=amount, map_name=map_name)
    else:
        raise Exception("该地区已采集")


if __name__ == "__main__":
    main()