#!/usr/bin/env bash
# encoding:utf-8

# The script is used to fire up the ASGI from the project root. It is a
# blocking script
cd src||exit
uv run python3 gateway.py