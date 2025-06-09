from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

load_dotenv()

def get_kite_client():
    from kiteconnect import KiteConnect
    import os
    print("🔍 API_KEY =", os.getenv("API_KEY"))
    print("🔍 ACCESS_TOKEN =", os.getenv("ACCESS_TOKEN"))

    kite = KiteConnect(api_key=os.getenv("API_KEY"))
    kite.set_access_token(os.getenv("ACCESS_TOKEN"))
    return kite
