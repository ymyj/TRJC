-- 数据库迁移脚本：添加公司字段和任务创建人字段
-- 执行日期: 2026-06-04

-- 1. 人员表添加公司字段
ALTER TABLE person_info ADD COLUMN GS VARCHAR(100) COMMENT '所属公司';

-- 2. 任务表添加创建人字段
ALTER TABLE task_info ADD COLUMN CJR INT COMMENT '创建人ID';

-- 3. 初始化第一个项目经理的公司（用于首次登录系统）
UPDATE person_info SET GS = '默认公司' WHERE GW = '项目经理' LIMIT 1;
