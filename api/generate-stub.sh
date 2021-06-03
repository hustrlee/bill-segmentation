#!/bin/sh
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli:latest-release generate \
  -i /local/bill-segmentation-api.yaml \
  -g python-flask \
  -o /local/python-flask \
  -c /local/server-config.json
