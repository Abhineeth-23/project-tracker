import os
import sys
from sqlalchemy import text
from app.database import engine, SQLALCHEMY_DATABASE_URL

def run_migration():
    print(f"Running migration against: {SQLALCHEMY_DATABASE_URL[:30]}...")
    tables = ["users", "teams", "logs", "moms", "holidays"]
    
    with engine.connect() as conn:
        for table in tables:
            try:
                # Add company column if not exists
                if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
                    try:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN company VARCHAR DEFAULT 'CallHealth'"))
                        print(f"Added 'company' column to SQLite table {table}")
                    except Exception as e:
                        if "duplicate column" in str(e).lower():
                            print(f"'company' column already exists in SQLite table {table}")
                        else:
                            print(f"SQLite notice on {table}: {e}")
                else:
                    # PostgreSQL syntax
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS company VARCHAR DEFAULT 'CallHealth'"))
                    print(f"Verified/Added 'company' column to Postgres table {table}")
                
                # Backfill any nulls with 'CallHealth'
                conn.execute(text(f"UPDATE {table} SET company = 'CallHealth' WHERE company IS NULL OR company = ''"))
                print(f"Backfilled existing rows in {table} with company='CallHealth'")
                
            except Exception as ex:
                print(f"Error migrating table {table}: {ex}")
                
        conn.commit()
    print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()
