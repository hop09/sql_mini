import sqlite3
class Database():
    def __init__(self,**options):
        self.options = options
        self.conn = sqlite3.connect(self.options.get('database_name'))
        self.cursor = self.conn.cursor()

    def Create_Table(self,**details):
        fields_name = details.get('fields_name').split(',')
        query = f'CREATE TABLE {details.get("table_name")} ('
        total_fields = len(fields_name)
        count = 0
        for field in fields_name:
            if 'id' in field or 'sr_no' in field:
                query+=f'{field} INT PRIMARY KEY AUTOINCREMENT,'
                count+=1
            else:
                if count == total_fields-1:
                    query+=f'{field} CHAR(50)'
                else:
                    query += f'{field} CHAR(50),'
                    count+=1
        query+=')'

        print(query)
        print(status := self.conn.execute(query))
        if status:
            print(' Database and table has been created')
    def insert_data(self,**data):
        self.data = data
        entires_list = self.GetEntry()
        query = f'INSERT into {self.data.get("table_name")} ('
        count = 0
        for xd in entires_list:
            if count == len(entires_list) - 1:
                query+=xd
            else:
                query+=xd+','
                count+=1
        query+=') VALUES ('
        count_field = 0
        for xp in entires_list:
            if count_field == len(entires_list) -1:
                value = input(f' Put value for field <{xp}>: ')
                query+=f'"{value}"'
            else:
                value = input(f' Put value for field <{xp}>: ')
                query += f'"{value}",'
                count_field+=1
        query +=')'
        status = self.cursor.execute(query)
        self.conn.commit()
        if status:
            print(' Data saved to the database')
        else:
            print(' Failed to save database to the database')

    def load_data(self,tablename):
        query = f"SELECT * from {tablename}"
        data = self.cursor.execute(query).fetchall()
        for xp in data:
            print(xp)

        print(50*'-')
    def GetEntry(self):
        # query = f'select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME="{self.data.get("table_name")}"'
        query = f'PRAGMA table_info({self.data.get("table_name")})'
        status = self.cursor.execute(query).fetchall()
        fields = []
        for row in status:
            fields.append(row[1])
        return fields
if __name__ == "__main__":
    print(' SQL Management BY HOP\n ')
    while True:
        print(' [1] Create Table \n [2] Insert data \n [3] View data \n [4] Create database')
        match input('\n Choose operation: '):
            case '1':
                print(' Put database name, write any name if you dont have any database it will auto created')
                database = input(' Put database name: ')
                print('\n Put fields name separated by , Put keyword "id" or "sr_no" to have a id field')
                fields = input(' Put fields: ')
                table = input(' Put table name: ')
                Database(database_name=database).Create_Table(fields=len(fields.split(',')),fields_name=fields,table_name=table)
            case '2':
                table = input(' Put table name: ')
                database = input(' Database name: ')
                Database(database_name=database).insert_data(table_name=table)
            case '3':
                table = input(' Put table name: ')
                database = input(' Database name: ')
                Database(database_name=database).load_data(tablename=table)
            case '4':
                database = input(' Put database name: ')
                sqlite3.connect(database)
            case _:
                print(' Choose valid option ')

