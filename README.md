## 目标
		获取所有A股最近300个交易日的日K数据。
## 思路
		通过一台 redis 数据库创建一个任务队列，存放所有的 A股股票代码，所有的爬虫共享这个队列。
		爬虫程序循环不断地从队列中拿到股票代码，然后模拟请求，从东方财富网获取最近300个交易的数据，解析后，存入mysql数据库。
##  实现
   整个程序分为两部分，RedisServer 负责从上交所、深交所获取所有的 A股股票代码，然后放入redis中的 "stock" 列表中。其中 main.py 是主要运行文件，通过 settings.py 文件配置 redis 数据库， tools.py 中存放了从上交所、深交所获取数据的具体实现方法。

![Image](https://github.com/a596480606/images/blob/master/file.png)
	
  然后是 SlaveSpider, 其中 main.py 通过一个 while 循环，不停地从 redis 数据中 "stock" 列表获取股票代码，拿到股票代码后就会的调用 tools.py 中的方法，从东方财富网获取数据，经过简单处理处理后存入mysql数据库。
![Image](https://github.com/a596480606/images/blob/master/data.png)
## 使用方法
先配置 RedisServer、SalveSpider中的 settings.py  文件，改为自己的数据库地址，然后先运行   中的 main.py ，等其运行完毕后，redis 中已经有了数据，就可以在任意多的电脑上启动 SalveSpider 的 main.py。

