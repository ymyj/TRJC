"""
数据库迁移脚本：为 task_assign 表添加 DKID 字段
执行：python migrations/add_dkid_to_task_assign.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

def run_migration():
    with engine.begin() as conn:
        # 1. 检查 DKID 列是否已存在
        result = conn.execute(text("""
            SELECT COLUMN_NAME FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'task_assign'
            AND COLUMN_NAME = 'DKID'
        """))
        if result.fetchone():
            print("DKID 字段已存在，跳过添加。")
        else:
            print("正在添加 DKID 字段...")
            conn.execute(text("ALTER TABLE task_assign ADD COLUMN DKID INT COMMENT '地块ID' AFTER RWID"))
            print("DKID 字段添加成功。")

        # 2. 迁移数据：为每个任务-人员组合，在该任务的所有地块上创建分配记录
        print("正在迁移历史数据...")
        
        # 先备份
        conn.execute(text("DROP TABLE IF EXISTS task_assign_backup"))
        conn.execute(text("CREATE TABLE task_assign_backup AS SELECT * FROM task_assign"))
        print("  已创建备份表 task_assign_backup")
        
        # 清空现有数据
        conn.execute(text("DELETE FROM task_assign"))
        
        # 从备份恢复：为每个任务-人员组合，在该任务的所有地块上创建分配记录
        conn.execute(text("""
            INSERT INTO task_assign (RWID, DKID, RYID, FPSJ)
            SELECT DISTINCT bak.RWID, tp.DKID, bak.RYID, bak.FPSJ
            FROM task_assign_backup bak
            INNER JOIN task_plot tp ON bak.RWID = tp.RWID AND tp.SFSC = 0
            WHERE bak.SFSC = 0
        """))
        
        # 恢复已删除的记录
        conn.execute(text("""
            INSERT INTO task_assign (RWID, DKID, RYID, FPSJ, SFSC)
            SELECT DISTINCT bak.RWID, tp.DKID, bak.RYID, bak.FPSJ, 1
            FROM task_assign_backup bak
            INNER JOIN task_plot tp ON bak.RWID = tp.RWID AND tp.SFSC = 0
            WHERE bak.SFSC = 1
        """))
        
        print("历史数据迁移完成。")
        print("迁移成功！备份表 task_assign_backup 仍保留，确认无误后可手动删除。")

if __name__ == "__main__":
    run_migration()
