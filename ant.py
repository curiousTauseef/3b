import re
import pymongo

def insertPost(db, blogName, userName, title, postBody, tags, timestamp):
    collection = db.Blogs
    permalink  = blogName+'.'+ re.sub('[^0-9a-zA-Z]+', '_', title)
    present = collection.find_one({"permalink": permalink})
    if not present:
        collection.insert_one({
            "blogName" : blogName,
            "userName" : userName,
            "title" : title,
            "postBody" : postBody,
            "tags" : tags,
            "timestamp": timestamp,
            "permalink" : permalink
        })
        print("Post inserted with permalink: " + permalink)
    else:
        print("Document with permalink: " + permalink + " is already in DB.")

def insertComment(db, blogName, permalink, userName, commentBody, timestamp):
    blogCollection = db.Blogs
    commentCollection = db.Comments
    blogPresent = blogCollection.find_one({"permalink": permalink})
    commentPresent = commentCollection.find_one({"permalink": permalink})
    if blogPresent:
        blogCollection.update_one({
            "permalink": permalink
              },{
            "$push": {
                "comments" : {
                    "permalink" : timestamp,
                    }}})
        commentCollection.insert_one({
            "commentBody" : commentBody,
            "userName" : userName,
            "timestamp": timestamp,
            "permalink": timestamp,
            "blogName": blogName,
            "parent": permalink
        })
        print("Comment inserted with permalink: " + timestamp)
    elif commentPresent:
        commentCollection.update_one({
            "permalink": permalink
              },{
            "$push": {
                "comments" : {
                    "permalink" : timestamp,
                    }}})
        commentCollection.insert_one({
            "commentBody" : commentBody,
            "userName" : userName,
            "timestamp": timestamp,
            "permalink": timestamp,
            "blogName": blogName,
            "parent": permalink
        })
        print("Comment inserted with permalink: " + timestamp)
    else:
        print("No post or comment exists with permalink: " + permalink)

def delete(db, blogName, permalink, userName, timestamp):
    blogCollection = db.Blogs
    commentCollection = db.Comments
    blogPresent = blogCollection.find_one({"permalink": permalink})
    commentPresent = commentCollection.find_one({"permalink": permalink})
    if blogPresent:
        blogCollection.find_one_and_replace({
                "permalink" : permalink
            },{
                "body" : "Deleted by " + userName,
                "timestamp" : timestamp,
                "userName" : userName
                })
        print("Deleted post with permalink: " + permalink)
    elif commentPresent:
        commentCollection.find_one_and_replace({
                "permalink" : permalink
            },{
                "body" : "Deleted by " + userName,
                "timestamp" : timestamp,
                "userName" : userName
                })
        print("Deleted comment with permalink: " + permalink)
    else:
        print("No post in DB with permalink: " + permalink)


def printBlogInfo(blog):
    print("- - - - - - - - - -")
    print("Title: " + blog["title"])
    print("userName: " + blog["userName"])
    print("tags: " + blog["tags"])
    print("timestamp:" + blog["timestamp"])
    print("permalink: " + blog["permalink"])

def printComments(db, entity):



def show(db, blogName):
    print("In " + blogName + ':')
    collection = db.Blogs
    posts = collection.find({"blogName" : blogName})
    for i in posts:
        printBlogInfo(i)
        printComments(db, i)

