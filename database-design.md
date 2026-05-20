# 数据库表设计（最终版）

## 表关联关系（逻辑关联，无外键约束）

```
task_info (任务表)
├── RWBH (任务编号) - 自动生成器
│
├── task_plot (任务地块关联表)
│   ├── RWID → task_info.ID
│   └── DKID → plot_info.ID
│
├── task_assign (任务分配表)
│   ├── RWID → task_info.ID
│   └── RYID → person_info.ID
│
├── survey_record (勘察记录表)
│   ├── RWID → task_info.ID
│   └── DKID → plot_info.ID
│
├── sample_record (样品采集记录表)
│   ├── RWID → task_info.ID
│   └── DKID → plot_info.ID
│
└── farmland_dataset (耕地质量数据集表)
    ├── 聚合自 survey_record + sample_record + task_info + plot_info
    └── 包含完整的33个字段（来自详情弹窗）
```

---

## 字段命名规则
- 使用中文拼音首字母大写
- 例如：姓名 → XM、联系方式 → LXFS、图斑编号 → TBH

---

## 1. person_info 表 - 人员信息表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 姓名 | XM | VARCHAR(200) | **加密存储**，前端脱敏显示 |
| 联系方式 | LXFS | VARCHAR(200) | **加密存储**，前端脱敏显示 |
| 岗位 | GW | VARCHAR(20) | 项目经理/技术员/采样员/分析员 |
| 所属区划 | SSQH | VARCHAR(50) | 负责区域 |
| 所属部门 | SSBM | VARCHAR(50) | 所属部门 |
| 人员状态 | RYZT | VARCHAR(20) | active/inactive |
| 创建时间 | CJSJ | DATETIME | 创建时间 |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

### 加密/脱敏处理

**后端加密存储：**
- 姓名（XM）和联系方式（LXFS）字段在入库前进行加密
- 使用对称加密算法（如 AES）
- 数据库存储密文

**前端脱敏显示：**
- 姓名：只显示第一位字符，其余用 `**` 表示
  - 示例：`张**`（原：`张调查员`）
- 联系方式：保留前3位和后4位，中间4位用 `****` 表示
  - 示例：`138****8001`（原：`13800138001`）

---

## 2. plot_info 表 - 地块信息表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 图斑编号 | TBH | VARCHAR(50) | 图斑编号，前端手动填写 |
| 所属单元 | SSDY | VARCHAR(50) | 所属单元 |
| 图斑面积 | TBMJ | DECIMAL(10,2) | 图斑面积(㎡) |
| 所属区划 | SSQH | VARCHAR(50) | 所属区划 |
| 经度 | JD | DECIMAL(10,6) | 经度 |
| 纬度 | WD | DECIMAL(10,6) | 纬度 |
| 围栏坐标 | WLZB | JSON | 围栏多边形坐标点 |
| 创建时间 | CJSJ | DATETIME | 创建时间 |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 3. task_info 表 - 任务信息表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 任务编号 | RWBH | VARCHAR(50) | **自动生成器**：RW+年份+序号 |
| 任务名称 | RWMC | VARCHAR(200) | 任务名称 |
| 任务类型 | RWLX | VARCHAR(20) | routine/supplement/special/census/check |
| 所属区划 | SSQH | VARCHAR(50) | 所属区划 |
| 负责人 | FZR | VARCHAR(50) | 项目负责人 |
| 状态 | ZT | VARCHAR(20) | draft/pending/processing/completed |
| 创建时间 | CJSJ | DATETIME | 创建时间 |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 4. task_plot 表 - 任务地块关联表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 任务ID | RWID | INT | 关联 task_info.ID |
| 地块ID | DKID | INT | 关联 plot_info.ID |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 5. task_assign 表 - 任务分配表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 任务ID | RWID | INT | 关联 task_info.ID |
| 人员ID | RYID | INT | 关联 person_info.ID |
| 分配时间 | FPSJ | DATETIME | 分配时间 |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 6. survey_record 表 - 勘察记录表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 任务ID | RWID | INT | 关联 task_info.ID |
| 地块ID | DKID | INT | 关联 plot_info.ID |
| 项目名称 | XMMC | VARCHAR(200) | 项目名称 |
| 图斑编号 | TBH | VARCHAR(50) | 图斑编号 |
| 面积 | MJ | DECIMAL(10,2) | 面积(㎡) |
| **地理位置** | **DLWZ** | **VARCHAR(200)** | **完整地理位置：市+县+村** |
| 地理坐标-经度 | DLZB-JD | VARCHAR(50) | 地理坐标-经度 |
| 地理坐标-纬度 | DLZB-WD | VARCHAR(50) | 地理坐标-纬度 |
| 变更前土地利用类型 | BGQ | VARCHAR(50) | 变更前土地利用类型 |
| 变更时间 | BGSJ | VARCHAR(20) | 变更时间 |
| 利用类型 | LYLX | VARCHAR(50) | 利用类型 |
| 有效土层厚度 | YXTCHD | DECIMAL(5,2) | 有效土层厚度(cm) |
| 侵入体类型及含量 | QRLXJHL | VARCHAR(50) | 侵入体类型及含量(%) |
| 砾石含量 | LSHL | DECIMAL(5,2) | 砾石含量(%) |
| 地形坡度 | DXPD | DECIMAL(5,2) | 地形坡度(°) |
| 田面平整程度 | TMPZCD | VARCHAR(20) | 田面平整程度 |
| 水资源保障条件 | SZBZTJ | VARCHAR(20) | 水资源保障条件 |
| 道路通行条件 | DLTXTJ | VARCHAR(20) | 道路通行条件 |
| 地形部位 | DXBW | VARCHAR(50) | 地形部位 |
| 质地构型 | ZDGX | VARCHAR(50) | 质地构型 |
| 排水能力 | PSNL | VARCHAR(20) | 排水能力 |
| 海拔高度 | HBGD | DECIMAL(8,2) | 海拔高度(m) |
| 农田防护与生态环境保护水平 | NTFH | VARCHAR(20) | 农田防护与生态环境保护水平 |
| 耕层厚度 | GCHD | DECIMAL(5,2) | 耕层厚度(cm) |
| 勘察日期 | KCRQ | DATE | 勘察日期 |
| 调查人员 | DCRY | VARCHAR(50) | 调查人员(签字) |
| 项目承担单位代表 | XMDWDB | VARCHAR(50) | 项目承担单位代表(签字) |
| 踏勘专家 | TKZJ | VARCHAR(50) | 踏勘专家(签字) |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 7. sample_record 表 - 样品采集记录表

| 中文字段 | 数据库字段 | 数据类型 | 说明 |
|----------|-----------|----------|------|
| ID | ID | INT | 主键，自增 |
| 任务ID | RWID | INT | 关联 task_info.ID |
| 地块ID | DKID | INT | 关联 plot_info.ID |
| 土壤混合样品编号 | TRHHYPBH | VARCHAR(50) | 前端手动填写 |
| **地理位置** | **DLWZ** | **VARCHAR(200)** | **完整地理位置：市+县+村** |
| 地理坐标-点1编号 | DLZB-D1BH | VARCHAR(50) | 地理坐标-点1编号 |
| 地理坐标-点1经度 | DLZB-D1JD | VARCHAR(50) | 地理坐标-点1经度 |
| 地理坐标-点1纬度 | DLZB-D1WD | VARCHAR(50) | 地理坐标-点1纬度 |
| 地理坐标-点2编号 | DLZB-D2BH | VARCHAR(50) | 地理坐标-点2编号 |
| 地理坐标-点2经度 | DLZB-D2JD | VARCHAR(50) | 地理坐标-点2经度 |
| 地理坐标-点2纬度 | DLZB-D2WD | VARCHAR(50) | 地理坐标-点2纬度 |
| 地理坐标-点3编号 | DLZB-D3BH | VARCHAR(50) | 地理坐标-点3编号 |
| 地理坐标-点3经度 | DLZB-D3JD | VARCHAR(50) | 地理坐标-点3经度 |
| 地理坐标-点3纬度 | DLZB-D3WD | VARCHAR(50) | 地理坐标-点3纬度 |
| 采样深度-点1 | CYSD-D1 | VARCHAR(50) | 采样深度-点1 |
| 采样深度-点2 | CYSD-D2 | VARCHAR(50) | 采样深度-点2 |
| 采样深度-点3 | CYSD-D3 | VARCHAR(50) | 采样深度-点3 |
| 采样点位数量 | CYDWSL | INT | 采样点位数量(个) |
| 混合样品重量 | HHYPSL | DECIMAL(8,2) | 混合样品重量(g) |
| 采样日期 | CYRQ | DATE | 采样日期 |
| 采样人员 | CYRY | VARCHAR(50) | 采样人员(签字) |
| 项目承担单位代表 | XMDWDB | VARCHAR(50) | 项目承担单位代表(签字) |
| 踏勘专家 | TKZJ | VARCHAR(50) | 踏勘专家(签字) |
| 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 8. farmland_dataset 表 - 耕地质量数据集表（完整版）

此表聚合了勘察记录、样品采集、分析结果和任务基础信息，共 **33个字段**：

| 序号 | 中文字段 | 数据库字段 | 数据类型 | 数据来源 |
|------|----------|-----------|----------|----------|
| 1 | ID | ID | INT | 自增主键 |
| 2 | 任务ID | RWID | INT | task_info.ID |
| 3 | 地块ID | DKID | INT | plot_info.ID |
| 4 | 任务名称 | RWMC | VARCHAR(200) | task_info.RWMC |
| 5 | 图斑编号 | TBH | VARCHAR(50) | plot_info.TBH |
| 6 | 经度 | JD | DECIMAL(10,6) | plot_info.JD |
| 7 | 纬度 | WD | DECIMAL(10,6) | plot_info.WD |
| 8 | 采样日期 | CYRQ | DATE | sample_record.CYRQ |
| 9 | 地形部位 | DXBW | VARCHAR(50) | survey_record.DXBW |
| 10 | 有效土层厚度 | YXTCHD | DECIMAL(5,2) | survey_record.YXTCHD |
| 11 | 耕层质地 | GCZD | VARCHAR(50) | H5端填写 |
| 12 | 容重 | RZ | DECIMAL(5,2) | H5端填写 |
| 13 | 质地构型 | ZDGX | VARCHAR(50) | survey_record.ZDGX |
| 14 | 生物多样性 | SWDYX | VARCHAR(20) | H5端填写 |
| 15 | 农田林网化程度 | NTLW | VARCHAR(20) | H5端填写 |
| 16 | 障碍因素 | ZAYS | VARCHAR(50) | H5端填写 |
| 17 | 灌溉能力 | GGNL | VARCHAR(20) | H5端填写 |
| 18 | 排水能力 | PSNL | VARCHAR(20) | survey_record.PSNL |
| 19 | pH值 | PHZ | DECIMAL(4,2) | H5端填写 |
| 20 | 有机质 | YJZ | DECIMAL(8,2) | H5端填写 |
| 21 | 有效磷 | YXL | DECIMAL(8,2) | H5端填写 |
| 22 | 速效钾 | SXJ | DECIMAL(8,2) | H5端填写 |
| 23 | 水溶性盐总量 | SRXYLZL | DECIMAL(8,2) | H5端填写 |
| 24 | 地类名称 | DLMC | VARCHAR(50) | H5端填写 |
| 25 | 清洁程度 | JQCD | VARCHAR(20) | H5端填写 |
| 26 | 备注 | BZ | VARCHAR(500) | H5端填写 |
| 27 | 镉 | GD | DECIMAL(8,3) | H5端填写 |
| 28 | 总汞 | ZG | DECIMAL(8,3) | H5端填写 |
| 29 | 总砷 | ZS | DECIMAL(8,2) | H5端填写 |
| 30 | 铅 | Q | DECIMAL(8,2) | H5端填写 |
| 31 | 铬 | G | DECIMAL(8,2) | H5端填写 |
| 32 | 耕地质量等级 | GDZLDJ | DECIMAL(10,6) | 计算得出 |
| 33 | 质量分级 | ZLFJ | VARCHAR(20) | 计算得出 |
| 34 | 是否删除 | SFSC | TINYINT | **软删除标记**：0-未删除，1-已删除 |

---

## 字段补充说明

### 数据来源关系
```
farmland_dataset (耕地质量数据集)
├── 基础信息：task_info (任务名称)、plot_info (图斑编号、经纬度)
├── 勘察数据：survey_record (地形部位、有效土层厚度、质地构型、排水能力)
├── 采集数据：sample_record (采样日期)
└── 分析数据：H5端录入 (pH、有机质、重金属等20+字段)
```

### 关键字段说明

1. **RWBH (任务编号)** - 使用生成器自动生成：RW + 年份(4位) + 序号(5位)
2. **DLWZ (地理位置)** - 完整字段，H5端填写，PC端直接显示
3. **farmland_dataset** - 33个业务字段 + 1个软删除标记
4. **GDZLDJ/ZLFJ** - 耕地质量等级和质量分级，由算法计算得出
5. **XM/LXFS (姓名/联系方式)** - 数据库加密存储，前端脱敏显示
6. **SFSC (是否删除)** - 所有表都有的软删除标记

---

## 软删除处理规则

所有查询默认添加条件 `WHERE SFSC = 0`

删除操作执行：`UPDATE table SET SFSC = 1 WHERE ID = ?`
