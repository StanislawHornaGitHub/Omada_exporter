import uvicorn
from fastapi import FastAPI
import src.Router as Router
from src.Observability import *

app = FastAPI()
app.include_router(Router.Prometheus_router)
app.include_router(Router.HealthCheck)

opentelemetry_instrument(app)
prometheus_instrument(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
