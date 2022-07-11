import scrapy
from tqdm import tqdm
from mgpSpider.items import MgpspiderItem 
import logging

# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
class BasicSpider(scrapy.Spider): 
       name = "basic" 
       #allowed_domains = ["web"] 
       # start_urls = ["https://www.genealogy.math.ndsu.nodak.edu/id.php?id=1" 
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=122738" 
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=53410"
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=60782"
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=93643"
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=125886"
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=283247"
       #        ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=129807"
       #        ]
       def start_requests(self):
           api = "https://www.mathgenealogy.org/id.php?id="
           min = 1
           max = 283247
           for self.i in tqdm(range(min,max+1, 1)):
              url = api + str(self.i)
              yield scrapy.Request(url, callback=self.parse)
                            # print("start\n") 

       def parse(self, response):
              # try:
              #        h1 = response.body.h1
              #        pass
              # except:
              #        logging.info("id %s doesn't exist" % self.i)
              #        yield None

              # print("start parsing\n")
              # perhaps define a raw item?
              item = MgpspiderItem()
              item['id'] = response.url.split("=")[-1]
              item['name'] = response.css("h2::text").extract()[0].strip()
              content = response.xpath('//*[@id="paddingWrapper"]')[0]
              item['mathscinet_id'] = content.xpath('.//a[text()="MathSciNet"]/@href').extract()
              #note the plural since there may have plural terms
              item['degree_years'] = content.xpath('./div/span[span[contains(@style,"color:\n  #006633")]]/text()').extract()[-1].strip()
              item['school_names'] = content.xpath('./div/span/span[contains(@style,"color:\n  #006633")]/text()').extract()
              item['school_countries'] = content.xpath('./div//img/@alt').extract()
              item['advisors'] = content.xpath('./p[contains(text(),"Advisor")]/a/@href').extract()
              item['students_and_descendants'] = content.xpath('./p[a[contains(text(),"students")] and a[contains(text(),"descendants")]]/text()').extract()
              # print(item['id'])
              # print("parse finished\n")

              yield item
