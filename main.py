from src.base.database import engine
from src.base.middleware import CORSMiddleware, origins
from src.base.models import Base
from src.base.controller import route
from run_finetune import finetune_route
from run_crawl import crawl_route
from run_export_model import export_route
from run_deploy import deploy_route
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from dotenv import dotenv_values
from contextlib import asynccontextmanager
from src.api.api_server import llm_route, run_llm
import torch


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swaqqer-ui/5.6.2/swagqer-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.6.2/swagger-ui.min.css"
    )


# 初始化数据库
Base.metadata.create_all(bind=engine)
# 初始化app实例
app = FastAPI(title="ZISU-LLM", version="1.0.0", lifespan=lifespan)
# 导入路由
app.include_router(route)
app.include_router(llm_route, prefix="/api")
app.include_router(finetune_route, prefix="/api")
app.include_router(crawl_route, prefix="/api")
app.include_router(export_route, prefix="/api")
app.include_router(deploy_route, prefix="/api")
# 跨域中间件
app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/api")
def root_page():
    return {"ZISU-LLM": "Hello World!"}


def run():
    """
    通过python main.py, 根据env设置的MODE运行在指定PORT上, 默认为DEVELOPMENT的3000端口
    """
    mode = dotenv_values(".env").get("MODE")
    if mode == "DEVELOPMENT":
        import uvicorn

        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=int(dotenv_values(".env").get("PORT")),
            reload=True,
        )

    elif mode == "PRODUCTION":
        import uvicorn

        uvicorn.run(
            "main:app", host="0.0.0.0", port=int(dotenv_values(".env").get("PORT"))
        )
    else:
        raise RuntimeError("Please check the .env file.")


if __name__ == "__main__":
    run()
