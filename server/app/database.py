'''
db connection string
'''
from pymongo import MongoClient

# CONN_STRING = "mongodb://calorie-user:calorie123@localhost:27020/?authMechanism=DEFAULT&authSource=calorie-tracker-db"
CONN_STRING = (
    "mongodb://calorie-user:calorie123@mongodb:27017/?authSource=calorie-tracker-db"
)
client = MongoClient(CONN_STRING)

db = client["calorie-tracker-db"]
