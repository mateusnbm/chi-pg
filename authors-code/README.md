# CHI-PG (Author's Original Source Code)

### Instructions for macOS:

Performed on macOS 10.13.3 Beta (17D46a).

#### 1. Install Eclipse:

Download installer [here](https://www.eclipse.org/downloads/). I've used version Neon.3 Release (4.6.3).

#### 2. Install Hadoop:

Steps based on this [tutorial](http://hadooprecipes.blogspot.com.br/2015/09/setting-up-hadoop-271-on-mac-os-x.html).

##### 2.1 Java

Run the following command in a terminal:

```
$ java -version
```

If Java is already installed, you can see a similar result like:

```
$ java -version
java version "1.8.0_25"
Java(TM) SE Runtime Environment (build 1.8.0_25-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.25-b02, mixed mode)
```

If not, the terminal will prompt you for installation or you can download Java JDK [here](http://www.oracle.com/technetwork/java/javase/downloads/index.html).

##### 2.2 SSH

First enable Remote Login in System Preference -> Sharing.

Now check that you can ssh to the localhost without a passphrase:

```
$ ssh localhost
```

If you cannot ssh to localhost without a passphrase, execute the following commands:

```
$ ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
$ cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
```

##### 2.3 Download Hadoop:

You can download it from [Apache Download Mirror](http://www.apache.org/dyn/closer.cgi/hadoop/common/).

I've download version "3.1.0".

##### 2.4 Find Java home directory path:

Run the following copy and save the output path, we'll need it later.

```
$ /usr/libexec/java_home
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home
```

##### 2.5 Edit "hadoop-env.sh":

Open the file "etc/hadoop/hadoop-env.sh" in a text editor and uncomment the following lines:

```
export JAVA_HOME={your java home directory}
export HADOOP_PREFIX={your hadoop distribution directory}
```

Then replace "{your java home directory}" and "{your hadoop distribution directory}" with the correct paths.

##### 2.6 Test:

Type the following commands in a terminal window.

```
cd {your hadoop distribution directory}
$ bin/hadoop
```

This will display the usage documentation for the hadoop script.

##### 2.7: Edit configuration files:

Edit "etc/hadoop/core-site.xml":

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

Edit "etc/hadoop/hdfs-site.xml":

```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

Edit "etc/hadoop/mapred-site.xml":

```
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>

    <property>
      <name>yarn.app.mapreduce.am.env</name>
      <value>HADOOP_MAPRED_HOME={your hadoop distribution directory}</value>
    </property>
    <property>
      <name>mapreduce.map.env</name>
      <value>HADOOP_MAPRED_HOME={your hadoop distribution directory}</value>
    </property>
    <property>
      <name>mapreduce.reduce.env</name>
      <value>HADOOP_MAPRED_HOME={your hadoop distribution directory}</value>
    </property>
</configuration>
```

Edit "etc/hadoop/yarn-site.xml":

```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

##### 2.8: Wrapping up:

Run the following commands:

```
$ cd {your hadoop distribution directory}
$ bin/hdfs namenode -format
$ sbin/start-dfs.sh
$ bin/hdfs dfs -mkdir /user
$ bin/hdfs dfs -mkdir /user/{username} #make sure you add correct username
$ sbin/start-yarn.sh
```

If no errors arise, you should be able to access the following urls:

http://localhost:9870/  
http://localhost:8088/

If nothing shows up, try the other ports suggested [here](https://stackoverflow.com/questions/19641326/http-localhost50070-does-not-work-hadoop).

#### 3. Configuring the Project:

Download this repository and place the authors-code in a convenient location.

Fire Eclise and open the project from "authors-code/eclipse".

If multiple import errors arise, do "Right-click project > Propoerties > Java Build Path > Libraries > Add External JARs." and add the jars from the following paths:

{your hadoop distribution directory}/share/hadoop/client/  
{your hadoop distribution directory}/share/hadoop/mapreduce/

#### 4. Run:

Do the following in order to generate a jar "Right-click project > Export > JAR file > Next > Finish".

Place the jar in the "authors-code" folder.

Open a new terminal window and run the following commands:

```
$ cd {your hadoop distribution directory}
$ bin/hadoop fs -ls hdfs://localhost:9000/
$ bin/hadoop fs -ls hdfs://localhost:9000/user/
```

You should see something like this:

```
Found 1 items
drwxr-xr-x   - mateusnbm supergroup          0 2018-05-24 19:58 hdfs://localhost:9000/user
Found 1 items
drwxr-xr-x   - mateusnbm supergroup          0 2018-05-25 12:37 hdfs://localhost:9000/user/{your username}
```

Now we need to copy our example folder ("authors-code/example/") to Hadoop filesystem, run:

```
$ bin/hdfs dfs -put {path to authors-code}/example/ example
```

We got everything need, it's time to run the application. Open a new terminal and run:

```
$ cd {your authors-code folder}
$ {your hadoop distribution directory}/bin/hadoop jar chipg.jar es.unavarra.chi_pr.mapreduce.MapReduceLauncher hdfs://localhost:9000 /user/{your username}/example/config.txt /user/{your username}/example/header_example.header /user/{your username}/example/data_example.data /user/{your username}/example/output
```

You should see an output like this:

```
$ /Users/mateusnbm/hadoop-3.1.0/bin/hadoop jar chipg.jar es.unavarra.chi_pr.mapreduce.MapReduceLauncher hdfs://localhost:9000 /user/mateusnbm/example/config.txt /user/mateusnbm/example/header_example.header /user/mateusnbm/example/data_example.data /user/mateusnbm/example/output
2018-05-25 12:37:57,143 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
^HERE^
2018-05-25 12:37:58,017 INFO client.RMProxy: Connecting to ResourceManager at /0.0.0.0:8032
2018-05-25 12:37:58,387 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/mateusnbm/.staging/job_1527258693441_0008
2018-05-25 12:37:58,482 INFO input.FileInputFormat: Total input files to process : 1
2018-05-25 12:37:58,518 INFO mapreduce.JobSubmitter: number of splits:32
2018-05-25 12:37:58,544 INFO Configuration.deprecation: yarn.resourcemanager.system-metrics-publisher.enabled is deprecated. Instead, use yarn.system-metrics-publisher.enabled
2018-05-25 12:37:58,623 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1527258693441_0008
2018-05-25 12:37:58,624 INFO mapreduce.JobSubmitter: Executing with tokens: []
2018-05-25 12:37:58,740 INFO conf.Configuration: resource-types.xml not found
2018-05-25 12:37:58,740 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2018-05-25 12:37:58,784 INFO impl.YarnClientImpl: Submitted application application_1527258693441_0008
2018-05-25 12:37:58,807 INFO mapreduce.Job: The url to track the job: http://mateuss-mbp.home:8088/proxy/application_1527258693441_0008/
2018-05-25 12:37:58,807 INFO mapreduce.Job: Running job: job_1527258693441_0008
2018-05-25 12:38:03,874 INFO mapreduce.Job: Job job_1527258693441_0008 running in uber mode : false
2018-05-25 12:38:03,876 INFO mapreduce.Job:  map 0% reduce 0%
2018-05-25 12:38:10,948 INFO mapreduce.Job:  map 9% reduce 0%
2018-05-25 12:38:11,956 INFO mapreduce.Job:  map 19% reduce 0%
2018-05-25 12:38:30,086 INFO mapreduce.Job:  map 34% reduce 0%
2018-05-25 12:38:39,147 INFO mapreduce.Job:  map 34% reduce 1%
2018-05-25 12:38:45,180 INFO mapreduce.Job:  map 47% reduce 1%
2018-05-25 12:38:51,223 INFO mapreduce.Job:  map 47% reduce 2%
2018-05-25 12:38:56,262 INFO mapreduce.Job:  map 47% reduce 4%
2018-05-25 12:38:58,274 INFO mapreduce.Job:  map 50% reduce 4%
2018-05-25 12:38:59,282 INFO mapreduce.Job:  map 59% reduce 4%
2018-05-25 12:39:03,320 INFO mapreduce.Job:  map 59% reduce 5%
2018-05-25 12:39:11,367 INFO mapreduce.Job:  map 69% reduce 5%
2018-05-25 12:39:15,396 INFO mapreduce.Job:  map 69% reduce 6%
2018-05-25 12:39:20,426 INFO mapreduce.Job:  map 72% reduce 6%
2018-05-25 12:39:21,433 INFO mapreduce.Job:  map 72% reduce 9%
2018-05-25 12:39:22,442 INFO mapreduce.Job:  map 78% reduce 9%
2018-05-25 12:39:27,473 INFO mapreduce.Job:  map 78% reduce 10%
2018-05-25 12:39:30,490 INFO mapreduce.Job:  map 81% reduce 10%
2018-05-25 12:39:31,495 INFO mapreduce.Job:  map 88% reduce 10%
2018-05-25 12:39:33,505 INFO mapreduce.Job:  map 88% reduce 11%
2018-05-25 12:39:40,541 INFO mapreduce.Job:  map 91% reduce 11%
2018-05-25 12:39:41,549 INFO mapreduce.Job:  map 97% reduce 11%
2018-05-25 12:39:45,578 INFO mapreduce.Job:  map 97% reduce 12%
2018-05-25 12:39:50,611 INFO mapreduce.Job:  map 100% reduce 21%
2018-05-25 12:39:51,619 INFO mapreduce.Job:  map 100% reduce 63%
2018-05-25 12:40:06,712 INFO mapreduce.Job:  map 100% reduce 88%
2018-05-25 12:40:07,717 INFO mapreduce.Job:  map 100% reduce 100%
2018-05-25 12:40:07,722 INFO mapreduce.Job: Job job_1527258693441_0008 completed successfully
2018-05-25 12:40:07,778 INFO mapreduce.Job: Counters: 50
	File System Counters
		FILE: Number of bytes read=97210
		FILE: Number of bytes written=9223426
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=129950
		HDFS: Number of bytes written=3718
		HDFS: Number of read operations=136
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=88
	Job Counters 
		Killed reduce tasks=1
		Launched map tasks=32
		Launched reduce tasks=8
		Data-local map tasks=32
		Total time spent by all maps in occupied slots (ms)=154046
		Total time spent by all reduces in occupied slots (ms)=247313
		Total time spent by all map tasks (ms)=154046
		Total time spent by all reduce tasks (ms)=247313
		Total vcore-milliseconds taken by all map tasks=154046
		Total vcore-milliseconds taken by all reduce tasks=247313
		Total megabyte-milliseconds taken by all map tasks=157743104
		Total megabyte-milliseconds taken by all reduce tasks=253248512
	Map-Reduce Framework
		Map input records=100
		Map output records=100
		Map output bytes=130900
		Map output materialized bytes=98698
		Input split bytes=4064
		Combine input records=100
		Combine output records=74
		Reduce input groups=23
		Reduce shuffle bytes=98698
		Reduce input records=74
		Reduce output records=5
		Spilled Records=148
		Shuffled Maps =256
		Failed Shuffles=0
		Merged Map outputs=256
		GC time elapsed (ms)=2113
		CPU time spent (ms)=0
		Physical memory (bytes) snapshot=0
		Virtual memory (bytes) snapshot=0
		Total committed heap usage (bytes)=9135194112
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters 
		Bytes Read=125886
	File Output Format Counters 
		Bytes Written=1774

Prototypes built. Parameters:

	Number of linguistic labels: 4
	Minimum number of examples per prototype: 3
	Aggregation: arithmetic mean (single class)
	Number of mappers: 32
	Number of reducers: 8

Writing to disk...
hdfs://localhost:9000//user/mateusnbm/example/output/_TMP
hdfs://localhost:9000//user/mateusnbm/example/output/prototypes.txt
hdfs://localhost:9000//user/mateusnbm/example/output/time
hdfs://localhost:9000//user/mateusnbm/example/output/time.txt
Done.
```

#### Useful commands:

```
$ /Users/mateusnbm/hadoop-3.1.0/bin/hadoop jar chipg.jar es.unavarra.chi_pr.mapreduce.MapReduceLauncher hdfs://localhost:9000 /user/mateusnbm/example/config.txt /user/mateusnbm/example/header_example.header /user/mateusnbm/example/data_example.data /user/mateusnbm/example/output  
$ bin/hdfs dfs -put /Users/mateusnbm/Desktop/chipg/example/ example  
$ bin/hadoop fs -rmr hdfs://localhost:9000/user/mateusnbm/example  
$ bin/hadoop fs -ls hdfs://localhost:9000/user/mateusnbm/example/output/  
$ bin/hadoop fs -get hdfs://localhost:9000/user/mateusnbm/example/output/ /Users/mateusnbm/Desktop  
```

#### Useful resources:

http://hadooprecipes.blogspot.com.br/2015/09/setting-up-hadoop-271-on-mac-os-x.html  
http://boatboat001.com/index.php/blogs/view/setting_up_a_hadoop_cluster_under_mac_os_x_mountain  
http://www.shabdar.org/hadoop-java/138-how-to-create-and-run-eclipse-project-with-a-mapreduce-sample.html  
https://hadoop.apache.org/docs/r2.8.3/api/org/apache/hadoop/conf/Configuration.html  

https://stackoverflow.com/questions/13109588/base64-encoding-in-java  
https://docs.oracle.com/javase/8/docs/api/java/util/Base64.Decoder.html  

http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
