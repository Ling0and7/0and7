import os
import subprocess
import datetime
import shutil
from pathlib import Path

# 项目根目录（当前脚本所在 tea_scraper）
PROJECT_ROOT = Path(__file__).parent.parent

def run_scrapy():
    """运行 Scrapy 爬取，保存日志和 items.jl"""
    log_file = PROJECT_ROOT / "scrapy.log"
    items_file = PROJECT_ROOT / "items.jl"
    cmd = ["scrapy", "crawl", "tea_research", "-L", "INFO", "-o", str(items_file)]
    with open(log_file, "w") as f:
        subprocess.run(cmd, cwd=PROJECT_ROOT, stdout=f, stderr=subprocess.STDOUT, check=True)
    print("Scrapy 爬取完成，日志保存到 scrapy.log")

def run_export(output_file, **kwargs):
    """运行 export.py 生成 CSV"""
    cmd = ["python", "export.py", "--output", output_file]
    for k, v in kwargs.items():
        if v:
            cmd.extend([f"--{k}", str(v)])
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
    print(f"导出完成: {output_file}")

def run_validation():
    """运行 SQL 验证，保存到 validation.txt"""
    import pymysql  # 直接导入，避免依赖
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '0000',  # 与 export.py 一致，替换为实际密码
        'database': 'tea_research_db',
        'charset': 'utf8mb4'
    }
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    validation_queries = [
        "SELECT COUNT(*) AS total FROM papers;",
        "SELECT COUNT(*) AS tea_matches FROM papers WHERE title LIKE '%tea%' OR abstract LIKE '%tea%';",
        "SELECT COUNT(*) AS pests_matches FROM papers WHERE title LIKE '%pest%' OR title LIKE '%disease%' OR abstract LIKE '%pest%' OR abstract LIKE '%disease%';"
    ]
    
    with open(PROJECT_ROOT / "validation.txt", "w", encoding='utf-8') as f:
        f.write("=== SQL 验证输出 ===\n")
        f.write(f"执行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for query in validation_queries:
            cursor.execute(query)
            result = cursor.fetchone()[0]
            query_name = query.split(' AS ')[-1].strip('; ')
            f.write(f"{query_name}: {result}\n")
            print(f"{query_name}: {result}")
    
    cursor.close()
    conn.close()
    print("SQL 验证完成，保存到 validation.txt")

def main():
    # 生成时间戳目录
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    output_dir = PROJECT_ROOT / f"outputs/{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"创建输出目录: {output_dir}")

    # 临时文件路径
    temp_files = [
        "scrapy.log",
        "items.jl",
        "final.csv",
        "validation.txt",
        "tea.csv",
        "pests.csv"
    ]

    try:
        # 1. 运行 Scrapy
        run_scrapy()

        # 2. 运行 SQL 验证
        run_validation()

        # 3. 导出全量 (final.csv)
        run_export("final.csv")

        # 4. 导出主题 CSV
        run_export("tea.csv", keyword="tea")
        run_export("pests.csv", keyword="pests")

        # 5. 移动文件到输出目录
        for file in temp_files:
            src = PROJECT_ROOT / file
            if src.exists():
                shutil.move(str(src), str(output_dir / file))
                print(f"移动 {file} 到 {output_dir}")

        print(f"\n演示完成！所有文件在: {output_dir}")
        print("文件列表: scrapy.log, items.jl, final.csv, validation.txt, tea.csv, pests.csv")

    except subprocess.CalledProcessError as e:
        print(f"子进程错误: {e}")
    except Exception as e:
        print(f"运行错误: {e}")

if __name__ == "__main__":
    main()