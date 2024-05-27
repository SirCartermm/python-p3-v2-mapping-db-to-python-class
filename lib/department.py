import sqlite3

class Department:
    all = {}

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.id = None

    def __repr__(self):
        return f"Department('{self.name}', '{self.location}')"

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS departments")
        conn.commit()
        conn.close()

    @classmethod
    def new_department(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    def save(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """, (self.name, self.location))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            """, (self.name, self.location, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def instance_from_db(cls, row):
        department = cls(row[1], row[2])
        department.id = row[0]
        cls.all[department.id] = department
        return department

    @classmethod
    def get_all(cls):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        rows = cursor.fetchall()
        conn.close()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None