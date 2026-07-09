from fastapi import FastAPI

from league_simulator.api.routes import (
    router,
)

app = FastAPI(
    title="League Simulator API",
    version="1.0.0",
)

app.include_router(router)