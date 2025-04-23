from pymongo.client import MongoClient
from pymongo.server_api import ServerApi

url = ""

client = MongoClient(url, server_api = ServerApi('1'))

db = client.todo_db
collection = db["todo_data"]