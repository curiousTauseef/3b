import re
import pymongo
from pprint import pprint

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

def show(db, blogName):
    blogs = db.Blogs.find({"blogName": blogName})

    if not blogs:
        print("Error: no blog with name " + blogName)
        return

    toVisit = []

    for blog in blogs:
        toVisit.append(["blog", blog["permalink"]])

    while toVisit:
        type, permalink = toVisit.pop()

        if type == "blog":
            blog = db.Blogs.find_one({"permalink": permalink})
            printBlogInfo(blog)
            if ("comments" in blog):
                for comment in blog["comments"]:
                    toVisit.append(["comment", comment["permalink"]])

        else:
            comment = db.Comments.find_one({"permalink": permalink})
            printCommentInfo(comment)
            if ("comments" in comment):
                for childComment in comment["comments"]:
                    toVisit.append(["comment", childComment["permalink"]])



def printBlogInfo(blog):
    print("----------------------------")
    print("title: " + blog["title"])
    print("user: " + blog["userName"])
    print("tags: " + blog["tags"])
    print("timestamp: " + blog["timestamp"])
    print("permalink: " + blog["permalink"])

def printCommentInfo(comment):
    print("\t----------------------------")
    print("\tuser: " + comment["userName"])
    print("\tpermalink: " + comment["permalink"])
    print("\tcomment: " + comment["commentBody"])
