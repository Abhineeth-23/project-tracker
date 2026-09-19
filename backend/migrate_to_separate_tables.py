import os
import sys
from sqlalchemy import text
from app.database import engine, SessionLocal, Base
from app.models import (
    CallHealthUser, CallHealthTeam, CallHealthLog, CallHealthHoliday, CallHealthMoM,
    SucceedUser, SucceedTeam, SucceedLog, SucceedHoliday, SucceedMoM
)

def run_migration():
    print("[*] Creating all 10 physically separate SQL tables...")
    Base.metadata.create_all(bind=engine)
    print("[+] Tables created in PostgreSQL / SQLite successfully!")

    db = SessionLocal()
    try:
        # 1. Migrate CallHealth Teams
        ch_teams_count = db.query(CallHealthTeam).count()
        if ch_teams_count == 0:
            print("[*] Migrating CallHealth teams...")
            rows = db.execute(text("SELECT id, name FROM teams WHERE company = 'CallHealth' OR company IS NULL")).fetchall()
            for r in rows:
                db.add(CallHealthTeam(name=r.name, company="CallHealth"))
            db.commit()
            print(f"[+] Migrated {len(rows)} teams to callhealth_teams.")
        else:
            print(f"[i] callhealth_teams already has {ch_teams_count} records.")

        # 2. Migrate Succeed Teams
        si_teams_count = db.query(SucceedTeam).count()
        if si_teams_count == 0:
            print("[*] Migrating Succeed International teams...")
            rows = db.execute(text("SELECT id, name FROM teams WHERE company = 'Succeed International'")).fetchall()
            if rows:
                for r in rows:
                    db.add(SucceedTeam(name=r.name, company="Succeed International"))
                db.commit()
                print(f"[+] Migrated {len(rows)} teams to succeed_teams.")
            else:
                starter = ["Full Stack", "AI & ML", "Cloud Architecture", "QA & Testing"]
                for t in starter:
                    db.add(SucceedTeam(name=t, company="Succeed International"))
                db.commit()
                print(f"[+] Seeded {len(starter)} starter teams into succeed_teams.")
        else:
            print(f"[i] succeed_teams already has {si_teams_count} records.")

        # 3. Migrate Users
        ch_users_count = db.query(CallHealthUser).count()
        if ch_users_count == 0:
            print("[*] Migrating CallHealth users...")
            rows = db.execute(text("SELECT name, \"rollNumber\", team, role, \"createdAt\", password FROM users WHERE company = 'CallHealth' OR company IS NULL")).fetchall()
            for r in rows:
                db.add(CallHealthUser(
                    name=r.name,
                    rollNumber=r.rollNumber,
                    team=r.team or "",
                    role=r.role or "user",
                    createdAt=r.createdAt,
                    password=r.password,
                    company="CallHealth"
                ))
            db.commit()
            print(f"[+] Migrated {len(rows)} users to callhealth_users.")
        else:
            print(f"[i] callhealth_users already has {ch_users_count} records.")

        # 4. Migrate Logs
        ch_logs_count = db.query(CallHealthLog).count()
        if ch_logs_count == 0:
            print("[*] Migrating CallHealth logs...")
            rows = db.execute(text("""
                SELECT "userId", name, "rollNumber", team, hours, "todayLog", "tomorrowGoal", 
                       date, timestamp, suggestiontype, suggestiondescription, suggestiondeadline, suggestionstatus
                FROM logs 
                WHERE company = 'CallHealth' OR company IS NULL
            """)).fetchall()
            for r in rows:
                db.add(CallHealthLog(
                    userId=r.userId,
                    name=r.name,
                    rollNumber=r.rollNumber,
                    team=r.team or "",
                    hours=r.hours,
                    todayLog=r.todayLog,
                    tomorrowGoal=r.tomorrowGoal,
                    date=r.date,
                    timestamp=r.timestamp,
                    suggestionType=r.suggestiontype,
                    suggestionDescription=r.suggestiondescription,
                    suggestionDeadline=r.suggestiondeadline,
                    suggestionStatus=r.suggestionstatus or "Pending",
                    company="CallHealth"
                ))
            db.commit()
            print(f"[+] Migrated {len(rows)} logs to callhealth_logs.")
        else:
            print(f"[i] callhealth_logs already has {ch_logs_count} records.")

        # 5. Migrate MoMs
        ch_moms_count = db.query(CallHealthMoM).count()
        if ch_moms_count == 0:
            print("[*] Migrating CallHealth MoMs...")
            rows = db.execute(text("SELECT date, agenda, attendees, content, created_by, file_name, file_path FROM moms WHERE company = 'CallHealth' OR company IS NULL")).fetchall()
            for r in rows:
                db.add(CallHealthMoM(
                    date=r.date,
                    agenda=r.agenda,
                    attendees=r.attendees,
                    content=r.content,
                    created_by=r.created_by,
                    file_name=r.file_name,
                    file_path=r.file_path,
                    company="CallHealth"
                ))
            db.commit()
            print(f"[+] Migrated {len(rows)} MoMs to callhealth_moms.")
        else:
            print(f"[i] callhealth_moms already has {ch_moms_count} records.")

        # 6. Migrate Holidays
        ch_holidays_count = db.query(CallHealthHoliday).count()
        if ch_holidays_count == 0:
            print("[*] Migrating CallHealth holidays...")
            rows = db.execute(text("SELECT date, name FROM holidays WHERE company = 'CallHealth' OR company = 'All' OR company IS NULL")).fetchall()
            for r in rows:
                db.add(CallHealthHoliday(
                    date=r.date,
                    name=r.name,
                    company="CallHealth"
                ))
            db.commit()
            print(f"[+] Migrated {len(rows)} holidays to callhealth_holidays.")
        else:
            print(f"[i] callhealth_holidays already has {ch_holidays_count} records.")

        print("\n=======================================================")
        print("PHYSICAL SEPARATE TABLES MIGRATION AUDIT:")
        print(f"  callhealth_teams:    {db.query(CallHealthTeam).count()} records")
        print(f"  callhealth_users:    {db.query(CallHealthUser).count()} records")
        print(f"  callhealth_logs:     {db.query(CallHealthLog).count()} records")
        print(f"  callhealth_moms:     {db.query(CallHealthMoM).count()} records")
        print(f"  callhealth_holidays: {db.query(CallHealthHoliday).count()} records")
        print("  -----------------------------------------------------")
        print(f"  succeed_teams:       {db.query(SucceedTeam).count()} records")
        print(f"  succeed_users:       {db.query(SucceedUser).count()} records")
        print(f"  succeed_logs:        {db.query(SucceedLog).count()} records")
        print(f"  succeed_moms:        {db.query(SucceedMoM).count()} records")
        print(f"  succeed_holidays:    {db.query(SucceedHoliday).count()} records")
        print("=======================================================")

    except Exception as e:
        db.rollback()
        print(f"[!] Error during migration: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
