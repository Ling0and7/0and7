# 机器人协议和延迟（遵守 OpenAlex 速率限制）
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1.0  # 1秒延迟

# 输出管道：保存为 JSON
FEEDS = {
    'output.json': {'format': 'json'},
}

# 用户代理（可选）
USER_AGENT = 'TeaResearchBot/1.0'