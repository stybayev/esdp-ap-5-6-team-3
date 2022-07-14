import os
import environ
from dotenv import load_dotenv

load_dotenv()
env = environ.Env()
environ.Env.read_env()


merchant_key = os.getenv('MERCHANT_KEY')
client_key = os.getenv('CLIENT_KEY')
print(merchant_key)
print(client_key)