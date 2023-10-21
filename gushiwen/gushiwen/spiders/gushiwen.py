import os
import io
import re
import scrapy

def strip_text(text_list):
    result = []
    for t in text_list:
        if not t=='\n':
            result.append(t.strip())
    return '\n'.join(result)

def write_article_org_file(group_name, title, author, dynasty, text):
    content = f'''* {title} #card #诗词 #古文
** {author} {dynasty}
** {text}
    '''
    folder = f'articles/{group_name}'
    if not os.path.exists(folder): os.makedirs(folder) 
    with io.open(f'{folder}/{title}.org','w',encoding='utf8') as f:
        f.write(content)

class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    start_urls = ['https://so.gushiwen.cn/gushi/chuzhong.aspx']

    def parse(self, response):
        groups = response.css('div.main3 div.left div.sons div.typecont')
        for group in groups:
            # group = response.css('div.main3 div.left div.sons div.typecont')[0]
            group_name = group.css('div.bookMl strong::text').get()
            yield from response.follow_all(group.css('span a'), callback=self.parse_article, cb_kwargs={'group_name':group_name})

    def parse_article(self, response, group_name):
        content = response.css('div.main3 .left div#sonsyuanwen.sons div.cont')
        title = content.css('h1::text').get().strip()
        author = content.css('div p.source')
        author = strip_text( author.css('a:nth-child(1)::text').getall() )
        dynasty = re.sub(r'〔|〕', '', strip_text( content.css('a:nth-child(2)::text').getall()))
        text = strip_text( content.css('div.contson::text').getall() + content.css('div.contson p::text').getall() )

        self.log(f'Writing org file of {title}')
        write_article_org_file(group_name, title, author, dynasty, text)

        article = {
            'title' : title,
            'author' : author,
            'dynasty': dynasty,
            'text' : text
        }
        yield article
