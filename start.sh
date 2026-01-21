#!/bin/bash

echo "Activating Python virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Kali MCP Server..."
python src/mcp_server.py
