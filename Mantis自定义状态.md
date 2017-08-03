#在Mantis中添加/修改自定义状态的流程

编译: 暴力膜的编译器  
日期: 2017年7月24日

> “从今天起9527就是你的终身状态代码”

注：本文基于mantis 2.5.1版官方文档制作,如与最新版有出入,则以官方文档为准

----------

##1.准备
在开始前建议先备份`config/config_inc.php`文件。如有必要可以将mantis网站转入维护状态  

在mantis根目录下执行

	cp mantis_offline.php.sample mantis_offline.php

完成后删除mantis_offline.php即可解除维护状态
	
	rm mantis_offline.php

##2.定义新状态常量
在config文件夹下，新建或编辑`custom_constants_inc.php`文件，使其包含要添加的自定义状态

例如，欲添加新状态testing（测试中）：

	<?php
	 # Custom status code
	 define( 'TESTING', 60 );

其中'testing'为新状态的名称,60为对应的状态编号。

##3.将自定义状态加入状态枚举
编辑`config/config_inc.php`（如文件不存在则新建）

添加包含自定义状态的状态枚举字符串，并添加自定义状态对应的颜色，例如

	# Revised enum string with new 'testing' status
	$g_status_enum_string ='10:new,20:feedback,30:acknowledged,40:confirmed,50:assigned,60:testing,80:resolved,90:closed';
	# Status color additions
	$g_status_colors['testing'] = '#ACE7AE';

其中，`$g_status_colors[]`中的键值（key）必须和`$g_status_enum_string`中的自定义状态字符串值相同。颜色为十六进制色码，可在该网站查询：

	http://www.color-hex.com/

##4定义状态在mantis页面上如何显示

在config文件夹下，新建或编辑`custom_strings_inc.php`文件，为mantis使用的每种语言都设定状态文字。（应当至少包括当前使用的语言，如简体中文，以及mantis的默认语言，即英语）。 例如：

	<?php
	switch($g_active_language)
	{
	case 'chinese_simplified':
		$s_status_enum_string= '10:新建,20:反馈,30:认可,40:确认,50:已分配,60:测试中,80:已解决,90:已关闭';
		$s_inprogress_bug_title='状态改为测试中';
		$s_inprogress_button='开始测试';
		$s_email_notification_title_for_status_bug_inprogress ='下列问题已经进入测试阶段';
		break;
		
	default:
		$s_status_enum_string='10:new,20:feedback,30:acknowledged,40:confirmed,50:assigned,60:testing,80:resolved,90:closed';
		$s_inprogress_bug_title='Mark issues as testing';
		$s_inprogress_button='start testing';
		$s_email_notification_title_for_status_bug_inprogress ='The following issue is now testing';
		
		break;
	}

##5.扫尾工作
解除mantis的维护状态，进入管理-配置管理-工作流，查看自定义状态是否成功添加。

如果成功添加，建议调整工作流页面中的设定，使其能够匹配新添加的状态。

如果新添加的状态显示为类似于：`@66@` `@60@`

则请检查之前编辑的文件内容是否正确，且使用了正确的文件名

- `custom_strings_inc.php` 以及 `custom_constants_inc.php` 中的（s）不能少
- `custom_strings_inc.php` 文件中简体中文为chinese_simplified
- `switch`语句应该包含`break`

<br />