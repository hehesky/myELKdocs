# Logstash简要说明

作者：暴力膜的编译器  
日期：2017年7月17日


本说明基于Logstash 5.4.3版，如与最新版本的官方文档有出入，则以官方文档为准。

官方文档：`https://www.elastic.co/guide/en/logstash/current/index.html`

参考资料：`http://udn.yyuap.com/doc/logstash-best-practice-cn/index.html`


> “不要听风就是雨，整天就想搞个大新闻，你们自己也要有判断。”


##1.下载与安装

###1.1准备工作
Logstash需要Java 8 SE的环境，在开始安装Logstash前请检查是否已经有合适版本的Java环境。

可以使用如下命令

	java -version
应当返回类似的版本信息

	java version "1.8.0_65"
	Java(TM) SE Runtime Environment (build 1.8.0_65-b17)
	Java HotSpot(TM) 64-Bit Server VM (build 25.65-b01, mixed mode)
		
###1.2 下载并安装Logstash
从https://www.elastic.co/downloads/logstash 下载Logstash的最近版本安装包，也可以考虑使用apt或yum命令进行下载

如使用yum命令

1）执行如下命令添加Elastic Co的公钥

	rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
	
2）将下列文本添加进/etc/yum.repo.d/logstash.repo文件，如果文件不存在则创建新文件

	[logstash-5.x]
	name=Elastic repository for 5.x packages
	baseurl=https://artifacts.elastic.co/packages/5.x/yum
	gpgcheck=1
	gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
	enabled=1
	autorefresh=1
	type=rpm-md

3）执行yum命令进行下载安装

	sudo yum install logstash

如直接下载了安装包，则解压后即可使用。需要注意的是用安装包解压的方法不会把Logstash作为系统服务进行安装。

	关于如何使用apt命令安装请参阅官方说明：
	https://www.elastic.co/guide/en/logstash/current/installing-logstash.html 

###1.3 验证安装（Hello World）
安装完成后，将命令行切换到Logstash安装目录下，执行

	bin/logstash -e 'input { stdin { } } output { stdout {} }'

Windows系统下请执行

	bin/logstash.bat -e 'input { stdin { } } output { stdout {} }'

	
上述命令会启动logstash，并设定从stdin读取输入，并原样输出至stdout。在Logstash启动完成并显示"Pipeline main started"后，键入hello world。若出现如下文本则说明安装成功：

	hello world
	2017-07-17T11:22:14.405+0800 0.0.0.0 hello world
	
##2. 配置与运行logstash

###2.1与Filebeat联动
对Filebeat的配置文件filebeat.yml进行编辑，设定如下

	filebeat.prospectors:
	- input_type: log
	  paths:
	    - /path/to/file/example.log 
	output.logstash:
	  hosts: ["localhost:9200"]

其中paths应设定为想要抓取的文件  
完成后验证配置文件

	./filebeat -e -configtest

###2.2 Logstash的配置文件
在logstash/bin文件夹下创建`logstash-simple.conf`文件，作为logstash运行时的配置文件。  

logstash的配置文件分为三个部分，输入`input`，过滤器`filter`，输出`output`

- 输入负责接收数据流
- 过滤器负责处理（如正则匹配，添加，删改信息等）数据
- 输出负责将处理后的数据发送出去  

配置文件都应该有如下结构

	# The # character at the beginning of a line indicates a comment. Use
	# comments to describe your configuration.
	input {
	}
	# The filter part of this file is commented out to indicate that it is
	# optional.
	 filter {
	
	 }
	output {
	}

其中，行首的#标明这一行文字是注释。一个配置文件必须有`input`和`output`部分，而`filter`部分不是必需的  


配合2.1节的设置，向`logstash-simple.conf`添加如下内容

	input {
		beats {
			port => "9200"
		}
	}
	
	output {
		stdout { codec => rubydebug }
	}

**此处的端口号应该与filebeat中向logstash输出的端口一致。logstash启动后会自动监听指定的端口上所有的数据。output中的codec => rubydebug 设定了输出的格式。**

完成后保存conf文件，并用如下命令启动logstash

	./logstash -f logstash-simple.conf

确保希望抓取的文件（2.1节中设置的example.log文件）存在，然后启动Filebeat

	./filebeat -e
	
稍等片刻后logstash会输出抓取到的信息。例如：

	{
		"@timestamp" => 2017-07-17T09:54:06.733Z,
			"offset" => 325,
		  "@version" => "1",
			  "beat" => {
			"hostname" => "My-MacBook-Pro.local",
				"name" => "My-MacBook-Pro.local"
		},
		"input_type" => "log",
			  "host" => "My-MacBook-Pro.local",
			"source" => "/path/to/file/logstash-tutorial.log",
		   "message" => "83.149.9.216 - - [04/Jan/2015:05:13:42 +0000] \"GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1\" 200 203023 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"",
			  "type" => "log",
			  "tags" => [
			[0] "beats_input_codec_plain_applied"
		]
	}

如果抓取的文件中有多行文本，则类似的Json对象会出现多个,并按照抓取的顺序输出。

至此，logstash已经成功地和filebeat联动。

###2.3 输出至Elasticsearch
在output部分中设置 `elasticsearch{ hosts => ["localhost:6000"]}`，即：

	output {
		#stdout{codec =>rubydebug}
		elasticsearch{ hosts => ["localhost:6000"]}
	}
其中端口号应该与Elasticsearch配置的对应。详细内容请参阅Elasticsearch README.md以及Elasticsearch官方文档 
[https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

###2.4 Logstash输出详解
在logstash内部，每次输出的一个字典对象称为一个事件(`event`)，每个事件中含有若干字段(`field`)。 字段可能的数据类型包括：

- 字符串（用双引号标识）
- 数字
- 布尔值（true或false）
- 列表（用[]标识，列表的成员类型必须相同，可以是任意类型）
- 字典（Hash， 用{}标识，键与值用 =>关联，即 key => value 其中key必须是字符串，value可以是任意类型）


###2.5 Logstash命令行选项
在修改过conf文件后，可以使用 `--config.test_and_exit`选项对配置文件进行验证，如

	./logstash -f logstash-simple.conf --config.test_and_exit

使用--config.reload.automatic可以让logstash自动检测conf文件是否有变动并自动重新载入配置文件。当输入端设置了stdin时此选项无法使用。

##3. 使用过滤器处理数据
过滤器相关的官方文档：`https://www.elastic.co/guide/en/logstash/current/filter-plugins.html`

下文将介绍几个常用的过滤器

###3.1 Grok过滤器
grok过滤器是logstash中最常用的过滤器，它能借助正则表达式对任意文本进行处理。经过Grok处理后的数据会更容易被其他过滤器处理。

####3.1.1 match选项与匹配规则

match命令是grok中最主要的命令，典型的格式如下

    match => {"fieldname" => "pattern"}

示例

	filter {
	  grok {
		match => { "message" => "%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %
		{NUMBER:bytes} %{NUMBER:duration}" }
	  }
	}

fieldname为需要处理的字段，通常logstash会把从输入端接收到的原文保存在message字段下，因此对此字段进行处理
pattern为使用的正则表达式。正则表达式应符合oniguruma标准（https://github.com/kkos/oniguruma/blob/master/doc/RE）

每当match选项执行后，匹配规则所匹配到的数据都会被单独存入指定的字段中，具体方式请看下文。


#####3.1.1.1 oniguruma正则表达式
oniguruma的基本的格式为

	%{SYNTAX:SEMANTIC}

SYNTAX为匹配规则的名称，SEMANTIC为匹配后存放数据的字段，

例如日志条目： '55.3.244.1 GET /index.html 15824 0.043' 	会被如下规则匹配

	%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}
	
匹配后会新增以下字段

	client: 55.3.244.1
	method: GET
	request: /index.html
	bytes: 15824
	duration: 0.043

完整的配置文件以供参考：

	input {
	  file {
		path => "/var/log/http.log"
	  }
	}
	filter {
	  grok {
		match => { "message" => "%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}" }
	  }
	}

如果一个匹配规则中SEMANTIC为空，则匹配到的数据不会被单独保存到一个字段中。	
	
Grok自带非常丰富的匹配规则，具体可在
`logstash安装文件夹\vendor\bundle\jruby\1.9\gems\logstash-patterns-core-4.1.0\patterns` 下查看

#####3.1.1.2使用常规的正则表达式
Grok本身是建立在正则表达式上的，所以普通的正则表达式也可通用。格式如下：

	(?<field_name>the pattern here)

例如：

	(?<queue_id>[0-9A-F]{10,11}) 会匹配一个10或11位的16进制数并保存到queue_id字段中
	
#####3.1.1.3 自定义匹配规则
为简化配置文件，可以自定义配置规则并将其保存在文件中方便调用。例如：

可以将

	POSTFIX_QUEUEID [0-9A-F]{10,11}
	
保存在logstash安装文件夹/bin/patterns/postfix文件中,并在grok中定义 patterns_dir => ["./patterns"]，然后在match选项中使用。即：

	match => { "message" => "%{POSTFIX_QUEUEID:queue_id}: %{GREEDYDATA:syslog_message}" }
 

完整的filter部分以供参考：

	filter {
	  grok {
		patterns_dir => ["./patterns"]
		match => { "message" => "%{POSTFIX_QUEUEID:queue_id}: %{GREEDYDATA:syslog_message}" }
	  }
	}
 
 
测试match命令中使用的匹配规则是否正确，可以使用grok debugger `http://grokdebug.herokuapp.com/` （需要科学上网）  

	与本文件同目录下的logstash_filters.txt中包含了nginx和tomcat用的匹配规则

####3.1.2 多重匹配

1）match选项对应的值可以是一个字符串列表，其成员为想要尝试匹配的匹配规则，例如：

	filter {
	  	grok { 
				match => { "message" => [ "Duration: %{NUMBER:duration}", 
										"Speed: %{NUMBER:speed}"]
						 } 
			 } 
		}
	

若使用多个匹配规则进行match，建议同时也设置break_on_match。该选项类型为bool，默认值为true。在设定为true时，match将在发现第一个完全匹配的匹配规则是停止。否则会将所有匹配规则都匹配一遍。


2）tag_on_failure选项为字符串列表，默认为["_grokparsefailure"]。
每次match匹配失败（所有的匹配规则都无法匹配）时，会自动添加列表中的字符串到事件的标签tag列表中。


###3.2 Date过滤器
默认情况下，filebeat每次输出会生成一个@timestamp域，并将其设为输出时的时间。而Kibana默认会以@timestamp的值作为各条目的时间戳记，并以此为排序基准。实际使用过程中，很多日志条目都包含时间戳记，并且我们希望能够使用日志内的时间信息对日志进行排序。为此需要用到date过滤器

date过滤器是专门用于解析日期时间的过滤器。每当date完成解析后，@timestamp字段（或其他某个指定的字段）会被解析出来的值覆盖。由此可以达到预期的目标。

官方文档：`https://www.elastic.co/guide/en/logstash/current/plugins-filters-date.html`

####3.2.1 match选项
类似于grok，date也使用match选项作为其主要功能选项。Date的match选项用法有所不同，具体如下。

	match => ["source_field","format1","format2",...]

其中source_field为包含有想要的日期信息的字段。format为符合 joda-time api的格式匹配规则（http://www.joda.org/joda-time/key_format.html）。 例如：

	date {
		match => [ "logdate", "MMM dd yyyy HH:mm:ss" ]
	}

以及

	match => [ "logdate", "MMM dd yyyy HH:mm:ss",
          "MMM  d yyyy HH:mm:ss", "ISO8601" ]
		  

		  
match匹配完成时@timestamp字段（或其他由target选项指定的字段）会被解析出来的值覆盖。		
  
#####3.2.1.1 内置日期匹配规则

- ISO8601   符合ISO8601标准的日期，如 2011-04-19T03:44:01.103Z
- UNIX      UNIX标准时，以秒为单位的浮点数
- UNIX_MS   UNIX标准时，以毫秒为单位的整数

使用内置匹配规则时直接填写名称即可

#####3.2.1.2 常用自定义日期匹配规则格式

	年份
	yyyy 四位数年份，如1999，2015等
	yy   两位数年份，如15表示2015年
	
	月份
	M    短数字月份，如1，5,10,12等
	MM   两位数月份，如01,05,10,12等
	MMM  月份英文缩写，如Jan, May, Oct,Dec等
	MMMM 月份英文全称，如January
	
	日期
	d    短数字日期，如1,6,16,30等
	dd   两位数日期，如01,06，16等
	
	小时（24小时制，0-24）
	H    短数字小时，如0表示午夜，12为正午
	HH   两位数小时，如00,06,12,23等
	
	分钟（0-59）
	m    短数字分钟
	mm   两位数分钟
	
	秒（0-59）
	s   短数字秒数
	ss  两位数秒数



####3.2.2 target选项
若希望覆盖其他字段而非@timestamp，可以使用target选项，格式为

	target => “fieldname”


###3.3 Mutate过滤器
Mutate过滤器用于修改字段内的数据

####3.3.1 Covert选项

	Convert选项用于转换字段数据的类型，格式为：
	  mutate {
	    convert => { "fieldname" => "<type>" }
	  }	

可用的type名称包括 boolean，integer，string。
如果要转换的字段是一个数组，则其所有成员都会被转换；如果要转换的字段是一个字典，则不会发生任何变化。

在尝试转换为bool类型时，
以下数据会被转换为true ：

	true, t, yes, y, 1

以下数据会被转换为false：

	false, f, no, n, 0
	

####3.3.2 add_field选项
`add_field`允许添加自定义的字段，且允许使用%{}来引用其他字段，如

	add_field => { "foo_%{somefield}" => "Hello world, from %{host}" }
	
####3.3.3 remove_field选项
使用`remove_field`来移除指定域，如
	remove_field =>["offset","beat","@version","input_type"]
	

####3.3.4 if-else语句

在filter中允许使用if else进行条件性操作
如：

	if [AccessClass] 
	{
		mutate { add_tag => ["Catalina"] }
	}
	else
	{
		mutate { add_tag =>["Nginx"] }
	}
	
当AccessClass字段存在时，添加标签Catalina，否则添加标签Nginx


###3.4 Logstash的多行事件（不推荐使用）
Logstash本身也可以将多个事件合并为一个事件。按照Elastic官方的文档，logstash的多行事件并不安全，有可能造成编码错误，因此应当作为备用手段。在可以使用Filebeat以及其他日志文件处理工具时，应当优先考虑这些选项。

若要使用logstash的多行事件，可以在conf文件中对想要设定的input部分进行如下设定

	
	input {
	  stdin {
		codec => multiline {
		  pattern => "pattern, a regexp"
		  negate => "true" or "false"
		  what => "previous" or "next"
		}
	  }
	}	
	
类似于filebeat的多行设定，pattern为正则表达式，negate为bool类型表示是在正则表达式匹配还是不匹配时激活多行事件，what类似于match控制当前行是向前还是向后合并。 其中negate是可选的，默认为false。

下面的例子可以用于处理java异常日志（即空格开头的行向前合并）

	input {
	  stdin {
	    codec => multiline {
	      pattern => "^\s"
	      what => "previous"
	    }
	  }
	}
	
		
	
<br />	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
