import uvicorn
from private_api.settings.settings import settings
from private_api.setup import app

if __name__ == '__main__':
    uvicorn.run(app, host=settings.rest_host_private, port=settings.rest_port_private)
