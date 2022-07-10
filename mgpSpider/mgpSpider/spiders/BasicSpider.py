import scrapy
class BasicSpider(scrapy.Spider):
    name = "basic"
    #allowed_domains = ["web"]
    start_urls = ["https://www.genealogy.math.ndsu.nodak.edu/id.php?id=1"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=122738"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=53410"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=60782"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=93643"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=125886"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=283247"
                ,"https://www.genealogy.math.ndsu.nodak.edu/id.php?id=129807"
                ]
    # def start_requests(self):
    #     url = "https://www.mathgenealogy.org/id.php?id=1"
    #     return
    print("start\n") 

    def parse(self, response):
        print("start parsing\n")
        self.log("id: %s" % response.url.split("=")[-1])
        self.log("name: %s" % response.css("h2::text").extract()[0].strip())
        content = response.xpath('//*[@id="paddingWrapper"]')[0]
        self.log("mathscinet_id: %s" % content.xpath('.//a[text()="MathSciNet"]/@href').extract())
        
        self.log("degree_year: %s" % content.xpath('./div/span[span[contains(@style,"color:\n  #006633")]]/text()').extract()[-1].strip())
        self.log("school_name: %s" % content.xpath('./div/span/span[contains(@style,"color:\n  #006633")]/text()').extract())
        
        self.log("advisors: %s" % content.xpath('./p[contains(text(),"Advisor")]/a/@href').extract())
        self.log("students and descedants: %s" % content.xpath('./p[a[contains(text(),"students")] and a[contains(text(),"descendants")]]/text()').extract())
        #self.log("mathematics_subject_classification: %s" % )
