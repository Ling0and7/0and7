import pymysql
import pandas as pd
import argparse
from datetime import datetime

# MySQL 配置（修改为您的实际值）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',  # 替换为您的密码
    'database': 'tea_research_db',
    'charset': 'utf8mb4'
}

def query_papers(latest_n=None, date_from=None, date_to=None, keyword=None):
    """查询论文数据，支持过滤"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 基础 SELECT + FROM + JOIN
    select_part = """
    SELECT 
        p.title,
        GROUP_CONCAT(a.name ORDER BY pa.ord SEPARATOR ', ') AS authors,
        p.publish_date,
        p.abstract,
        p.url
    FROM papers p
    LEFT JOIN paper_authors pa ON p.id = pa.paper_id
    LEFT JOIN authors a ON pa.author_id = a.id
    """

    # WHERE 条件
    conditions = []
    params = []
    if date_from:
        conditions.append("p.publish_date >= %s")
        params.append(int(date_from))
    if date_to:
        conditions.append("p.publish_date <= %s")
        params.append(int(date_to))
    if keyword:
        conditions.append("(p.title LIKE %s OR p.abstract LIKE %s)")
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # GROUP BY + ORDER BY + LIMIT
    group_order = " GROUP BY p.id ORDER BY p.id DESC"
    if latest_n:
        group_order += f" LIMIT {latest_n}"

    # 完整 SQL
    full_sql = select_part + where_clause + group_order

    # 打印 SQL 调试（可选，生产时注释掉）
    print(f"执行 SQL: {full_sql}")
    print(f"参数: {params}")

    # 执行查询
    cursor.execute(full_sql, params)
    results = cursor.fetchall()
    columns = ['title', 'authors', 'publish_date', 'abstract', 'url']

    cursor.close()
    conn.close()

    return pd.DataFrame(results, columns=columns)

def export_to_csv(df, filename):
    """导出到 CSV，支持中文无乱码"""
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"导出完成：{filename} ({len(df)} 条记录)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="导出论文数据到 CSV")
    parser.add_argument('--all', action='store_true', help='全量导出（默认）')
    parser.add_argument('--latest', type=int, help='导出最新 N 条')
    parser.add_argument('--date-from', type=int, help='日期范围起始年份 (YYYY)')
    parser.add_argument('--date-to', type=int, help='日期范围结束年份 (YYYY)')
    parser.add_argument('--keyword', type=str, help='关键词过滤 (title 或 abstract 中搜索)')
    parser.add_argument('--output', type=str, default='papers_export.csv', help='输出文件名 (默认: papers_export.csv)')

    args = parser.parse_args()

    # 验证参数互斥：全量优先
    if args.latest and (args.date_from or args.date_to or args.keyword):
        print("警告：--latest 与其他过滤互斥，使用 --latest。")
        df = query_papers(latest_n=args.latest)
    elif args.keyword or args.date_from or args.date_to:
        df = query_papers(latest_n=args.latest, date_from=args.date_from, date_to=args.date_to, keyword=args.keyword)
    else:
        df = query_papers()  # 全量

    if df.empty:
        print("无匹配数据！")
    else:
        export_to_csv(df, args.output)