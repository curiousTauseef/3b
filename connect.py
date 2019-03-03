import pymongo
from getDbCredentials import getDbCredentials

def connect():
    server = getDbCredentials()
    db = None
    try:
        client = pymongo.MongoClient(server)
        db = client.Team08DB
        return db

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print('failed!')
        print(err)
        return False

    # records = db.test.find()
    # for i in records:
    #     print(i)


if __name__ == "__main__":
    connect()




'''
if db:
    try:
        post = {
            "author": "Ben"
        }
        post_id = db.test.insert_one(post).inserted_id
        print("post_id 1: {}".format(post_id))
    except Exception as e:
        print(e)
else:
    print('no db')

'''
