#!/bin/bash

path="$(readlink -f .)/app/"
echo $path
docker run -it --name demo-python-develop --mount type=bind,source=$path,target=/app demo-python-develop
