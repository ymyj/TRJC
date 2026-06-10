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
- **UI组件库**: Element Plus
- **路由**: Vue Router 4
- **HTTP客户端**: Axios

### 前端 (H5移动端)
- **框架**: Vue.js 3
- **UI组件库**: Vant 4
- **状态管理**: Pinia
- **构建工具**: Vite 5
- **语言**: TypeScript

## 功能模块

### 1. 认证模块
- 用户登录/登出
- JWT Token 认证与刷新

### 2. 任务管理
- 任务发布（关联地块、人员）
- 任务列表查询
- 任务分配
- 任务详情查看
- 任务地块管理

### 3. 人员管理
- 人员信息维护
- 敏感数据加密存储
- 前端脱敏显示

### 4. 地块管理
- 地块信息录入
- 地理坐标管理
- 围栏坐标管理

### 5. 勘察记录
- 勘察信息填写
- 关联任务和地块

### 6. 样品采集
- 土壤混合样品管理
- 采样点位记录
- 批量提交样品

### 7. 数据分析
- 数据统计与分析

### 8. 耕地质量数据集
- 数据聚合展示（33个业务字段）
- 耕地质量等级计算
- 质量分级

## 项目结构

```
TRJC/
├── README.md
├── TRJC-backend/               # 后端项目
│   ├── app/
│   │   ├── api/                # API路由
│   │   │   ├── auth.py         # 认证相关
│   │   │   ├── tasks.py        # 任务管理
│   │   │   ├── task_plots.py   # 任务地块管理
│   │   │   ├── personnel.py    # 人员管理
│   │   │   ├── plots.py        # 地块管理
│   │   │   ├── survey.py       # 勘察记录
│   │   │   ├── samples.py      # 样品采集
│   │   │   ├── analysis.py     # 数据分析
│   │   │   └── datasets.py     # 数据集
│   │   ├── middleware/
│   │   │   └── auth.py         # 认证中间件
│   │   ├── models/             # 数据模型
│   │   ├── schemas/            # 数据验证
│   │   ├── services/           # 业务逻辑
│   │   ├── utils/              # 工具类
│   │   │   ├── crypto.py       # 加密解密
│   │   │   ├── code_generator.py
│   │   │   ├── dataset_helper.py
│   │   │   └── task_helper.py
│   │   ├── config.py           # 配置
│   │   ├── database.py         # 数据库连接
│   │   └── main.py             # 入口
│   ├── uploads/                # 文件上传目录
│   └── requirements.txt
├── TRJC-web/                   # PC端前端
│   ├── src/
│   │   ├── api/                # API封装
│   │   ├── components/         # 公共组件
│   │   ├── views/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   └── styles/             # 全局样式
│   ├── package.json
│   └── vite.config.js
└── TRJC-h5/                    # H5移动端
    ├── src/
    │   ├── api/                # API封装
    │   ├── components/         # 公共组件
    │   ├── views/              # 页面组件
    │   ├── store/              # 状态管理
    │   └── styles/             # 全局样式
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

后端API统一使用 `/trjcai` 前缀，例如：`http://localhost:8000/trjcai/login`

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

## 角色与权限

系统基于岗位（GW字段）进行角色划分和权限控制：

| 岗位 | 登录端 | 数据权限 | 说明 |
|------|--------|----------|------|
| 超管 | Web + H5 | 全部数据 | 最高权限，查看所有公司数据 |
| 管理员 | Web + H5 | 本公司数据 | 企业管理员，仅查看所属公司数据 |
| 项目经理 | Web + H5 | - | 项目管理相关 |
| 其他岗位 | 仅 H5 | - | 仅可通过移动端登录 |

**登录权限控制：**
- 非超管/管理员/项目经理岗位尝试登录 Web 端将被拒绝
- 登录时通过 `X-Login-Source` 请求头判断登录来源（web/h5）

**Token 信息：**
- JWT 中包含用户 ID、公司（GS）、岗位（GW）信息
- 返回数据中 `isAdmin` 字段标识是否为超管或管理员

## 安全特性

- JWT Token认证（支持Token刷新机制，有效期24小时，刷新有效期7天）
- Token 中携带用户角色和公司信息，用于接口级权限控制
- 认证中间件统一鉴权（白名单机制，支持 `/trjcai` 前缀）
- 敏感数据（姓名、联系方式）使用 Fernet（AES）加密存储
- 密码使用 bcrypt 哈希存储
- 手机号登录时采用解密后匹配方式
- 前端脱敏显示（姓名：`张**`，手机：`138****8001`）
- CORS跨域控制
- 软删除机制

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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
JWT_REFRESH_EXPIRE_SECONDS=604800
```

## 开发规范

- 数据库字段命名：中文拼音首字母大写（如姓名 → XM）
- 软删除：所有表包含 SFSC 字段，默认查询 SFSC=0
- 接口返回格式统一：`{"code": 200, "msg": "", "data": {}}`
- 敏感数据（姓名、联系方式、密码）必须加密存储
- 前端样式复用现有 CSS 类名，保持 UI 一致性

## 许可证

[项目许可证信息]
