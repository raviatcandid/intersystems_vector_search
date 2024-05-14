#!/bin/bash
sleep 40
python3 db_operations.py
exec streamlit run main.py --server.address 0.0.0.0
