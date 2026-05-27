-- 为 task_assign 表增加 DKID（地块ID）字段
-- 执行此迁移脚本以支持地块级别的独立人员分配

-- 1. 备份现有数据
CREATE TABLE task_assign_backup AS SELECT * FROM task_assign;

-- 2. 增加 DKID 字段
ALTER TABLE task_assign 
ADD COLUMN DKID INT COMMENT '地块ID' AFTER RWID;

-- 3. 清空现有数据（已备份）
DELETE FROM task_assign;

-- 4. 从备份表迁移数据：为每个任务-人员组合，在该任务的所有地块上创建分配记录
INSERT INTO task_assign (RWID, DKID, RYID, FPSJ)
SELECT DISTINCT bak.RWID, tp.DKID, bak.RYID, bak.FPSJ
FROM task_assign_backup bak
INNER JOIN task_plot tp ON bak.RWID = tp.RWID AND tp.SFSC = 0
WHERE bak.SFSC = 0;

-- 5. 恢复已删除的记录（保持SFSC=1的状态）
INSERT INTO task_assign (RWID, DKID, RYID, FPSJ, SFSC)
SELECT DISTINCT bak.RWID, tp.DKID, bak.RYID, bak.FPSJ, 1
FROM task_assign_backup bak
INNER JOIN task_plot tp ON bak.RWID = tp.RWID AND tp.SFSC = 0
WHERE bak.SFSC = 1;

-- 6. 可选：删除备份表（确认迁移无误后执行）
-- DROP TABLE task_assign_backup;
