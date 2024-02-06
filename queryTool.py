import psycopg2
from dotenv import load_dotenv
import os

class queryTool:
    def __init__(self):
        load_dotenv()
            
        # Login details for database user
        host = os.getenv("host")
        dbname = os.getenv("dbname")
        user = os.getenv("user")
        port = os.getenv("port")
        pwd = os.getenv("pwd")

        # Gather all connection info into one string
        connection = \
            "host='" + host + "' " + \
            "user='" + user + "' " + \
            "port='" + port + "' " + \
            "password='" + pwd + "'"
            
        self.conn = psycopg2.connect(connection) # Create a connection
        
        self.table = None
        self.column = None
        self.conditions = {}
        
    def setTable(self, table):
        self.table = table
        
    def setColumn(self, column):
        self.column = column
        
    def setCondition(self, attribute, condition):
        self.conditions[attribute] = condition
        
    def conditionsPresent(self):
        return len(self.conditions) != 0
        
    def getConditions(self):
        queryText = " WHERE "
        for attribute, condition in self.conditions.items():
            if queryText != " WHERE ":
                queryText += " AND "
            
            queryText += attribute + " "
            
            if conditionIsRange(condition):
                queryText += "BETWEEN " + condition[0] + " AND " + condition[1]
            else:
                queryText += condition[0] + " " + condition[1]
        
        return queryText
        
    def conditionIsRange(condition):
        if "<" in condition or ">" in condition:
            return False
        return True

    def query(self):
        cur = self.conn.cursor()
        
        query = "SELECT %s FROM %s" % (self.column, self.table)
                
        if self.conditionsPresent():
            query += self.getConditions()
            
        query += ";"
                
        cur.execute(query)
        
        rows = cur.fetchall() 
        
        return rows