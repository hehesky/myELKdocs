#Mantis安装与升级

编译：周恺华 （a.k.a暴力膜的编译器）  
更新日期：2017年7月24日

注：本文翻译自Mantis官方文档第二章，原文（HTML版）[https://www.mantisbt.org/docs/master/en-US/Admin_Guide/html-desktop/](https://www.mantisbt.org/docs/master/en-US/Admin_Guide/html-desktop/)
> **“螳螂捕蝉，不抓bug”**

----------

##1.先决条件
安装/升级Mantis前请确保服务器已安装有如下组件：

	1）Web Server， 例如Apache，nginx等
	2）PHP 解释器（5.5版以上，建议使用php7或更新的）
	3）PHP插件
		a. 数据库插件（mysqli，pgsql等）
		b. mbstring插件（用于支持UTF-8编码）
	4）数据库：mysql或pgsql

	
##2. 准备工作
在开始安装/更新前，请执行如下步骤

	1）下载MantisBT，地址 https://www.mantisbt.org/download.php 下载完毕后应为一zip压缩文件（如mantisbt-2.5.1.zip）
	2）将压缩文件上传至服务器（使用scp，ftp或winscp等）
	3）解压压缩文件至单独一个目录。如果条件允许则重命名该目录为mantisbt。
	
##3. 安装Mantis
本节适用于在一个从未安装过mantis或已经完全卸载mantis的服务器上安装mantis的情形。若想要升级已有的mantis系统请参阅下文。


将mantisbt文件夹复制到web服务器的根目录（或者服务器下其他目录），例如：

	/var/www/html/
	
使用网页浏览器打开mantis安装脚本，例如：

	http://yoursite/mantisbt/admin/install.php

打开后，执行如下步骤

	1）脚本会自动检测环境，如果显示全部正常（全绿），则执行下一步。否则请检查服务器配置
	2）在页面上填写如下信息：
		- 数据库类型
		- 数据库地址 （如localhost）
		- 供Mantis使用的数据库名称
		- 供Mantis使用的数据库用户名和密码 （如果没有则请先创建账户，并提供SELECT, INSERT, UPDATE, and DELETE权限）
		- 有管理员权限的数据库用户名和密码 （如root账户）
	3）点击Install/Upgrade Database按钮
	4）脚本将自动在数据库中创建对应的数据库和表。
	5）如果安装脚本没有报错，会提示安装即将完成。
		- 该脚本会尝试向mantisbt/config/config_inc.php写入基本配置信息。
		- 在大多数情况下该行为会失败（权限不足），并在页面上显示一个警告。
		- 此时应手动创建该文件，并从网页上复制相关内容写入文件。
	6）检查页面上是否有其他错误与警告。采取相应的措施进行修复
	
##4. 升级Mantis
升级mantis前请先执行前文准备工作中的步骤。

执行如下步骤进行升级：

1）将已有的mantis网站切换为下线维护状态，在mantis安装目录下执行
	
	cp mantis_offline.php.sample mantis_offline.php

2）对已有的数据进行备份。如使用数据库的dump指令  
3）备份配置文件。可能文件包括：



- `config_inc.php`
- `custom_strings_inc.php`
- 额外添加的css
- 图片文件

4）执行安装脚本

	http://yoursite/mantisbt-NEW/admin/install.php
   
其中mantisbt-NEW为新版文件的解压地址

5）在页面上提供相关信息：


- 有管理员权限的数据库用户名和密码
	
6）点击Install/Upgrade Database按钮

7）脚本执行完毕后，检查页面上是否有其他错误和警告。采取相应措施进行修复
	
##5.测试安装/升级

1）从浏览器打开 `http://yoursite/mantisbt/admin/check/index.php` 该脚本会验证mantis是否已经正确安装。建议修复所有的问题之后再执行之后的操作

2) 若mantis将在一个不安全的环境（如公网）下运行，应删除admin目录。该目录下的脚本有可能被恶意使用。

	rm -r admin
		
##6. 安装后的扫尾工作

1）登录mantis首页，使用默认账户登录：

	用户名： administrator 
	密码： root
2）修改`administrator`账户的密码或创建新的管理员账户

- 进入 管理-用户管理 执行相关操作。
- 如果创建了新的管理员账户，建议删除`administrator`账户以保证安全
		
##7.升级后的扫尾工作

1）测试新版mantis，登录并检查数据是否有遗漏  
2）将新版mantis上线。在web服务器的根目录执行：

	mv mantisbt mantisbt-old
	mv mantisbt-NEW mantisbt
3）将新版mantis投入使用

	rm mantis_offline.php
4）将之前备份的配置文件复制到新版mantis对应的位置

##8. 卸载mantis
1）删除mantis目录及其下属所有文件  
2）在数据库中drop所有相关的表。如果条件允许则可以drop整个mantis的数据库  
3）移除自定义配置文件等
	
	

<br />










