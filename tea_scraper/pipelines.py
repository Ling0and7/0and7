# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import hashlib
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class TeaMysqlPipeline:
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password, mysql_port=3306):
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_port = mysql_port
        self.connection = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST', 'localhost'),
            mysql_db=crawler.settings.get('MYSQL_DBNAME', 'tea_research_db'),
            mysql_user=crawler.settings.get('MYSQL_USER', 'root'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD', 'your_password'),
            mysql_port=crawler.settings.get('MYSQL_PORT', 3306),
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host=self.mysql_host,
            db=self.mysql_db,
            user=self.mysql_user,
            password=self.mysql_password,
            port=self.mysql_port,
            charset='utf8mb4',
            autocommit=True
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get('title', '')
        publish_date = adapter.get('publication_date')
        abstract = adapter.get('abstract', '')
        url = adapter.get('url', '')
        authors = adapter.get('authors', [])  # 列表

        if not title or not url:
            raise DropItem(f"Missing title or url: {item}")

        # 计算 content_hash (title + abstract 的 MD5)
        content_str = (title + abstract).encode('utf-8')
        content_hash = hashlib.md5(content_str).hexdigest()

        try:
            # 插入/检查 papers（使用 INSERT IGNORE 利用 UNIQUE 约束去重）
            self.cursor.execute("""
                INSERT IGNORE INTO papers (title, publish_date, abstract, url, content_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, publish_date, abstract, url, content_hash))
            paper_id = self.cursor.lastrowid  # 如果插入成功，获取 ID；否则为 0

            if paper_id == 0:
                # 已存在，查询 ID
                self.cursor.execute("SELECT id FROM papers WHERE url = %s OR content_hash = %s LIMIT 1", (url, content_hash))
                result = self.cursor.fetchone()
                if result:
                    paper_id = result[0]
                else:
                    raise DropItem(f"Duplicate but no ID found: {url}")

            # 插入 authors 和 paper_authors
            for ord_idx, author_name in enumerate(authors, start=1):
                # 插入/检查 author
                self.cursor.execute("INSERT IGNORE INTO authors (name) VALUES (%s)", (author_name,))
                author_id = self.cursor.lastrowid
                if author_id == 0:
                    self.cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
                    result = self.cursor.fetchone()
                    if result:
                        author_id = result[0]
                    else:
                        raise DropItem(f"Author insert failed: {author_name}")

                # 插入 paper_authors（忽略重复）
                self.cursor.execute("""
                    INSERT IGNORE INTO paper_authors (paper_id, author_id, ord)
                    VALUES (%s, %s, %s)
                """, (paper_id, author_id, ord_idx))

            spider.logger.info(f"Inserted paper: {title[:50]}... (ID: {paper_id})")
            return item

        except Exception as e:
            spider.logger.error(f"DB insert error: {e}")
            raise DropItem(f"DB error: {e}")

# 其他默认 Pipeline（可选）
class TeaScraperPipeline:
    def process_item(self, item, spider):
        return item