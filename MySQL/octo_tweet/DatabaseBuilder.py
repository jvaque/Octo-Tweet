import os

def addDatabaseDirToList():
    database = "octo_tweet"
    # Probably can be improved to look under the current directory and find the
    #  file with the .sql extension
    
    addToDirListFromName(database)

def addTablesDirToList():
    tables = []
    # Hard coded as it's important that they are executed a specific order
    # Array elements are separated in "visual groups" ordered alphabetically and
    #  separated by an empty line, all the elements in a "visual group" could be
    #  run in any order within that group.

    # Tables with only Primary Keys
    tables.extend([
        "Data_Sources",
        ])

    # Tables with Foreign Keys Not Many-to-Many
    tables.extend([
        "Data_Values",
        "Chart_Tracker",
        ])

    # Tables with Foreign Keys Many-to-Many
    # tables.extend([
    #     ])

    for table in tables:
        addToDirListFromName(table, dirName="Tables")

def addToDirListFromName(fileName, dirName=""):
    if (dirName == ""):
        fullPathSqlFiles.append(f"{dboDir}/{fileName}.sql")
    else:
        fullPathSqlFiles.append(f"{dboDir}/{dirName}/{fileName}.sql")

def addToDirListFromDir(dirName):
    files = os.listdir(f"{dboDir}/{dirName}")

    for file in files:
        fullPathSqlFiles.append(f"{dboDir}/{dirName}/{file}")

def addToDirListFromSubDirs(dirName):
    subDirs = os.listdir(f"{dboDir}/{dirName}/")

    for subDir in subDirs:
        addToDirListFromDir(f"{dirName}/{subDir}")

def createAndSaveSourceCallsToFile():
    sourceCalls = ""
    for sqlPath in fullPathSqlFiles:
        sourceCalls += f"SOURCE {sqlPath}\n"

    with open(f'{dir}/migrations.sql', 'w') as f:
        f.write(sourceCalls)

def terminalOutput():
    print("Run the following sql command:")
    print(f"SOURCE {dir}/migrations.sql")

def main():
    addDatabaseDirToList()
    addTablesDirToList()
    addToDirListFromDir("Views")
    addToDirListFromSubDirs("Stored_Procedures")
    addToDirListFromDir("Users")
    addToDirListFromDir("Permissions")

    createAndSaveSourceCallsToFile()

    terminalOutput()

dir = os.path.abspath(os.path.dirname(__file__))
dboDir = f"{dir}/dbo"
fullPathSqlFiles = []

if __name__ == "__main__":
    main()