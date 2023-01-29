#!/bin/bash

path="$(readlink -f .)/app/"
docker container rm demo-python-develop 2>/dev/null
docker run -it --name demo-python-develop --mount type=bind,source=$path,target=/app demo-python-develop
