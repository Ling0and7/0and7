import scrapy
from scrapy.http import JsonRequest
from tea_scraper.items import TeaResearchItem

class TeaResearchSpider(scrapy.Spider):
    name = 'tea_research'
    allowed_domains = ['api.openalex.org']

    def start_requests(self):
        # 宽松 OR 查询：去掉引号，增加变体，预计 500+ 条
        search_query = 'tea (pests OR diseases OR spread OR diffusion OR UAV OR drone OR "remote sensing" OR hyperspectral OR multispectral OR "visible light" OR "deep learning" OR "object detection" OR "semantic segmentation" OR "large language model" OR LLM OR multimodal)'
        encoded_search = search_query.replace(' ', '%20')
        base_url = f"https://api.openalex.org/works?search={encoded_search}&per-page=100"
        yield JsonRequest(url=base_url, callback=self.parse)
        
    def parse(self, response):
        data = response.json()
        meta = data.get('meta', {})

        # 解析每篇论文
        for work in data.get('results', []):
            authorships = work.get('authorships', [])
            authors = []
            for auth in sorted(authorships, key=lambda x: x.get('author_position', 999)):
                author_name = auth.get('author', {}).get('display_name', '')
                if author_name:
                    authors.append(author_name)
            
            item = TeaResearchItem()
            item['title'] = work.get('title', '')
            item['authors'] = authors
            item['publication_date'] = work.get('publication_year')
            item['abstract'] = work.get('abstract', '')
            item['url'] = f"https://doi.org/{work.get('doi')}" if work.get('doi') else work.get('id', '').replace('https://openalex.org/', 'https://openalex.org/')
            yield item

            # 打印标题检查相关性（可选，生产环境可移除）
            self.logger.info(f"Scraped title: {item['title'][:100]}...")

        # 分页
        next_cursor = meta.get('next_cursor')
        if next_cursor:
            search_part = response.url.split('?search=')[1].split('&')[0] if '?search=' in response.url else ''
            next_url = f"https://api.openalex.org/works?search={search_part}&cursor={next_cursor}&per-page=100"  # &filter=publication_year:>=2015
            yield JsonRequest(url=next_url, callback=self.parse)

        # 日志
        total_count = meta.get('count', 0)
        page_results = len(data.get('results', []))
        self.logger.info(f"Processed page: {page_results} items, total available: {total_count}")