import pymysql
conn = pymysql.connect(host='localhost', user='root', password='your_password', db='tea_research_db', charset='utf8mb4')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM papers")
print(f"论文总数: {cursor.fetchone()[0]}")
cursor.close()
conn.close()