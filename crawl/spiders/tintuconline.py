import scrapy

from ..items import NewscrawlerItem

class ThanhnienSpider(scrapy.Spider):
    name = "thanhnien"
    page_number = 2
    start_urls = ["https://thanhnien.vn/gioi-tre/"]

    def parse(self, response):

        all_div_news = response.css("div.relative article.story")

        for div in all_div_news:
            title = div.css("a.story__title::text").get()
            href = "https://thanhnien.vn/gioi-tre"+ div.css('a.story__title::attr(href)').get()
            sub_content = div.css("div.summary div::text").get()
            if href:
                request = scrapy.Request(url=href, callback=self.raw_content_parse)
                request.meta['title'] = title
                request.meta['sub_content'] = sub_content
                yield request

        next_page = "https://thanhnien.vn/gioi-tre/trang-" + str(ThanhnienSpider.page_number) +".html"
        if ThanhnienSpider.page_number <= 5:
            ThanhnienSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


    def raw_content_parse(self, response):
        title = response.meta.get('title')
        sub_content = response.meta.get('sub_content')
        href = response.url
        str = ''
        for raw_content in response.css("div.detail div::text").extract():
            str += raw_content
        items = NewscrawlerItem()
        items['title'] = title
        items['href'] = href
        items['sub_content'] = sub_content
        items['raw_content'] = str
        yield items