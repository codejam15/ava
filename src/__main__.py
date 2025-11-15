from uvicorn import run

from src import create_app
from src.config import settings as s

development = s.FASTAPI_ENV == "development"

app = create_app()

if __name__ == "__main__":
    run("src.__main__:app", host="0.0.0.0", port=s.PORT, reload=development)
