from fastapi import APIRouter, HTTPException, status,Request
from fastapi.responses import JSONResponse
from .schemas import AddCardSchema
from colorama import Fore, init
from .vertx import *

router = APIRouter()
init(autoreset=True)


@router.get("/card-data/")
async def get_controller_info(request: Request):
    addr = "192.168.1.199"
    addr = "192.168.1.252"
    # print(request.app.state.connected_controllers)
    controller_information(addr, request.app.state.connected_controllers)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Controller information requested successfully"}
    )

@router.get("/get-connected/")
async def get_connected_controller(request: Request):
    addr = "192.168.1.199"
    addr = "192.168.1.252"
    # print(request.app.state.connected_controllers)
    arr = []
    print(request.app.state.connected_controllers)
    for i in request.app.state.connected_controllers:
        print(Fore.GREEN + f"Connected controller: {i}")
        arr.append(i)
    controller_information(addr, request.app.state.connected_controllers)
    return JSONResponse(
        content={"detail": "successfully","data": arr},
        status_code=status.HTTP_200_OK
    )

@router.post("/add-card/")
async def add_card(request: Request, card_data: AddCardSchema):
    try:
        addr = "192.168.1.252"
        addr = "192.168.1.199"
       
        add_card_record(addr, request.app.state.connected_controllers, CN=card_data.card_number, UID=card_data.unique_id)
        return JSONResponse(
            content={"detail": "successfully","data": f"card {card_data.card_number} added with UID {card_data.unique_id}"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print(Fore.RED + f"Error adding card: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add card: {str(e)}"
        )