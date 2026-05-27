from sqlalchemy import Column, Integer, String, DECIMAL, Date, DateTime, JSON, Text, func, BigInteger
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base


class PersonInfo(Base):
    __tablename__ = "person_info"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    XM = Column(String(200), comment="姓名-加密存储")
    LXFS = Column(String(200), comment="联系方式-加密存储")
    MM = Column(String(200), comment="密码-bcrypt加密存储")
    GW = Column(String(20), comment="岗位")
    SSQH = Column(String(50), comment="所属区划")
    SSBM = Column(String(50), comment="所属部门")
    RYZT = Column(String(20), default="active", comment="人员状态")
    CJSJ = Column(DateTime, server_default=func.now(), comment="创建时间")
    SFSC = Column(TINYINT, default=0, comment="是否删除：0-未删除，1-已删除")


class PlotInfo(Base):
    __tablename__ = "plot_info"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    TBH = Column(String(50), comment="图斑编号")
    SSDY = Column(String(50), comment="所属单元")
    TBMJ = Column(DECIMAL(10, 2), comment="图斑面积")
    SSQH = Column(String(50), comment="所属区划")
    JD = Column(DECIMAL(10, 6), comment="经度")
    WD = Column(DECIMAL(10, 6), comment="纬度")
    WLZB = Column(JSON, comment="围栏坐标")
    CJR = Column(Integer, comment="创建人ID")
    CJSJ = Column(DateTime, server_default=func.now(), comment="创建时间")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class TaskInfo(Base):
    __tablename__ = "task_info"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWBH = Column(String(50), unique=True, comment="任务编号")
    RWMC = Column(String(200), comment="任务名称")
    RWLX = Column(String(20), comment="任务类型")
    SSQH = Column(String(50), comment="所属区划")
    FZR = Column(String(50), comment="负责人")
    JHKSSJ = Column(String(50), comment="计划开始时间")
    LXDH = Column(String(50), comment="联系电话")
    RWMS = Column(Text, comment="任务描述")
    ZT = Column(String(20), default="draft", comment="状态")
    CJSJ = Column(DateTime, server_default=func.now(), comment="创建时间")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class TaskPlot(Base):
    __tablename__ = "task_plot"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class TaskPlotStatus(Base):
    __tablename__ = "task_plot_status"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    ZT = Column(String(20), default="pending", comment="状态：pending-待领取, sampling-待采样, transport-待运输, analysis-待分析, completed-已完成")
    KCFSJ = Column(DateTime, comment="勘察完成时间")
    CYFSJ = Column(DateTime, comment="采样完成时间")
    CJSJ = Column(DateTime, server_default=func.now(), comment="创建时间")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class TaskAssign(Base):
    __tablename__ = "task_assign"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    RYID = Column(Integer, comment="人员ID")
    FPSJ = Column(DateTime, server_default=func.now(), comment="分配时间")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class TaskAttachment(Base):
    __tablename__ = "task_attachment"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    FILE_NAME = Column(String(255), comment="原始文件名")
    FILE_PATH = Column(String(500), comment="存储路径")
    FILE_SIZE = Column(BigInteger, comment="文件大小(字节)")
    FILE_TYPE = Column(String(50), comment="文件类型")
    CJSJ = Column(DateTime, server_default=func.now(), comment="创建时间")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class SurveyRecord(Base):
    __tablename__ = "survey_record"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    XMMC = Column(String(200), comment="项目名称")
    TBH = Column(String(50), comment="图斑编号")
    MJ = Column(DECIMAL(10, 2), comment="面积")
    DLWZ = Column(String(200), comment="地理位置")
    DLZB_JD = Column("DLZB-JD", String(50), comment="地理坐标-经度")
    DLZB_WD = Column("DLZB-WD", String(50), comment="地理坐标-纬度")
    BGQ = Column(String(50), comment="变更前土地利用类型")
    BGSJ = Column(String(20), comment="变更时间")
    LYLX = Column(String(50), comment="利用类型")
    YXTCHD = Column(DECIMAL(5, 2), comment="有效土层厚度")
    QRLXJHL = Column(String(50), comment="侵入体类型及含量")
    LSHL = Column(DECIMAL(5, 2), comment="砾石含量")
    DXPD = Column(DECIMAL(5, 2), comment="地形坡度")
    TMPZCD = Column(String(20), comment="田面平整程度")
    SZBZTJ = Column(String(20), comment="水资源保障条件")
    DLTXTJ = Column(String(20), comment="道路通行条件")
    DXBW = Column(String(50), comment="地形部位")
    ZDGX = Column(String(50), comment="质地构型")
    PSNL = Column(String(20), comment="排水能力")
    HBGD = Column(DECIMAL(8, 2), comment="海拔高度")
    NTFH = Column(String(20), comment="农田防护与生态环境保护水平")
    GCHD = Column(DECIMAL(5, 2), comment="耕层厚度")
    KCRQ = Column(Date, comment="勘察日期")
    DCRY = Column(String(50), comment="调查人员")
    XMDWDB = Column(String(50), comment="项目承担单位代表")
    TKZJ = Column(String(50), comment="踏勘专家")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class SampleRecord(Base):
    __tablename__ = "sample_record"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    TRHHYPBH = Column(String(50), comment="土壤混合样品编号")
    DLWZ = Column(String(200), comment="地理位置")
    DLZB_D1BH = Column("DLZB-D1BH", String(50), comment="地理坐标-点1编号")
    DLZB_D1JD = Column("DLZB-D1JD", String(50), comment="地理坐标-点1经度")
    DLZB_D1WD = Column("DLZB-D1WD", String(50), comment="地理坐标-点1纬度")
    DLZB_D2BH = Column("DLZB-D2BH", String(50), comment="地理坐标-点2编号")
    DLZB_D2JD = Column("DLZB-D2JD", String(50), comment="地理坐标-点2经度")
    DLZB_D2WD = Column("DLZB-D2WD", String(50), comment="地理坐标-点2纬度")
    DLZB_D3BH = Column("DLZB-D3BH", String(50), comment="地理坐标-点3编号")
    DLZB_D3JD = Column("DLZB-D3JD", String(50), comment="地理坐标-点3经度")
    DLZB_D3WD = Column("DLZB-D3WD", String(50), comment="地理坐标-点3纬度")
    CYSD_D1 = Column("CYSD-D1", String(50), comment="采样深度-点1")
    CYSD_D2 = Column("CYSD-D2", String(50), comment="采样深度-点2")
    CYSD_D3 = Column("CYSD-D3", String(50), comment="采样深度-点3")
    CYDWSL = Column(Integer, comment="采样点位数量")
    HHYPSL = Column(DECIMAL(8, 2), comment="混合样品重量")
    CYRQ = Column(Date, comment="采样日期")
    CYRY = Column(String(50), comment="采样人员")
    XMDWDB = Column(String(50), comment="项目承担单位代表")
    TKZJ = Column(String(50), comment="踏勘专家")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class FarmlandDataset(Base):
    __tablename__ = "farmland_dataset"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    RWMC = Column(String(200), comment="任务名称")
    TBH = Column(String(50), comment="图斑编号")
    JD = Column(DECIMAL(10, 6), comment="经度")
    WD = Column(DECIMAL(10, 6), comment="纬度")
    CYRQ = Column(Date, comment="采样日期")
    DXBW = Column(String(50), comment="地形部位")
    YXTCHD = Column(DECIMAL(5, 2), comment="有效土层厚度")
    GCZD = Column(String(50), comment="耕层质地")
    RZ = Column(DECIMAL(5, 2), comment="容重")
    ZDGX = Column(String(50), comment="质地构型")
    SWDYX = Column(String(20), comment="生物多样性")
    NTLW = Column(String(20), comment="农田林网化程度")
    ZAYS = Column(String(50), comment="障碍因素")
    GGNL = Column(String(20), comment="灌溉能力")
    PSNL = Column(String(20), comment="排水能力")
    PHZ = Column(DECIMAL(4, 2), comment="pH值")
    YJZ = Column(DECIMAL(8, 2), comment="有机质")
    YXL = Column(DECIMAL(8, 2), comment="有效磷")
    SXJ = Column(DECIMAL(8, 2), comment="速效钾")
    SRXYLZL = Column(DECIMAL(8, 2), comment="水溶性盐总量")
    DLMC = Column(String(50), comment="地类名称")
    JQCD = Column(String(20), comment="清洁程度")
    BZ = Column(String(500), comment="备注")
    GD = Column(DECIMAL(8, 3), comment="镉")
    ZG = Column(DECIMAL(8, 3), comment="总汞")
    ZS = Column(DECIMAL(8, 2), comment="总砷")
    Q = Column(DECIMAL(8, 2), comment="铅")
    G = Column(DECIMAL(8, 2), comment="铬")
    GDZLDJ = Column(DECIMAL(10, 6), comment="耕地质量等级")
    ZLFJ = Column(String(20), comment="质量分级")
    SFSC = Column(TINYINT, default=0, comment="是否删除")


class AnalysisResult(Base):
    __tablename__ = "analysis_result"

    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    RWID = Column(Integer, comment="任务ID")
    DKID = Column(Integer, comment="地块ID")
    RZ = Column(DECIMAL(5, 2), comment="容重")
    PHZ = Column(DECIMAL(4, 2), comment="pH值")
    YJZ = Column(DECIMAL(8, 2), comment="有机质")
    YXP = Column(DECIMAL(8, 2), comment="有效磷")
    XJK = Column(DECIMAL(8, 2), comment="速效钾")
    SRXYLZL = Column(DECIMAL(8, 2), comment="水溶性盐总量")
    GE = Column(DECIMAL(8, 3), comment="镉")
    ZG = Column(DECIMAL(8, 3), comment="总汞")
    ZS = Column(DECIMAL(8, 2), comment="总砷")
    QIAN = Column(DECIMAL(8, 2), comment="铅")
    GE_CHROME = Column(DECIMAL(8, 2), comment="铬")
    SFSC = Column(TINYINT, default=0, comment="是否删除")
