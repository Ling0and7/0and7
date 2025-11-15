-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS tea_research_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tea_research_db;

-- 表1: papers（论文表）
CREATE TABLE IF NOT EXISTS papers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(1000) NOT NULL,
    publish_date INT NOT NULL COMMENT '出版年份 (YYYY)',
    abstract TEXT,
    url VARCHAR(500) UNIQUE NOT NULL COMMENT 'DOI 或 OpenAlex URL',
    content_hash VARCHAR(32) UNIQUE NOT NULL COMMENT 'MD5 哈希 (title + abstract)',
    INDEX idx_date (publish_date),
    FULLTEXT INDEX idx_title (title(128))  -- 前缀 128 字符的全文索引（MySQL 8.0+ 支持）
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='论文信息表';

-- 表2: authors（作者表）
CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='作者表';

-- 表3: paper_authors（论文-作者关联表）
CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id INT NOT NULL,
    author_id INT NOT NULL,
    ord INT NOT NULL COMMENT '作者顺序 (1=第一作者)',
    PRIMARY KEY (paper_id, author_id),
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='论文-作者多对多关系表';