#!/bin/bash

uvicorn setup:app --host ${REST_HOST_PRIVATE} --port ${REST_PORT_PRIVATE}