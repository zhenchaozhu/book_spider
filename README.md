# 笔趣库的小说爬虫
总共爬取了大概3千多本书籍，每次启动爬虫章节可以自动更新  
小说的章节内容是存成txt格式的文件到硬盘，小说的封面图上传到七牛上进行存储  
可以在crontab设置爬虫进程定时进行爬取，并且爬虫日志根据每次启动时间来进行分割

### 接下来的开发工作
##### ~~使用scrapy_redis来实现分布式部署爬取~~
##### 考虑使用adsl或者定时爬取可以的免费ip来做请求代理
##### 多个网站来源爬取小说
