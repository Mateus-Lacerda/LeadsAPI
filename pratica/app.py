from fastapi import FastAPI
# import uvicorn
from api.routes.leads import router as leads_router
from tests.tests import main as make_tests

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(leads_router)
    return app

app = create_app()

if __name__ == "__main__":
    make_tests()
    app = 'pratica.app:app'
    # uvicorn.run(app, host="localhost", port=8000, reload=True)
