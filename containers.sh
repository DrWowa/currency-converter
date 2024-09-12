#!/usr/bin/env sh

podman build -t rex .

podman run \
  --detach \
  --rm \
  --publish 6000:6379 \
  --name rex-redis \
  redis

podman run \
  --detach \
  --rm \
  --publish 8000:8080 \
  --name rex-main \
  rex
