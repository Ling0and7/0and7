
创建代码：cd tea_scraper

 		scrapy crawl tea_research -o output.json



tea_scraper/          # 项目根目录

├── scrapy.cfg        # 配置文件（文本文件）

└── tea_scraper/      # 子文件夹（项目包）

    ├── __init__.py   # 空文件（Python 模块）

    ├── items.py      # 空文件

    ├── middlewares.py# 空文件

    ├── pipelines.py  # 空文件

    ├── settings.py   # 设置文件

    └── spiders/      # 子文件夹

        ├── __init__.py  # 空文件

        └── tea_research_spider.py  # 您的蜘蛛代码文件


清空数据库代码：
USE tea_research_db;
TRUNCATE TABLE paper_authors;  -- 清空关联表
TRUNCATE TABLE authors;        -- 清空作者表
TRUNCATE TABLE papers;         -- 清空论文表（重置计数）

各个脚本的作用注释：
export.py：用于从 MySQL 数据库 (tea_research_db) 导出论文数据到 CSV。脚本使用 pymysql 连接数据库、pandas 处理数据和导出 CSV。


*************************************************运行该项目操作（有demo版）****************************************************************

步骤1：打开终端，登录数据库，代码为：mysql -u root -p       输入密码

步骤2：根据自己的路径调整并输入这个代码：
 	例：	SOURCE C:/Users/用户名/Desktop/tea_scraper/create_tables.sql;


步骤3：创建完成以后验证代码 ：

SHOW DATABASES;  -- 检查数据库列表，应有 tea_research_db

USE tea_research_db;

SHOW TABLES;     -- 检查表列表，应有 papers, authors, paper_authors

DESCRIBE papers; -- 查看 papers 表结构（字段、索引）


步骤4：退出mysql，代码为：EXIT;   

步骤5：一键运行脚本代码：
cd C:\Users\用户名\Desktop\tea_scraper
python demo/run_demo.py
