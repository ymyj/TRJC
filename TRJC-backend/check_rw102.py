import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT ta.ID, ta.RWID, ta.DKID, ta.RYID FROM task_assign ta WHERE ta.SFSC = 0 AND ta.RWID = 102 ORDER BY ta.DKID"))
    print("=== TaskAssign records (RWID=102, SFSC=0) ===")
    print(f"{'ID':<5} {'RWID':<6} {'DKID':<6} {'RYID':<6}")
    print("-" * 30)
    for row in result:
        print(f"{row[0]:<5} {row[1]:<6} {row[2]:<6} {row[3]:<6}")
    result2 = conn.execute(text("SELECT tp.ID, tp.RWID, tp.DKID FROM task_plot tp WHERE tp.SFSC = 0 AND tp.RWID = 102 ORDER BY tp.DKID"))
    print("\n=== TaskPlot records (RWID=102, SFSC=0) ===")
    print(f"{'ID':<5} {'RWID':<6} {'DKID':<6}")
    print("-" * 20)
    for row in result2:
        print(f"{row[0]:<5} {row[1]:<6} {row[2]:<6}")
