import re
import scrapy

def strip_text(text_list):
    result = []
    for t in text_list:
        if not t=='\n':
            result.append(t.strip())
    return '\n'.join(result)

class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    start_urls = ['https://so.gushiwen.cn/gushi/chuzhong.aspx']

    def parse(self, response):
        seven_first = response.css('div.main3 div.left div.sons div.typecont')[0]
        yield from response.follow_all(seven_first.css('span a'), callback=self.parse_article)

    def parse_article(self, response):
        content = response.css('div.main3 .left div#sonsyuanwen.sons div.cont')
        title = content.css('h1::text').get().strip()
        author = content.css('div p.source')
        author_name = strip_text( author.css('a:nth-child(1)::text').getall() )
        author_dynasty = strip_text( content.css('a:nth-child(2)::text').getall() )
        text = strip_text( content.css('div.contson::text').getall() + content.css('div.contson p::text').getall() )
        article = {
            'title' : title,
            'author_name' : author_name,
            'author_dynasty': re.sub(r'〔|〕', '', author_dynasty),
            'text' : text
        }
        yield article
