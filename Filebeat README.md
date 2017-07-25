#Filebeat 简要说明

作者：暴力膜的编译器  
日期：2017年7月17日

> "要是文件上的读取出现了偏差，等于你们也有责任的。"

本说明基于Filebeat 5.4.3版，如与最新版本的官方文档有出入，则以官方文档为准。
官方文档地址：https://www.elastic.co/guide/en/beats/filebeat/current/index.html


##1.下载与安装

官方下载地址：https://www.elastic.co/downloads/beats/filebeat
windows可直接下载zip文件并解压后直接使用

Unix环境下参考https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html 
的说明可以使用.deb或rpm进行下载安装，也可直接下载zip文件解压使用

注意：直接解压zip文件（以及tar文件）的安装方式不会将Filebeat设置为系统服务，进而无法作为服务启动

##2.配置Filebeat
在Filebeat的安装目录下有filebeat.yml文件。该文件是Filebeat的默认配置文件，使用的是YAML语法。
同目录下有filebeat.full.yml文件，包含所有的配置选项以及说明，可供参考
在配置文件中没有设置的选项将全部使用默认值，关于默认值可参阅filebeat.full.yml

###2.1设置抓取的文件
在初始的配置文件中有如下片段


	filebeat.prospectors:
	- input_type: log
	  paths:
		- /var/log/*.log
		#- c:\programdata\elasticsearch\logs\*
	

prospectors负责抓取文件内容，input_type可以为log或stdin。设定为stdin时接受从键盘输入。
设定为log时默认逐行读取文件，且一次处理一行内容。需要设定文件的路径，即paths选项。Filebeat允许设定多个prospectors，且每个prospector都能设定多个路径。例：

	filebeat.prospectors:
	- input_type: log
	  paths:
		- /var/log/system.log
		- /var/log/wifi.log
	- input_type: log
	  paths:
		- "/var/log/apache2/*"

应当注意YAML中冒号后必须有空格, 且YAML中缩进是有意义的（默认空两格为一层，类似于python的缩进关系）	

###2.2 Filebeat的输出
Filebeat在抓取文本时，默认每抓取一行生成一个事件（event）。事件以Json的格式输出，其中抓取到的文本保存在message字段下。其他重要的字段包括@timestamp，source等，关于字段的解析请参阅logstash的说明文档。

Filebeat支持多种输出方式，包括Elasticsearch，logstash等

####2.2.1 向stdout输出

output.console:
    pretty: true
	
output.console指向stdout输出。pretty选项控制输出的json是否以高可读性的方式输出（缩进换行等），默认为false

####2.2.2 向Elasticsearch输出
如果希望直接向Elasticsearch输出，可做如下设置：

output.elasticsearch:
  hosts: ["192.168.1.42:9200"]

其中，hosts可以设置多个地址， 如：
  hosts: ["192.168.1.42:9200"，“localhost：9200”]

####2.2.3 向Logstash输出
类似于向Elasticsearch输出

output.logstash:
  hosts: ["127.0.0.1:5044"]

相似地，hosts中可以设置多个地址


####2.3验证配置
执行如下命令验证配置是否符合filebeat的要求
UNIX下：
 ./filebeat -configtest -e
Windows下：
 filebeat.exe -configtest -e
 
###2.4 拓展配置
若需要向其他程序（如kafka，redis等）输出，可参阅filebeat.full.yml

####2.4.1 在Filebeat输出添加自定义字段 （可选）

在prospectors的设定下可以添加fields选项。 fields选项将在输出的Json对象中插入指定的字段，可以接受的数据类型为任意的标量（字符串，数字），数组，字典以及上述类型的复合结构。若fields选项中指定的字段已经存在，则会覆盖已有的数据。请务必小心。默认状态下由fields添加的字段将会集中放在fields字段下（如fields.app_id）。如需将自定义字段置于顶层，则需设定fields_under_root为true

例：

	filebeat.prospectors:
	- paths: ["/var/log/app/*.log"]
	  fields:
	    app_id: query_engine_12
	fields_under_root：true

上述片段表示将额外添加app_id字段，值为query_engine_12，且保存在Json对象的顶层。


##3. 运行filebeat

在控制台输入如下命令可以运行filebeat

	UNIX下：
	 ./filebeat -e
	Windows下：
	 filebeat.exe -e

其中-e选项将启用调试信息。
如果不使用-e选项运行，filebeat不会输出任何信息（除非配置了output.console）


#4.其他
##4.1 重置Filebeat读取文件的位置
在安装目录的/data文件夹下有一个registry文件，里面以Json的格式记录了Filebeat读取过的文件的进度。修改或删除该文件即可调整filebeat读取文件的起始位置。


##4.2 配置多行读取
默认情况下filebeat每读取一行就产生一个事件并输出。使用multiline选项可以要求Filebeat读取符合一定特征的多行文本后再输出一个事件。具体如下。

配置multiline至少需要配置以下两个选项

- `multiline.pattern` 用于匹配的正则表达式，如 `'^[A-Z]+:\s'` <br />  建议将正则表达式用单引号标识，以便YAML语言解释器区分
- `multiline.match` 可用值为after和before。 after表示如果当前行匹配则与前一行合并。before表示与后一行合并。
	
可选配置


- `multiline.negate` 可用值为true和false，默认为false。当设为true时，在当前行 *不匹配* 正则表达式时按照match选项进行合并。设为false时不改变行为方式。
	

例如，尝试处理Java异常信息

	Exception in thread "main" java.lang.NullPointerException
			at com.example.myproject.Book.getTitle(Book.java:16)
			at com.example.myproject.Author.getBookTitles(Author.java:25)
			at com.example.myproject.Bootstrap.main(Bootstrap.java:14)

易知以空格开始的每一行都应与前一行合并，故设置如下

	multiline.pattern: '^[[:space:]]'
	multiline.negate: false
	multiline.match: after


为测试multiline的正则表达式，可以访问（需要科学上网）：

	https://play.golang.org/p/uAd5XHxscu

<br />

















  
  