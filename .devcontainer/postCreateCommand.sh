#!/bin/bash
# uv sync --frozen
uv python pin 3.12.8
uv venv
uv sync
source .venv/bin/activate
