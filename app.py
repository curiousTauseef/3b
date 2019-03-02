import sys
from connect import connect
from ant import insertPost

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
        tokens = parseCommand(line)
        print(tokens)

        # POST -----------------------------------------------------------------
        if tokens[0] == "post":
            print("posting!")
            blogName = None
            userName = None
            title = None
            postBody = None
            tags = None

            # type checking
            if isString(tokens[1]):
                blogName = tokens[1]
            else:
                print("Error: blogName must be a string")
                break
            if isString(tokens[2]):
                userName = "\"" + tokens[2] + "\""
            else:
                print("Error: userName must be a quoted string")
                break
            if isString(tokens[3]):
                title = "\"" + tokens[3] + "\""
            else:
                print("Error: title must be a quoted string")
                break
            if isString(tokens[4]):
                postBody = "\"" + tokens[4] + "\""
            else:
                print("Error: postBody must be a quoted string")
                break
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

            insertPost(db, blogName, userName, title, postBody, tags)

        # COMMENT --------------------------------------------------------------
        elif tokens[0] == "comment":
            print("commenting!")

        # DELETE ---------------------------------------------------------------
        elif tokens[0] == "delete":
            print("deleting!")

        # SHOW -----------------------------------------------------------------
        elif tokens[0] == "show":
            print("showing!")

        else:
            print("Possible actions are 'post', 'comment', 'delete', and 'show'.")

def parseCommand(command):
	tokens = []
	currString = ""
	inQuotedString = False
	print(command)
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
