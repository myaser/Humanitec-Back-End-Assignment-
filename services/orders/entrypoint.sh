#!/usr/bin/env bash

cmd="$@"
export JWT_SECRET_KEY=$(cat /keys/jwtHS256.key)
export JWT_PUBLIC_KEY=$(cat /keys/jwtRS256.key.pub)
export JWT_PRIVATE_KEY=$(cat /keys/jwtRS256.key)
exec $cmd