import datetime
import re
import pymongo

# server = "mongodb://Team08:3GfnR9a8WV4gR6lT@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/Team99DB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
# db = None
# try:
#     client = pymongo.MongoClient(server)
#     db = client.Team08DB
#
# except pymongo.errors.ServerSelectionTimeoutError as err:
#     print('failed!')
#     print(err)
#
# records = db.test.find()
# for i in records:
#     print(i)



def insertPost(db, blogName, userName, title, postBody, tags):
    collection = db.Blogs
    permalink  = blogName+'.'+ re.sub('[^0-9a-zA-Z]+', '_', title)
    present = collection.find_one({"permalink": permalink})
    if not present:
        timestamp = datetime.datetime.utcnow()
        collection.insert_one({
                "blogName" : blogName,
                "userName" : userName,
                "title" : title,
                "postBody" : postBody,
                "tags" : tags,
                "timestamp": timestamp,
                "permalink" : permalink
            })
    else:
        print("Document with permalink: " + permalink + " already in DB.")


# insertPost("Time", "potatoMan", "TItleME", "Now this here is a body", [])







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
