## Mathematical Genealogy Project scrape
这是一个自学爬虫的项目，最终目标是爬取数学家系谱图计划(Mathematical Genealogy Project)的数据库。

## 参考资料：
### 爬虫项目类
1. 北理工python爬虫公开课[https://www.bilibili.com/video/BV1P741177gm?p=1]，主要介绍requests库和bs4库，附带一点点scrapy框架。适合不想看英语的python初学者，但年代较久远，后面的示例已经失效。子文件夹learn_crawler是一些杂乱的课堂笔记。

2. QQ空间说说爬取[https://cloud.tencent.com/developer/article/1839514]，使用了selenium库和chrome浏览器驱动模拟填写表单登录QQ空间。代码仍然有效，复制粘贴即可。

3. 一个类似的mgp scraper[https://github.com/skipperkongen/math-genealogy-geocoder]，我参考了它将数据以数据库形式存储。

### 爬虫书籍类

1. Python 网络数据采集 Ryan Mitchell，在北理工课程基础上多介绍了一些（比如数据库）。Github上有配套的项目代码[https://github.com/REMitchell/python-scraping]。第一版有中文翻译（科技书中为数不多较有个性的翻译），第二版中加入了scrapy章节，浅尝辄止且大部分是官方文档摘录。

2. Learning scrapy。主要介绍scrapy库，第一版有人翻译成中文发布在简书上[https://www.jianshu.com/c/a3b6e459f76c]，不过第一版介绍的scrapy版本较老，注意有一些关键词的用法变更。其中结合chrome检查页面功能介绍并获取xpath的部分非常有趣，还介绍了scrapy的shell用法，可以呼出ipython kernel交互，适合scrapy框架编写前的调试。

3. Getting Started with SQL。主要介绍sql语言和一些数据库的基本操作，非常简短，适合随时查阅。

### 官方文档类

1. scrapy[https://docs.scrapy.org/en/latest/]，一个非常优秀的开源爬虫框架

2. sqlite3[https://docs.python.org/3/library/sqlite3.html]，一个轻型数据库界面

### 其他

还学了一丢丢的html语法树、xpath语言和正则表达式，爽！

### 截图留念

近三十万个页面，服务器爬取用时近10小时。

(https://raw.githubusercontent.com/alephpi/Mathematical-Genealogy/master/mgpSpider/%E6%88%AA%E5%9B%BE%E7%95%99%E5%BF%B5%20copy.png)
