import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',  # 替换为您的实际密码
    'database': 'tea_research_db',
    'charset': 'utf8mb4'
}

try:
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM papers")
    count = cursor.fetchone()[0]
    print(f"连接成功！论文总数: {count}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"连接失败: {e}")