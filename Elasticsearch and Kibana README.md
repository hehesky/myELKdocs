#Elasticsearch 与 Kibana 简要说明

作者：	暴力膜的编译器   
更新日期：2017年7月24日

注：本文基于Elasticsearch 和Kibana 5.4.3版，如与最新版有出入，则以官方文档为准

Elasticsearch官方文档：[https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

Kibana官方文档：
[https://www.elastic.co/guide/en/kibana/current/index.html](https://www.elastic.co/guide/en/kibana/current/index.html)

>“你有权保持沉默，但你说的一切都会被Kibana画成饼状图” 

----------

##1.安装Elasticsearch
开始安装前请保证本地已经安装有Java 8，可以使用下述命令查看

	java -version

访问Elasticsearch 官方网站下载安装包 https://www.elastic.co/downloads/elasticsearch
下载后解压即可

也可以通过deb和rpm命令进行安装，详情请参阅官方说明https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html
Windows环境下也可以使用.msi安装文件

安装完成后切换到Elasticsearch安装目录，启动Elasticsearch

	bin/elasticsearch （Windows下执行bin\elasticsearch.bat）

用curl命令检查Elasticsearch是否正确启动

	curl http://localhost:9200/

编辑 `config/elasticsearch.yml`可以修改Elasticsearch绑定的ip与端口（默认localhost:9200）
##2.安装Kibana
访问https://www.elastic.co/downloads/kibana 获取最新版的Kibana安装包

解压/安装后，进入Kibana安装目录，编辑config/kibana.yml，设定elasitcsearch.url使其指向一个运行中的Elasticsearch实例，例如

	elasticsearch.url: "http://localhost:9200"
	
确保Elasticsearch在正常运行后，启动kibana

	bin/kibana (windows下 bin\kibana.bat)
	
在浏览器中访问`http://localhost:5601 `如果安装正确则会显示Kibana的启动页面

需要注意的是，Kibana启动必须要有一个运行中的Elasticsearch实例。故两者是天然联动的

##3.使用Kibana的dev tool对Elasticsearch中的数据进行操作
进入kibana页面后，点击左侧导航栏中的Dev Tool，打开开发者控制台。

在主界面的左边可以输入HTTP/REST 指令，按执行按钮（三角形）后在右侧可以看到运行结果

###3.1 检查Elasticsearch集群健康状况
在控制台输入如下指令

	GET /_cat/health?v

会得到关于所有集群的信息，例如

	epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
	1475247709 17:01:49  elasticsearch green           1         1      0   0    0    0        0             0                  -                100.0%
	



- Elasticsearch 是分布式的全文检索系统。每个运行的Elasticsearch实例称为一个节点（`node`），一或多个节点可以形成一个集群（`cluster`）。集群内的节点共同负责数据的存储、备份和查询。任何一个节点都必须从属于一个集群（即使这个集群只有一个节点）。


- Elasticsearch的集群健康状态分为 `red` `yellow` `green` 三种。其中`red`表示有严重错误无法使用；`yellow`表示有非致命错误（比如备份节点未上线）但可以使用；`green`表示一切正常。

###3.2罗列索引
在Elasticsearch中，数据以索引（index）的方式储存。索引类似于SQL中的表，有相对固定的结构。当Logstash向Elasticsearch输出数据时，Logstash自动会生成对应的索引。默认状况下会命名为`logstash-xxx`, 其中xxx为日期。

在kibana的开发者控制台中执行以下命令可以查看所有的索引

	GET /_cat/indices?v
	
###3.3创建新的索引
使用下列命令创建customer索引并罗列所有索引

	PUT /customer?pretty
	GET /_cat/indices?v

会得到类似的回复：

	health status index    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
	yellow open   customer 95SQ4TSUT7mWBT7VNHH67A   5   1          0            0       260b           260b

此处索引健康状态为yellow是因为没有设定备份（`replica`）。关于如何设定备份请参阅官方文档。


###3.4 向索引插入新的条目（Document）

尝试向customer索引中插入external类型的新条目，id为1

	PUT /customer/external/1?pretty
	{
	  "name": "John Doe"
	}

得到如下回复

	{
	  "_index" : "customer",
	  "_type" : "external",
	  "_id" : "1",
	  "_version" : 1,
	  "result" : "created",
	  "_shards" : {
		"total" : 2,
		"successful" : 1,
		"failed" : 0
	  },
	  "created" : true
	}


查询刚才插入的新条目

	GET /customer/external/1?pretty
	
得到如下回复：

	{
	  "_index" : "customer",
	  "_type" : "external",
	  "_id" : "1",
	  "_version" : 1,
	  "found" : true,
	  "_source" : { "name": "John Doe" }
	}


###3.5 删除索引

删除customer索引并罗列所有的索引

	DELETE /customer?pretty
	GET /_cat/indices?v

###3.6 小结
REST 的请求结构如下

	<REST Verb> /<Index>/<Type>/<ID>






<br />


















