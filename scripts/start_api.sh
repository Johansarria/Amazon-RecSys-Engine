#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/mnt/c/MLpractica4
/home/johan/.local/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
