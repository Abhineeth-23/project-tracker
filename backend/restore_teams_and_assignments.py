from app.database import engine, SessionLocal
from app.models import CallHealthTeam, CallHealthUser, SucceedTeam
from sqlalchemy import text

def restore():
    db = SessionLocal()
    try:
        # All 12 CallHealth teams that were in logs and projects
        all_ch_teams = [
            'Blood Connect', 'Prachtiz', 'CHAV', 'Automation', 
            'Ambulance Connect', 'Audit', 'CHID', 'FHIR', 
            'MIRTH Connect', 'Digi Yatra', 'OCR', 'ChatBot'
        ]
        
        # 1. Restore all 12 CallHealth Teams
        existing_ch = {t.name for t in db.query(CallHealthTeam).all()}
        for tname in all_ch_teams:
            if tname not in existing_ch:
                db.add(CallHealthTeam(name=tname, company='CallHealth'))
                print(f"[+] Restored CallHealth team: {tname}")
        db.commit()
        
        # 2. Restore student teams in callhealth_users from legacy users table
        legacy_users = db.execute(text('SELECT "rollNumber", team FROM users WHERE team IS NOT NULL AND team != \'\'')).fetchall()
        for r in legacy_users:
            db.query(CallHealthUser).filter(CallHealthUser.rollNumber == r.rollNumber).update({CallHealthUser.team: r.team})
        db.commit()
        print(f"[+] Restored {len(legacy_users)} student team assignments in callhealth_users.")

        # 3. Restore Succeed teams
        all_si_teams = ['Full Stack', 'AI & ML', 'Cloud Architecture', 'QA & Testing']
        existing_si = {t.name for t in db.query(SucceedTeam).all()}
        for tname in all_si_teams:
            if tname not in existing_si:
                db.add(SucceedTeam(name=tname, company='Succeed International'))
                print(f"[+] Restored Succeed team: {tname}")
        db.commit()

        print("\n=================================================")
        print("RESTORATION AUDIT:")
        print(f"  callhealth_teams: {db.query(CallHealthTeam).count()} records (Full 12 Teams)")
        print(f"  succeed_teams:    {db.query(SucceedTeam).count()} records (4 Teams)")
        print(f"  callhealth_users: {db.query(CallHealthUser).count()} records (17 Students)")
        print("=================================================")
        
        print("\nStudent Roster:")
        for u in db.query(CallHealthUser).order_by(CallHealthUser.name).all():
            print(f"  {u.name.strip()} ({u.rollNumber}) -> Team: {u.team or 'Unassigned'}")

    finally:
        db.close()

if __name__ == "__main__":
    restore()
