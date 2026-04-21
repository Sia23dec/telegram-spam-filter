#!/bin/bash
python -m bot.main &
streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0
