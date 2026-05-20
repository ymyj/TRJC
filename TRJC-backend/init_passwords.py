from sqlalchemy import text, Column, String
from app.database import engine, SessionLocal
from app.models import PersonInfo
from app.utils.crypto import hash_password

DEFAULT_PASSWORD = "123456"

def init_database():
    conn = engine.connect()
    try:
        conn.execute(text("""
            ALTER TABLE person_info 
            ADD COLUMN MM VARCHAR(200) COMMENT '密码-bcrypt加密存储' AFTER LXFS
        """))
        print("MM字段已添加")
    except Exception as e:
        if "Duplicate column name" in str(e):
            print("MM字段已存在，跳过")
        else:
            print(f"添加字段错误: {e}")
    finally:
        conn.close()

def init_passwords():
    db = SessionLocal()
    try:
        users = db.query(PersonInfo).filter(
            PersonInfo.SFSC == 0,
            PersonInfo.MM == None
        ).all()

        if users:
            hashed = hash_password(DEFAULT_PASSWORD)
            print(f"发现 {len(users)} 个用户需要初始化密码")
            for user in users:
                user.MM = hashed
            db.commit()
            print(f"已为 {len(users)} 个用户设置默认密码: {DEFAULT_PASSWORD}")
        else:
            print("没有需要初始化密码的用户")

        all_users = db.query(PersonInfo).filter(PersonInfo.SFSC == 0).all()
        print(f"\n人员列表 (可用手机号登录):")
        for u in all_users:
            from app.utils.crypto import decrypt_data
            print(f"  ID={u.ID}, 姓名={decrypt_data(u.XM)}, 手机={decrypt_data(u.LXFS)}, 密码={DEFAULT_PASSWORD}")

    except Exception as e:
        print(f"错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("数据库初始化脚本")
    print(f"默认密码: {DEFAULT_PASSWORD}")
    print("=" * 50)
    init_database()
    init_passwords()
    print("=" * 50)
    print("完成")
