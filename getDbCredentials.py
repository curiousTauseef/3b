from configparser import ConfigParser

def getDbCredentials(filename="config.ini", section="mongodb"):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        return parser.items(section)[0][1]

if __name__ == "__main__":
    getDbCredentials()
