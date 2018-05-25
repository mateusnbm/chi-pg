# CHI-PG (Author's Original Source Code)

### Instructions for macOS:

Performed on macOS 10.13.3 Beta (17D46a).

#### 1. Installing Eclipse:

Download installer [here](https://www.eclipse.org/downloads/). I've used version Neon.3 Release (4.6.3).

#### 2. Installing Hadoop:

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

#### 3. Configuring Eclipse project:



#### Configuring the environment:

1. Open the Project in Eclipse.
2. Right-click on the project in the Package Explorer Menu.
3. Click on Properties > Java Build Path > Libraries > Add External JARs.
4. Select the JARS within the following paths:

**"$HADOOP_PATH/share/hadoop/client/"**  
**"$HADOOP_PATH/share/hadoop/mapreduce/"**

#### Useful resources:

http://hadooprecipes.blogspot.com.br/2015/09/setting-up-hadoop-271-on-mac-os-x.html  
http://boatboat001.com/index.php/blogs/view/setting_up_a_hadoop_cluster_under_mac_os_x_mountain  
http://www.shabdar.org/hadoop-java/138-how-to-create-and-run-eclipse-project-with-a-mapreduce-sample.html  
https://hadoop.apache.org/docs/r2.8.3/api/org/apache/hadoop/conf/Configuration.html  

Because of import errors:

https://stackoverflow.com/questions/13109588/base64-encoding-in-java  
https://docs.oracle.com/javase/8/docs/api/java/util/Base64.Decoder.html  

Future:  

http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
