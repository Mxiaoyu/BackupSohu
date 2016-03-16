# BackupSohu
backup the page of "http://m.sohu.com" once 60s by python  
实现方式为urllib2+beautifulsoup
Backup类：实现页面的访问和解析，实现了两个方法，download_page,访问页面，取得页面源码；para_page，解析页面源码，将src和href属性的图片，js，css下载并更改其显示路径
# 待完善  
* 广告图片由于隐藏未能找到合适的解决方法
* 最下面广告由于采iframe框架，也为能够爬取
