from app.vertx.handlers import router as vertx_router
from app.vertx.vertx import event_starter, exit_event
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.database import init_db
from fastapi import FastAPI
import uvicorn



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    try:
        await init_db(app)  # Make this awaitable
        print("✅ Database connection established successfully")
    except Exception as e:
        print(f"❌ Failed to connect to database: {str(e)}")
        raise False
    app.state.connected_controllers = {}
    event_starter(app.state.connected_controllers)
    print("Initiated background task for event server")
    yield

    print("Shutting down...")
    exit_event.set()
    if hasattr(app.state, 'db'):
        await app.state.db.close()
        print("✅ Database connection closed successfully")


app = FastAPI(title="Vertx V1000", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(vertx_router,  prefix="/vertx",  tags=["vertx"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=1)
