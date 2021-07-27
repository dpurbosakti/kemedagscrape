import scrapy


class PostSpider(scrapy.Spider):
    name = "kemend"
    allowed_urls = ['http://djpen.kemedag.po.go.id']
    start_urls = ['http://djpen.kemendag.go.id/app_frontend/imp_profiles/view/{page}'.format(page=i)
                  for i in range(1, 1000)]

    def parse(self, response):

        for post in response.css('div.left.grid_9'):
            test_ambil = post.css('h1::text').get()
            if test_ambil is None:
                scrapy.Request(callback=self.parse)

            else:
                adr = post.css('.detail p::text')[0:2].getall()
                adr = ''.join(adr)
                adr = adr.replace(' ','')
                adr = adr.replace('\n','')
                adr = adr.replace('\t','')
                item = {
                    "page": response.url[59:],
                    "title": post.css('h1::text').get(),
                    "address": adr,
                    "phone": post.css('.detail p::text')[2].get().strip(),
                    "fax": post.css('.detail p::text')[3].get().strip(),
                    "email": post.css('.detail p::text')[5].get().strip(),
                    "website": post.css('.detail p a::text').get(),
                    "contact": post.css('.detail ul li::text').get(),
                    "product": post.css('.detail ul li::text')[1:].getall()
                }

                yield item
