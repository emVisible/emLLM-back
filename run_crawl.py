import os
from fastapi import APIRouter
from src.base.schemas import Crawl

crawl_route = APIRouter(prefix="/llm")


@crawl_route.post("/crawl", tags=["Data", "LLM"])
async def crawl(config: Crawl):
    amount = config.amount
    city = config.city
    if not city or len(city) == 0:
        raise Exception("缺失城市参数")
    if amount > 0 and amount < 500:
        base_path = "./src/crawl"
        command = f"python {base_path}/main.py {city} {amount}"
        os.system(command)
    else:
        raise Exception("单次采集数量范围为1-500条")