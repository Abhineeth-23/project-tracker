import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sql_app.db")

def migrate():
    print(f"Connecting to database at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    columns_to_add = [
        ("suggestionType", "VARCHAR"),
        ("suggestionDescription", "VARCHAR"),
        ("suggestionDeadline", "VARCHAR"),
        ("suggestionStatus", "VARCHAR DEFAULT 'Pending'")
    ]

    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE logs ADD COLUMN {col_name} {col_type}")
            print(f"Successfully added column {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Column {col_name} already exists. Skipping.")
            else:
                print(f"Error adding column {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
