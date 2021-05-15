class MySqlDataAccess:
    def __init__(self, config):
        self._config = config

    def callStoredProcedure(self, storedProcedureName, args, connectionStringName):
        try:
            cnx = mysql.connector.connect(
                user=self._config[connectionStringName]['user_name'],
                password=self._config[connectionStringName]['password'],
                host=self._config[connectionStringName]['host'],
                database=self._config[connectionStringName]['database_name'])
            
            cursor = cnx.cursor()

            resultArgs = cursor.callproc(storedProcedureName, args)

            for element in cursor.stored_results():
                listOfResults = element.fetchall()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        finally:
            cursor.close()
            cnx.close()
        
        return listOfResults

    def saveData(self, storedProcedureName, args, connectionStringName):
        try:
            cnx = mysql.connector.connect(
                user=self._config[connectionStringName]['user_name'],
                password=self._config[connectionStringName]['password'],
                host=self._config[connectionStringName]['host'],
                database=self._config[connectionStringName]['database_name'])
            
            cursor = cnx.cursor()

            cursor.callproc(storedProcedureName, args)
            cnx.commit()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        finally:
            cursor.close()
            cnx.close()
