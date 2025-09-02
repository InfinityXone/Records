#!/opt/infinity_x_one/venv/bin/python3
import os
from supabase import create_client
def get_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    return create_client(url, key)
