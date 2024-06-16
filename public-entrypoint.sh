#!/bin/bash

uvicorn setup:app --host ${REST_HOST_PUBLIC} --port ${REST_PORT_PUBLIC}