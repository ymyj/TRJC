import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT ta.ID, ta.RWID, ta.DKID, ta.RYID FROM task_assign ta WHERE ta.SFSC = 0 ORDER BY ta.RWID, ta.DKID"))
    print("=== TaskAssign records (SFSC=0) ===")
    print(f"{'ID':<5} {'RWID':<6} {'DKID':<6} {'RYID':<6}")
    print("-" * 30)
    for row in result:
        print(f"{row[0]:<5} {row[1]:<6} {row[2]:<6} {row[3]:<6}")
    result2 = conn.execute(text("SELECT ID, LXFS FROM person_info WHERE SFSC = 0"))
    print("\n=== PersonInfo records ===")
    print(f"{'ID':<5} LXFS(encrypted)")
    print("-" * 30)
    for row in result2:
        print(f"{row[0]:<5} {row[1]}")
