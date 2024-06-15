import uvicorn
from public_api.settings.settings import settings
from public_api.setup import app

if __name__ == '__main__':
    uvicorn.run(app, host=settings.rest_host_public, port=settings.rest_port_public)
