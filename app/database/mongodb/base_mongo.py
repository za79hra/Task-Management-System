import pymongo
from app.config import Settings


class MongoConnection:
    client = None

    def __init__(self):
        self.client = pymongo.MongoClient(Settings.MONGO_HOST, Settings.MONGO_PORT,
                                          username=Settings.MONGO_USER,
                                          password=Settings.MONGO_PASS
                                          ) if not self.client else self.client

        self.db = self.client['db-task-manager']
        self.users = self.db['tasks']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

# if __name__ == "__main__":
#     try:
#         with MongoConnection() as mongo_conn:

#             print("Connection successful!")
#

#             test_data = {"title": "Test Task", "status": "in-progress"}
#             result = mongo_conn.users.insert_one(test_data)
#             print(f"Document inserted with ID: {result.inserted_id}")
#

#             documents = mongo_conn.users.find()
#             for doc in documents:
#                 print(doc)
#
#     except ServerSelectionTimeoutError as e:
#         print("Failed to connect to MongoDB:", e)
#     except Exception as e:
#         print("An error occurred:", e)
