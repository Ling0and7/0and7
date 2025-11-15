



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





具体操作：

步骤1：打开终端，登录数据库，代码为：mysql -u root -p       输入密码



步骤2：根据自己的路径调整并输入这个代码：

 	例：	SOURCE C:/Users/93478/Desktop/tea_scraper/create_tables.sql;



步骤3：创建完成以后验证代码 ：

SHOW DATABASES;  -- 检查数据库列表，应有 tea_research_db

USE tea_research_db;

SHOW TABLES;     -- 检查表列表，应有 papers, authors, paper_authors

DESCRIBE papers; -- 查看 papers 表结构（字段、索引）



步骤4：退出mysql，代码为：EXIT;        
        注：在 tea_scraper/settings.py 末尾中，MYSQL_PASSWORD = '0000'  # 您的密码
                这一句里面的0000改为自己的密码

步骤5：切换到项目目录，代码为：cd C:\Users\93478\Desktop\tea_scraper

步骤6：验证配置，代码为：scrapy list     #预期输出为tea_research。如果无，检查 spiders 文件。

步骤7：执行爬取，代码为：scrapy crawl tea_research -L INFO

步骤8：重新连接数据库，打开终端，登录数据库，代码为：mysql -u root -p       输入密码
       输入代码：USE tea_research_db;

步骤9：运行验证查询，总计的代码为：
SELECT COUNT(*) AS paper_count FROM papers;
SELECT COUNT(*) AS author_count FROM authors;
SELECT COUNT(*) AS relation_count FROM paper_authors;
示例数据的代码（前5篇）为：
SELECT p.id, p.title, p.publish_date, p.url,
       GROUP_CONCAT(a.name ORDER BY pa.ord SEPARATOR ', ') AS authors_list
FROM papers p
LEFT JOIN paper_authors pa ON p.id = pa.paper_id
LEFT JOIN authors a ON pa.author_id = a.id
GROUP BY p.id, p.title, p.publish_date, p.url
ORDER BY p.id
LIMIT 5;

步骤10：退出mysql，代码为：EXIT;  

步骤11：运行export.py文件进行全量导出，导出结果为papers_export.csv文件，代码为：
cd C:\Users\93478\Desktop\tea_scraper
python export.py

步骤12：运行export.py文件进行关键词导出，导出结果为关键词主题文件。
    以'tea'（茶叶）关键词，就会导出tea_theme.csv文件，代码为：python export.py --keyword "tea" --output tea_theme.csv
    以'pests'（病虫害）关键词，就会导出pests_theme.csv文件，代码为：python export.py --keyword "pests" --output pests_theme.csv