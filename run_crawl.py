import os
from fastapi import APIRouter
from src.base.schemas import Crawl
from json import dumps, load

crawl_route = APIRouter(prefix="/llm")


def write_into_map(city_name: str):
    path = "./data/dataset_info.json"
    map_name = city_name

    data: dict = None
    with open(path, "r", encoding="utf-8") as f:
        data = load(f)
        data[map_name] = {"file_name": map_name + ".json"}
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(data, ensure_ascii=False))


@crawl_route.get("/crawl")
async def get_crwl_data():
    file_names = os.listdir("./data")
    json_names = [file for file in file_names if file.endswith('.json')]
    return {"code": 200, "status": "success", "data": {"names": json_names}, "message": "获取路径成功"}

@crawl_route.post("/crawl", tags=["Data", "LLM"])
async def crawl(config: Crawl):
    amount = config.amount
    city = config.city
    if not city or len(city) == 0:
        return {"code": 400, "status": "error", "data": {}, "message": "Error: 采集数量设置错误"}
    if amount > 0 and amount <= 1000:
        base_path = "./src/crawl"
        command = f"python {base_path}/main.py {city} {amount}"
        os.system(command)
    else:
        return {"code": 400, "status": "error", "data": {}, "message": "Error: 采集数量设置错误"}
    write_into_map(city)
    return {
        "code": 200,
        "status": "success",
        "data": {"city": city, "amount": amount},
        "message": "数据采集完毕",
    }
