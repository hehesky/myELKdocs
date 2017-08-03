#Apache Ant简要说明

作者/编译：暴力膜的编译器  
日期：2017年8月

注：本文基于Apache Ant 1.10.1版，如与官方文档有出入，则以官方文档为准

Apache Ant官方文档： `https://ant.apache.org/manual/`

> 从前有只蚂蚁会上树，直到它膝盖中了一架阿帕奇


##1.获取Ant
Appache Ant可以直接从官网下载安装包，也可以通过RPM的方式获取。如果希望使用RPM，请访问`http://www.jpackage.org/`

###1.1下载
访问Ant官方下载页面[http://ant.apache.org/bindownload.cgi](http://ant.apache.org/bindownload.cgi)，下载zip文件（或者tar文件亦可）。在本文写作时官方推荐的版本为`1.10.1`以及`1.9.9`。其中`1.10.1`需要Java 8（或更新）的运行环境，`1.9.9`需要Java 5（或更新）。条件允许时应尽量使用`1.10.x`或更新版本。

下载后直接解压，并配置相关环境变量：

- 将Ant的解压目录（如`D:\apache-ant-1.10.1`）设定为`ANT_HOME`
- 将`$ANT_HOME\bin`加入PATH变量中

在控制台运行如下命令检查Ant是否正确配置

	ant -version

应当返回如下信息

	Apache Ant(TM) version 1.10.1 compiled on February 2 2017

##2.关于Apache Ant

Apache Ant是适用于Java开发的编译、打包、整理工具。与GNU Make的很多功能相似，但有大量针对Java特性的优化。同时理论上也支持对C/C++等语言的编译。 Ant本身基于java，因此有着良好的跨平台兼容性，相比make只能在unix环境运行更加适合java项目。

Ant主要通过解析一个（或多个）XML文件来定义自身的行为，如`build.xml`。当在控制台运行`ant`指令时，Ant会自动在当前目录寻找`build.xml`（默认目标），并尝试解析。解析成功后会执行文件中定义的默认指令。

用户可以通过`-f`选项来指定XML文件给Ant使用，如
	
	ant -f myconfig.xml

为了简化说明，下文中尽量都使用`build.xml`为Ant的配置文件
###2.1编写简单的build.xml文件
本节将介绍一个简单实例，说明build.xml文件的结构以及如何使用ant
####2.1.1准备工作
在一空白目录下，新建`build.xml`  

在该目录下新建目录`src`，并将下述java代码保存至`src/oata/HelloWorld.java`

	package oata;
	public class HelloWorld {
	    public static void main(String[] args) {
	        System.out.println("Hello World");
	    }
	}

上述代码仅为一个简单的helloworld程序。
####2.1.2开始编写build.xml
打开并编辑之前创建的`build.xml`  

首先添加`<project></project>`标签对，此为文档的顶层标签。之后在`<project>`中添加`default`属性，值为任意。如：
	
	<project default="info"></project>

default属性设定了该文件的默认指令，示例中为`info`指令。接下来编写info指令。

指令使用`<target></target>`标签，并用属性name命名，如：

	<target name="info"></target>


现在info指令还为空。向其中添加任务（task），如`echo`:

	<project default="info">
		<target name="info"> 
			<echo>"Hello World with Ant."</echo> 
		</target>
	</project>

在Ant中，指令（`target`）是包含一组任务（`task`）的容器，是能执行最小单位。一个指令可以包括一或多个任务（`task`）。一个任务为某个特定的行为，如向控制台输出（即`echo`），编译（`javac`以及`jspc`)，打包（`jar`和`war`）等等。

完成后在build.xml所在文件夹打开控制台，执行
	
	ant info

应当显示

	Apache Ant(TM) version 1.10.1 compiled on February 2 2017
	
	D:\random_stuff\project>ant info
	Buildfile: D:\random_stuff\project\build.xml
	
	info:
	     [echo] "Hello World with Ant."
	
	BUILD SUCCESSFUL
	Total time: 0 seconds


####2.1.3编译、打包与运行
接下来将尝试编译、打包和运行之前准备的HelloWorld.java文件。

**_在开始前请先确保该文件能正常编译与运行（即直接使用javac和java指令）。_**

向`build.xml`文件中添加四个target，分别命名为compile，jar，run和clean

    <target name="compile" >
        <mkdir dir="debug\class" />
        <javac srcdir="src" destdir="debug\class" includeantruntime="false"/>
    </target>

    <target name="jar">
        <mkdir dir="debug\jar" />
        <jar destfile="debug\jar\HelloWorld.jar" basedir="debug\class">
            <manifest>
                <attribute name="Main-Class" value="oata.HelloWorld" />
            </manifest>
        </jar>
    </target>

    <target name="run">
        <java jar="debug\jar\HelloWorld.jar" fork="true" />
    </target>

    <target name="clean">
	    <delete includeEmptyDirs="true">
	        <fileset dir="debug" includes="**/*"/>
	    </delete>
	</target>

其中：


+ `mkdir`负责创建目录（如目录已存在则不进行如何操作），且支持创建多层目录。
	+ `dir`属性为要创建的路径
+ `javac`负责调用javac编译器
	+ `src`为源码目录
		+ `destdir`为产生的class文件存放目录
		+ `includeantruntime`为布尔类型，设定编译时是否载入AntRuntime库，官方文档上推荐设为false（默认值为true）。
+ `jar`负责将class文件打包为jar文件
	+ `destfile`为输出文件目录
	+ `basedir`为开始打包的顶层目录
	+ `jar`任务中必须包含一个`manifest`子元素，且`manifest`中至少要设定Main-Class，即`<attribute name="Main-Class" value="path.to.Main-Class" />`
+ `java`负责运行指定的文件。
	+ `jar`指定要执行的jar文件
	+ `fork`为bool类型，设定是否要新建一个JVM进程来运行文件。一般推荐设为true
+ `delete`负责删除指定的文件（以及目录）
	+ `delete`可以接受`file`或`dir`属性，前者指向文件，后者指向文件夹
	+ `delete`也可以接受一个嵌套的资源集合（resource collection，如上文中的`fileset`)。
		+ 关于资源集合在后文有更多信息

编辑并保存buid.xml文件，并在控制台执行

	ant compile
	ant jar
	ant run

或者也可以将三个命令合并为
	
	ant compile jar run

成功后应当有如下输出

	Buildfile: D:\random_stuff\project\build.xml
	
	compile:
	    [mkdir] Created dir: D:\random_stuff\project\debug\class
	    [javac] Compiling 1 source file to D:\random_stuff\project\debug\class
	
	jar:
	    [mkdir] Created dir: D:\random_stuff\project\debug\jar
	      [jar] Building jar: D:\random_stuff\project\debug\jar\HelloWorld.jar
	
	run:
	     [java] Hello World +1
	
	BUILD SUCCESSFUL
	Total time: 0 seconds


之后运行

	ant clean

观察生成的class和jar文件是否被删除

至此build.xml文件已经具备了基本的结构与功能

###2.2改进build.xml文件

到目前为止，`build.xml`文件中的所有路径都是常量，应当将其设定为变量方便未来编辑。

另外compile jar run命令都可以任意顺序执行，容易报错。

接下来将针对这两点对build.xml文件进行改进

###2.2.1利用target的依赖（depends）属性控制执行顺序
在build.xml文件中，可以为指令`target`配置`depends`属性。

例如，希望在执行jar指令前应该先执行compile，则可以设定：

	<target name="jar" depends="compile">
		...
	</target>

此时，如果直接执行`ant jar`，ant会先执行`compile`指令，再执行jar

同样的，可以要求ant在执行`run`之前必须执行`jar`，即：
	
	<target name="run" depends="jar">
		...
	</target>


###2.2.2利用property设定变量

在`<project>`标签下可以通过添加`<property>`标签来定义变量，例如

	<property name="debug.dir" value="debug" />

由此定义的变量可以被调用，格式为`${some_name}`，例如：

	<property name="jar.dir" value="${debug.dir}\jar" />

至此我们可以尝试将之前build.xml中所有的路径替换为定义的变量，即

	<project default="info">
	    <property name="debug.dir" value="debug" />
	    <property name="jar.dir" value="${debug.dir}\jar" />
	    <property name="class.dir" value="${debug.dir}\class" />
	
	    <target name="info"> 
			<echo>"Hello World with Ant. Try compile, jar and run!"</echo> 
		</target>
	
	    <target name="compile" >
	        <mkdir dir="${class.dir}" />
	        <javac srcdir="src" destdir="${class.dir}" includeantruntime="false"/>
	    </target>

	    <target name="jar" depends="compile">
	        <mkdir dir="${jar.dir}" />
	        <jar destfile="${jar.dir}\HelloWorld.jar" basedir="${class.dir}">
	            <manifest>
	                <attribute name="Main-Class" value="oata.HelloWorld" />
	            </manifest>
	        </jar>
	    </target>
	
	    <target name="run" depends="jar">
	        <java jar="${jar.dir}\HelloWorld.jar" fork="true" />
	    </target>
	
	    <target name="clean">
		    <delete includeEmptyDirs="true">
		        <fileset dir="${debug.dir}" includes="**/*"/>
		    </delete>
	    </target>
	</project>


##3.深入Ant
Apache Ant的官方文档中有对所有task的详细说明，请参阅
[http://ant.apache.org/manual/tasksoverview.html](http://ant.apache.org/manual/tasksoverview.html)

###3.1关于指令`target`

1)复杂依赖关系  
指令的依赖(`depends`)属性保证该指令执行前所有的依赖项都会至少被执行过一次。  

在Ant中，一个target可以有多个依赖关系，用逗号分隔，例如：

	<target name="A"/>
	<target name="B" depends="A"/>
	<target name="C" depends="B"/>
	<target name="D" depends="C,B,A"/>

其中指令B依赖于A，C依赖于B，D依赖于C,B,A  
当一个指令有多个依赖项时，Ant会尝试从左向右执行依赖项。在执行依赖项时，若依赖项也存在依赖关系，则会以递归地方式执行依赖项。例如，在上述文件设定的环境中直接执行 `ant D`，最终的执行顺序为：

	Call-Graph:  A --> B --> C --> D

在解析D的依赖关系时，先要执行C；而执行C需要先执行B；执行B需要先执行A。 因此会按照A-B-C的顺序执行依赖项。当依赖项C完成时，ant检查D的其他依赖项，发现B和A都已经被执行了。此时则可以直接执行D。

2）`if/unless`属性  
指令（`target`)以及其他一些任务（包括`fail`,`junit`等等），可以设定`if`或`unless`属性，使其只在特定满足（或不满足）特定条件时执行。 

+ if的值为已定义的property名称或值为true的表达式时，允许指令执行
+ unless的值为未定义的property名称或值为false的表达式时，允许指令执行  

（关于property后文有更多介绍）。  

例如：

	<target name="-check-use-file" unless="file.exists">
	    <available property="file.exists" file="some-file"/>
	</target>
	<target name="use-file" depends="-check-use-file" if="file.exists">
	    <!-- do something requiring that file... -->
	</target>
	<target name="lots-of-stuff" depends="use-file,other-unconditional-stuff"/>

有三个指令`-check-use-file`，`use-file`和`lots-of-stuff`，并涉及到名为`file.exists`的property。如果直接执行`lots-of-stuff`，Ant会：

+ 根据依赖项执行`use-file`
+ 执行`use-file`时，根据依赖关系，先执行`-check-use-file`
+ 因为`file.exists`不存在（之前没有定义），因此unless将允许运行`-check-use-file`
	+ available任务会检查指定的文件`some-file`是否存在。如果存在就将`file.exists`设为“true”，否则就设为未定义状态（即不存在）
+ 返回`use-file`指令，如果`file.exists`存在，ant会继续执行指令。否则就会跳过`use-file`指令
+ 返回`lots-of-stuff`指令。该指令为空，不做操作



###3.2关于property
首先要明确的是property和attribute（属性）是有很大区别的。 Property类似于一般程序里面的变量。而attribute按照XML的语法是某个标签的组成部分，在Ant的语境下作为指令（target）或任务（task）的额外参数而存在。

定义property的方法很多，最常见的是同名的任务`property`,例如前文出现过的

	<property name="class.dir" value="${debug.dir}\class" />

其他还有很多任务task可以设定property，如前文提到的`available`

使用`${property_name}`来访问property对应的值


###3.3关于资源集合（resource collection）
资源集合指的是一类指向多个资源（文件、路径等）的实体，常见的包括`fileset`,`filelist`,`dirset`,`path` 等等。下文将介绍一部分常用的资源集合。Apache Ant的官方文档有对所有资源集合的详细说明：[http://ant.apache.org/manual/Types/resources.html#collection](http://ant.apache.org/manual/Types/resources.html#collection)

####3.3.1 Fileset
Fileset通常指向一组符合特定条件的文件。

1） `file`属性指向单个文件
	
	<fileset file="somefile" \>
2) `dir`属性指向一个目录。如果没有其他限制条件则指向该文件夹及其子文件夹下所有文件。  
需要注意的是，一个fileset**有且只能有**file或dir这两者中的一个。  
`dir`可以配合`includes` `excludes`属性（attribute）以及嵌套的`include` `exclude` 元素来规定包含、排除某些特定文件。`includes`指定被包含的文件，`excludes`则会排除符合条件的文件。 若`includes` `excludes`两者都没有设定，则会包含所有文件。

例如：

	<fileset dir="${server.src}">
	 	<include name="**/*.java"/>
		<exclude name="**/*Test*"/>
	</fileset>
指向`${server.src}`目录下所有名字中不含Test的java源文件

另外也可以使用嵌套的`filename元素`（任务）来指定文件特征，如

	<fileset dir="${server.src}" casesensitive="yes">
	  <filename name="**/*.java"/>
	  <filename name="**/*Test*" negate="true"/>
	</fileset>

以及

	<fileset dir="${server.src}" casesensitive="yes">
	  <filename name="**/*.java"/>
	  <not>
	    <filename name="**/*Test*"/>
	  </not>
	</fileset>

两者和上面的例子效果相同

####3.3.2 Dirset
Dirset是一组目录的集合，使用方法类似于fileset。详细请参考下述范例

	<dirset dir="${build.dir}">
		<include name="apps/**/classes"/>
		<exclude name="apps/**/*Test*"/>
	</dirset>


包含`${build.dir}/apps`所有名为class的文件夹，并排除路径中有Test的文件夹

<br />
**建议在使用Dirset之前先进行充分的测试以确保文件安全**

####3.3.3 Filelist
Filelist用于选取一批指定名称的文件。这些名称对应的文件可以存在也可以不存在，ant在解析时只会返回存在的文件。应当注意的是filelist不同于fileset，不接受通配符等文件名匹配规则。 具体请参考下列范例

1）尝试选取${doc.src}文件夹下的foo.xml和bar.xml。

	<filelist  id="docfiles" dir="${doc.src}"  files="foo.xml,bar.xml"/>
 
2）效果同上
	
	<filelist  id="docfiles" dir="${doc.src}" files="foo.xml bar.xml"/> 

3）如果上述例子已经在文件中出现过了，则可以通过其id进行调用（关于id请参考后文常见attribute一节）

	<filelist refid="docfiles"/> 
4）用file元素（任务）代替files，效果同上

	<filelist id="docfiles" dir="${doc.src}">
	    <file name="foo.xml"/>
	    <file name="bar.xml"/>
	</filelist>


<br />

###3.4关于true和false值
在Ant中部分attribute是布尔类型的，其中：    

+ `true` `yes` `on` 会被认为是true
+ `false` `no` `off` 会被认为是false

同义项之间可以相互交换不影响解析

###3.5常见attribute

在Apache ant中，所有任务task都可以有下述三个attribute

+ `id` 即全文中独一无二的识别标记。在其他同类的task标签可以用refid的attribute来引用该任务
+ `taskname`用于重命名**当前**任务，使得ant在执行该任务时输出不同的名称。设定taskname不会影响其他任务，也不会影响当前任务的行为
+ `description` 对任务本身没有任何影响，主要用于为当前任务提供注释文本

###3.6 操作文件

####3.6.1 拼接文件
`Concat`任务可以将指定的多个文件内容进行拼接，并存入指定文件或输出至stdout。具体用法请参考下列示例

1)向文件`README`写入“Hello, World!”

	<concat destfile="README">Hello, World!</concat>
2)拼接fileset中的所有文件并输出至stdout

	  <concat>
	    <fileset dir="messages" includes="*important*"/>
	  </concat>
3）将filelist中的文件拼接至destfile的末端
	  <concat destfile="NOTES" append="true">
	    <filelist dir="notes" files="note.txt"/>
	  </concat>

####3.6.2 复制文件
使用copy任务实现对文件和文件夹的复制，具体用法请参考下列示例

1）复制单个文件
	
	 <copy file="myfile.txt" tofile="mycopy.txt"/>
2)复制文件夹

	  <copy todir="../new/dir">
	    <fileset dir="src_dir"/>
	  </copy>
3）复制一组文件

	  <copy todir="../dest/dir">
	    <fileset dir="src_dir">
	      <exclude name="**/*.java"/>
	    </fileset>
	  </copy>
	
	  <copy todir="../dest/dir">
	    <fileset dir="src_dir" excludes="**/*.java"/>
	  </copy>

####3.6.3移动文件
使用 `move`任务来移动或重命名文件和文件夹，用法与copy类似。详见`https://ant.apache.org/manual/Tasks/move.html`

####3.6.4 删除文件
使用`delete`任务删除文件和文件夹，例如

1）删除单个文件

	<delete file="/lib/ant.jar"/>
2）删当前文件夹下及其子文件夹下所有的.bak文件；不删除目录

	<delete>
	  	<fileset dir="." includes="**/*.bak"/>
	</delete>

3）删除build文件夹下的所有文件和子文件夹，不删除build文件夹本身

	<delete includeemptydirs="true">
		<fileset dir="build" includes="**/*"/>
	</delete>
将`includeemptydirs`设为true将删除空目录。将includes设为`**/*/`来排除顶层目录

4）删除build文件夹下的所有文件和子文件夹，并删除build文件夹本身

	<delete includeEmptyDirs="true">
    		<fileset dir="build"/>
	</delete>



####3.6.5创建文件
使用`touch`任务创建文件。如果目标文件已经存在则更新最后修改时间（modification time）。  
例如：

1）创建单个文件，如果文件存在则更新其最后修改时间为当前时间

	 <touch file="myfile"/>

2）尝试创建单个文件，并设定最后修改时间为指定时间

	 <touch file="myfile" datetime="06/28/2000 14:02 "/>

3)更新src_dir文件夹下所有文件的最后修改时间为指定时间

	<touch datetime="09/10/1974 4:30 pm">
		<fileset dir="src_dir"/>
	</touch>


####3.6.6创建目录

使用`mkdir`创建目录,例如

	<mkdir dir="${dist}/lib"/>





<br />