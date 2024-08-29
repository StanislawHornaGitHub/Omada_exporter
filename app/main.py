import os
from fastapi import FastAPI
import src.Router as Router

app = FastAPI()
app.include_router(Router.Prometheus_router)
app.include_router(Router.HealthCheck)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
