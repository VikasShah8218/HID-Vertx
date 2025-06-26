from fastapi import APIRouter, HTTPException, status,Request
from fastapi.responses import JSONResponse
from colorama import Fore, init
from .vertx import *

router = APIRouter()
init(autoreset=True)


@router.get("/card-data/")
async def list_lpu(request: Request):
    addr = "192.168.1.199"
    # print(request.app.state.connected_controllers)
    controller_information(addr, request.app.state.connected_controllers)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Controller information requested successfully"}
    )