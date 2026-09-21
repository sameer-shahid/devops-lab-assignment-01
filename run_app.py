#!/usr/bin/env python3
"""
Quick runner for CUI DevOps Cloud Web Application
Usage:
    python run_app.py
"""
import os
import sys

# Add app directory to python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app import app

import socket

def find_available_port(preferred_port=5000):
    env_port = os.environ.get("PORT")
    if env_port:
        return int(env_port)
    
    for port in (preferred_port, 5001, 8080, 8000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return 5001

if __name__ == "__main__":
    port = find_available_port(5000)
    print(f"[*] Starting DevOps Cloud Web Application on http://0.0.0.0:{port}")
    print(f"[*] Accessible locally at: http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

