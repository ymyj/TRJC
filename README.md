# 耕地质量监测管理系统 (TRJC)

## 项目简介

耕地质量监测管理系统是一个前后端分离的Web应用，用于管理农田质量监测相关任务、人员、地块等信息。系统包含PC端管理后台和H5移动端应用。

## 技术架构

### 后端
- **框架**: FastAPI (Python)
- **数据库**: MySQL
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (JSON Web Token)
- **加密**: bcrypt, cryptography (AES对称加密)

### 前端 (PC端)
- **框架**: Vue.js 3
- **构建工具**: Vite 5
- **路由**: Vue Router 4
- **HTTP客户端**: Axios

### 前端 (H5移动端)
- **框架**: Vue.js 3
- **UI组件库**: Vant 4
- **状态管理**: Pinia
- **构建工具**: Vite 5

## 功能模块

### 1. 任务管理
- 任务发布（关联地块、人员）
- 任务列表查询
- 任务分配
- 任务详情查看

### 2. 人员管理
- 人员信息维护
- 敏感数据加密存储
- 前端脱敏显示

### 3. 地块管理
- 地块信息录入
- 地理坐标管理
- 围栏坐标管理

### 4. 勘察记录
- 勘察信息填写
- 关联任务和地块

### 5. 样品采集
- 土壤混合样品管理
- 采样点位记录

### 6. 耕地质量数据集
- 数据聚合展示（33个业务字段）
- 耕地质量等级计算
- 质量分级

## 项目结构

```
TRJC/
├── README.md
├── database-design.md          # 数据库设计文档
├── TRJC-backend/               # 后端项目
│   ├── app/
│   │   ├── api/                # API路由
│   │   │   ├── auth.py         # 认证相关
│   │   │   ├── tasks.py        # 任务管理
│   │   │   ├── personnel.py    # 人员管理
│   │   │   ├── plots.py        # 地块管理
│   │   │   ├── survey.py       # 勘察记录
│   │   │   ├── samples.py      # 样品采集
│   │   │   └── datasets.py     # 数据集
│   │   ├── middleware/
│   │   │   └── auth.py         # 认证中间件
│   │   ├── models/             # 数据模型
│   │   ├── schemas/            # 数据验证
│   │   ├── utils/              # 工具类
│   │   │   ├── crypto.py       # 加密解密
│   │   │   └── code_generator.py
│   │   ├── config.py           # 配置
│   │   ├── database.py         # 数据库连接
│   │   └── main.py             # 入口
│   ├── requirements.txt
│   └── .env                    # 环境变量
├── TRJC-web/                   # PC端前端
│   ├── src/
│   │   ├── api/                # API封装
│   │   ├── views/              # 页面组件
│   │   └── router/             # 路由配置
│   ├── package.json
│   └── vite.config.js
└── TRJC-h5/                    # H5移动端
    ├── src/
    │   ├── views/              # 页面组件
    │   └── router/             # 路由配置
    ├── package.json
    └── vite.config.js
```

## 数据库设计

系统使用MySQL数据库，主要表结构如下：

| 表名 | 说明 |
|------|------|
| person_info | 人员信息表 |
| plot_info | 地块信息表 |
| task_info | 任务信息表 |
| task_plot | 任务地块关联表 |
| task_assign | 任务分配表 |
| survey_record | 勘察记录表 |
| sample_record | 样品采集记录表 |
| farmland_dataset | 耕地质量数据集表 |

详细设计请参考 `database-design.md`

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- MySQL 5.7+

### 后端启动

```bash
# 进入后端目录
cd TRJC-backend

# 创建虚拟环境（可选）
python -m venv venv
# Windows激活
venv\Scripts\activate
# Linux/Mac激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 编辑 .env 文件，配置数据库连接等信息

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 查看API文档

### 前端启动 (PC端)

```bash
cd TRJC-web

# 安装依赖
npm install

# 启动开发服务
npm run dev
```

访问 http://localhost:3000

### 前端启动 (H5端)

```bash
cd TRJC-h5

# 安装依赖
npm install

# 启动开发服务
npm run dev
```

访问 http://localhost:5173

## 安全特性

- JWT Token认证
- 敏感数据（姓名、联系方式）AES加密存储
- 前端脱敏显示
- CORS跨域控制
- 软删除机制

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 默认账号

系统内置测试账号：

| 姓名 | 手机号 | 密码 |
|------|--------|------|
| 张三 | 13800138001 | 123456 |

## 配置说明

后端配置文件 `TRJC-backend/.env` 示例：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=trjc_db

ENCRYPTION_KEY=your-32-byte-encryption-key-here!!

JWT_SECRET_KEY=trjc-secret-key-change-in-production-2024
JWT_ALGORITHM=HS256
JWT_EXPIRE_SECONDS=86400
```

## 开发规范

- 数据库字段命名：中文拼音首字母大写（如姓名 → XM）
- 软删除：所有表包含 SFSC 字段，默认查询 SFSC=0
- 接口返回格式统一：`{"code": 200, "msg": "", "data": {}}`
- 敏感数据（姓名、联系方式、密码）必须加密存储
- 前端样式复用现有 CSS 类名，保持 UI 一致性

## 参考资料

管理类模块开发请参考：[管理类模块开发指南.md](./管理类模块开发指南.md)

## 许可证

[项目许可证信息]
