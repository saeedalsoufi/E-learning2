import sqlite3

class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

        # This creates a new table to store classes data
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Classes
                            (server_id TEXT,
                             class_name TEXT,
                             teachers TEXT,
                             students TEXT,
                             PRIMARY KEY (server_id, class_name))''')

                # This creates a new table to store classes data
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Game_Points
                            (server_id TEXT,
                             user_id TEXT,
                             points NUMBER,
                             PRIMARY KEY (server_id, user_id))''')


    def add_point(self, server_id, user_id):
        self.conn.execute("INSERT OR IGNORE INTO Game_Points (server_id, user_id, points) VALUES (?, ?, 0)",
                          (server_id, user_id))
        self.conn.execute("UPDATE Game_Points SET points = points + 1 WHERE server_id = ? AND user_id = ?",
                          (server_id, user_id))
        self.conn.commit()

    def remove_point(self, server_id, user_id):
        self.conn.execute("INSERT OR IGNORE INTO Game_Points (server_id, user_id, points) VALUES (?, ?, 0)",
                          (server_id, user_id))
        self.conn.execute("UPDATE Game_Points SET points = points - 1 WHERE server_id = ? AND user_id = ?",
                          (server_id, user_id))
        self.conn.commit()

    def createclass(self, server_id, class_name, teachers='', students=''):
        # This function creates a new class row
        self.conn.execute("INSERT INTO classes (server_id, class_name, teachers, students) VALUES (?, ?, ?, ?)",
                           (server_id, class_name, teachers, students))
        self.conn.commit()

    def editclass(self, server_id, class_name, updated_fields):
        # This function will edit an existing row to add/remove students or teachers.
        if updated_fields:
            for column, value in updated_fields.items():
                self.conn.execute(f"UPDATE classes SET `{column}` = ? WHERE server_id = ? AND class_name = ?",
                                  (value, server_id, class_name))
            self.conn.commit()






    def getclass(self, server_id, class_name):
        # Using the server ID and class name we can use this function to pull info out of a class
        cursor = self.conn.execute("SELECT * FROM classes WHERE server_id = ? AND class_name = ?",
                                   (server_id, class_name))

        result = cursor.fetchone()

        cursor.close()

        return result[2] if result is not None else None

    def get_points(self, server_id, user_id):
        # Using the server ID and user ID, we can use this function to get the points
        cursor = self.conn.execute("SELECT points FROM Game_Points WHERE server_id = ? AND user_id = ?",
                                   (server_id, user_id))

        result = cursor.fetchone()
        cursor.close()

        return result[0] if result is not None else None


    def listclasses(self, server_id):
        # This wil list all classes in the server
        cursor = self.conn.execute("SELECT class_name, teachers, students FROM classes WHERE server_id = ?",
                                   (server_id,))

        results = cursor.fetchall()

        cursor.close()

        return results
