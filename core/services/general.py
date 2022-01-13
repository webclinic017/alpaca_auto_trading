import base64
import os

def generate_id(digit):
    r_id = base64.b64encode(os.urandom(digit)).decode("ascii")
    r_id = r_id.replace(
        "/", "").replace("_", "").replace("+", "").replace("=", "").strip()
    return r_id