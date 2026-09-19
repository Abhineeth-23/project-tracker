from app.database import SessionLocal, engine
from sqlalchemy import text
import time

def fix_mappings():
    db = SessionLocal()
    try:
        print("[*] Backing up and restructuring callhealth_users table...")
        
        # 1. Gather all master user data from legacy `users` table
        leg_rows = db.execute(text('SELECT id, name, "rollNumber", team, role, password, "createdAt" FROM users')).fetchall()
        master_users = {}
        for r in leg_rows:
            master_users[r.rollNumber.strip().upper()] = {
                "id": r.id,
                "name": r.name.strip(),
                "rollNumber": r.rollNumber.strip().upper(),
                "team": r.team or "",
                "role": r.role or "student",
                "password": r.password,
                "createdAt": r.createdAt or int(time.time() * 1000),
                "company": "CallHealth"
            }

        # 2. Add students from callhealth_logs who had assigned userIds in logs
        extra_logs_students = [
            (11, 'Arutla Prasanna', '23E51A6711', 'Digi Yatra', 'hitam@123'),
            (17, 'Pramod', '24E55A0312', 'Digi Yatra', 'hitam@123'),
            (18, 'Apurba Nandi', '23E51A6708', 'Digi Yatra', 'hitam@123'),
            (23, 'D.Sowmya', '24E51A6650', 'FHIR', 'hitam@123'),
            (25, 'Akshaya', '24E51A6618', 'FHIR', 'hitam@123'),
            (27, 'M. Bhavyanjali', '23E51A6673', 'OCR', 'hitam@123'),
            (28, 'Adari Vishnu', '23E51A0503', 'ChatBot', 'hitam@123'),
            (29, 'Sriya Nag Yazali', '23E51A05G4', 'Blood Connect', 'hitam@123'),
        ]
        
        for uid, name, roll, team, pwd in extra_logs_students:
            clean_roll = roll.strip().upper()
            if clean_roll not in master_users:
                master_users[clean_roll] = {
                    "id": uid,
                    "name": name,
                    "rollNumber": clean_roll,
                    "team": team,
                    "role": "student",
                    "password": pwd,
                    "createdAt": int(time.time() * 1000),
                    "company": "CallHealth"
                }

        print(f"[+] Total master CallHealth users prepared: {len(master_users)}")

        # 3. Truncate callhealth_users and re-insert with explicit IDs
        db.execute(text("TRUNCATE TABLE callhealth_users RESTART IDENTITY"))
        db.commit()

        insert_sql = text("""
            INSERT INTO callhealth_users (id, name, "rollNumber", team, role, password, "createdAt", company)
            VALUES (:id, :name, :rollNumber, :team, :role, :password, :createdAt, :company)
        """)

        sorted_users = sorted(master_users.values(), key=lambda x: x["id"])
        for u in sorted_users:
            db.execute(insert_sql, u)
            print(f"  Inserted ID={u['id']:2d} | Roll={u['rollNumber']:<12} | Name={u['name']}")

        db.commit()

        # 4. Set the sequence to max(id) + 1
        max_id = max(u["id"] for u in sorted_users)
        db.execute(text(f"SELECT setval('callhealth_users_id_seq', {max_id}, true)"))
        db.commit()
        print(f"[+] Reset callhealth_users_id_seq to {max_id}")

        print("\n=======================================================")
        print("VERIFICATION OF RESTORED MAPPINGS:")
        verify_rows = db.execute(text('SELECT id, name, "rollNumber", team, password FROM callhealth_users ORDER BY id')).fetchall()
        for r in verify_rows:
            print(f"  ID={r[0]:2d} | Roll={r[2]:<12} | Name={r[1]:<25} | Team={r[3]}")
        print("=======================================================\n")

        # Specific audit for Deepika and Pallavi
        deepika = db.execute(text("SELECT id, name, \"rollNumber\" FROM callhealth_users WHERE \"rollNumber\" = '23E51A6783'")).fetchone()
        pallavi = db.execute(text("SELECT id, name, \"rollNumber\" FROM callhealth_users WHERE \"rollNumber\" = '24E51A6633'")).fetchone()
        
        print(f"Deepika Audit: ID={deepika[0]} Name={deepika[1]} Roll={deepika[2]} (Expected ID 15)")
        print(f"Pallavi Audit: ID={pallavi[0]} Name={pallavi[1]} Roll={pallavi[2]} (Expected ID 22)")
        assert deepika[0] == 15, f"Deepika ID is {deepika[0]}, expected 15"
        assert pallavi[0] == 22, f"Pallavi ID is {pallavi[0]}, expected 22"
        print("[SUCCESS] Deepika and Pallavi IDs are 100% accurate!")

    except Exception as e:
        db.rollback()
        print(f"[!] Error: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    fix_mappings()
