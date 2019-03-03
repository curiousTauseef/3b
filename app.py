import sys
from connect import connect
from ant import insertPost, insertComment, delete, show, find

def app():
    """
    Main driver for CLI
    """
    db = connect()


    if db:
        print("Welcome to the blog engine CLI")
        print("Please type a valid command to begin!")

    else:
        print("Sorry, connection to database refused")
        return None

    for line in sys.stdin:
        tokens = parseCommand(line.rstrip())

        # POST -----------------------------------------------------------------
        if tokens[0] == "post":
            blogName = None
            userName = None
            title = None
            postBody = None
            tags = None

            if len(tokens) != 6 and len(tokens) != 7:
                print("Usage: post blogName userName title postBody tags timestamp")
                continue

            # type checking
            if isString(tokens[1]):
                blogName = tokens[1]
            else:
                print("Error: blogName must be a string")
                continue

            if isString(tokens[2]):
                userName = "\"" + tokens[2] + "\""
            else:
                print("Error: userName must be a quoted string")
                continue

            if isString(tokens[3]):
                title = "\"" + tokens[3] + "\""
            else:
                print("Error: title must be a quoted string")
                continue

            if isString(tokens[4]):
                postBody = "\"" + tokens[4] + "\""
            else:
                print("Error: postBody must be a quoted string")
                continue

            if len(tokens) == 7 and isString(tokens[5]):
                tags = "\"" + tokens[5] + "\""
            else:
                tags = '""'

            if len(tokens) == 7 and isString(tokens[6]):
                timestamp = tokens[6][1: len(tokens[6]) - 1]
            elif len(tokens) == 6 and isString(tokens[5]):
                timestamp = tokens[5][1: len(tokens[5]) - 1]
            else:
                print("Error: timestamp must be a string")
                break

            insertPost(db, blogName, userName, title, postBody, tags, timestamp)

        # COMMENT --------------------------------------------------------------
        elif tokens[0] == "comment":
            blogName = None
            permalink = None
            userName = None
            commentBody = None
            timestamp = None

            if len(tokens) != 6:
                print("Usage: comment blogName permalink userName commentBody timestamp")
                continue

            # type checking
            if isString(tokens[1]):
                blogName = tokens[1]
            else:
                print("Error: blogName must be a string")
                continue

            if isString(tokens[2]):
                permalink = tokens[2]
            else:
                print("Error: permalink must be a quoted string")
                continue

            if isString(tokens[3]):
                userName = "\"" + tokens[3] + "\""
            else:
                print("Error: userName must be a quoted string")
                continue

            if isString(tokens[4]):
                commentBody = "\"" + tokens[4] + "\""
            else:
                print("Error: commentBody must be a quoted string")
                continue

            if isString(tokens[5]):
                timestamp = tokens[5]
            else:
                print("Error: timestamp must be a string")
                continue

            insertComment(db, blogName, permalink, userName, commentBody, timestamp)


        # DELETE ---------------------------------------------------------------
        elif tokens[0] == "delete":
            blogName = None
            permalink = None
            userName = None
            timestamp = None

            if len(tokens) != 5:
                print("Usage: delete blogName permalink userName timestamp")
                continue

            # type checking
            if isString(tokens[1]):
                blogName = tokens[1]
            else:
                print("Error: blogName must be a string")
                continue

            if isString(tokens[2]):
                permalink = tokens[2]
            else:
                print("Error: permalink must be a quoted string")
                continue

            if isString(tokens[3]):
                userName = tokens[3]
            else:
                print("Error: userName must be a quoted string")
                continue

            if isString(tokens[4]):
                timestamp = tokens[4]
            else:
                print("Error: timestamp must be a string")

            delete(db, blogName, permalink, userName, timestamp)



        # SHOW -----------------------------------------------------------------
        elif tokens[0] == "show":
            blogName = None

            if len(tokens) != 2:
                print("Usage: show blogName")
                continue

            # type checking
            if isString(tokens[1]):
                blogName = tokens[1]
            else:
                print("Error: blogName must be a string")
                continue

            show(db, blogName)

        elif tokens[0] == "find":
            if len(tokens) != 3:
                print("usage: find blogName searchString")
                continue
            if isString(tokens[1]) and isString(tokens[2]):
                blogName = tokens[1]
                searchString = tokens[2]

            find(db, blogName, searchString)

        else:
            print("Possible actions are 'post', 'comment', 'delete', and 'show'.")

def parseCommand(command):
	tokens = []
	currString = ""
	inQuotedString = False
	for char in command:
		if char == "\"":
			if inQuotedString:
				if currString:
					tokens.append(currString)
					currString = ""
			inQuotedString = not inQuotedString
		elif char == " ":
			if inQuotedString:
				currString += char
			else:
				if currString:
					tokens.append(currString)
					currString = ""
		else:
			currString += char

	if currString:
		tokens.append(currString)

	return tokens

def isString(item):
    return isinstance(item, str)

def isQuotedString(item):
    return isinstance(item, str) and item[0] == "\"" and item[-1] == "\""

if __name__ == "__main__":
    app()
