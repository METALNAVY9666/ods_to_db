"""converts the passed ods file """
import sys
import os
import json
import datetime
import sqlite3
import pyexcel_ods3


def list_to_query(lst: list, debug=False) -> str:
    """converts a python list object into a sql 'values' set"""
    if debug:
        print(len(lst), " bills in ods file : ")
    for index, row in enumerate(lst):
        lst[index] = [index] + lst[index]
    for index, row in enumerate(lst):
        if type(row[1]).__name__ == "date":
            lst[index][1] = row[1].strftime("%m/%d/%Y")
    for index, row in enumerate(lst):
        if debug:
            print("\t", index, " : ", row)
            print("\t", type(row[0]).__name__)
    sys.exit()
    return json.dumps(lst).replace('"', "'").replace("[", "(").replace("]", ")")[1: -1]


class Database:
    """handles the conversion between ods file and db file"""
    def __init__(self, dest: str, debug=False):
        self.debug = debug
        if not os.path.isfile(dest):
            print(f"* Database '{dest}' does not exist !")
            sys.exit()
        self.connexion = sqlite3.connect(dest)
        self.cursor = self.connexion.cursor()

    def update(self, src: str, sheet_name: str, table: str):
        """overwrite the sheet of the ods file in the table of the database"""
        ods_rows = pyexcel_ods3.get_data(src)[sheet_name][1:]
        try:
            self.push(f"delete from {table}")
        except sqlite3.OperationalError as error:
            if self.debug:
                print(error)
            if f"no such table: {table}" == str(error):
                print(f"* Table '{table}' does not exist !")
                sys.exit()
        query = f"insert into {table} values {list_to_query(ods_rows, self.debug)}"
        if self.debug:
            print("query:\n", query, "\n")
        self.push(query)
        if self.debug:
            print("updated db:\n", self.pull(f"select * from {table}"), "\n")

    def pull(self, cmd: str) -> list:
        """simple pull query on the database"""
        return self.cursor.execute(cmd).fetchall()

    def push(self, cmd: str):
        """simple push query on the database"""
        self.cursor.execute(cmd)
        self.connexion.commit()

    def close(self):
        """closes the database (saves data)"""
        self.connexion.close()


if __name__ == "__main__":
    DEBUG = False
    argc = len(sys.argv)
    if argc not in (5, 6):
        print("ods to db")
        print("\noptional commands (at the end): \n\t-d --debug : debug")
        print("\nusage : ./ods_to_db odsfile.ods database.db ods_file_sheet database_table")
        print("\nexample: ./ods_to_db interventions.ods database.db Sheet1 interventions")
        sys.exit()
    if argc == 6:
        if sys.argv[5] in ["-d", "--debug"]:
            DEBUG = True
    database = Database(sys.argv[2], DEBUG)
    database.update(sys.argv[1], sys.argv[3], sys.argv[4])
    database.close()
    print("Database updated sucessfully.")
