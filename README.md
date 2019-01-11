# Airflow 在centos7环境的安装说明   
  
## 1、安装系统包  
  sudo yum install epel-release  
  sudo yum -y install gcc gcc-c++ libffi-devel mariadb-devel cyrus-sasl-devel python-devel  
  easy_install -U setuptools  
   
## 2、安装mysql  
  mysql一般默认安装了  
  配置：  
  创建数据库：airflow   create database airflow default character set utf8mb4 collate utf8mb4_unicode_ci;
  创建用户并授权：airflow  
  GRANT all privileges on airflow.* TO 'airflow'@'localhost' IDENTIFIED BY 'airflow';  
    
## 3、安装redis  
  yum install redis  
  开启redis服务  
  sudo systemctl start redis.server  
  测试redis安装成功  
  redis-cli ping  
  
## 4、安装virtualenv， virtualenvwrapper  
  ~/.bash_profile配置如下  
  export WORKON_HOME=$HOME/.virtualenvs  
  export PROJECT_HOME=$HOME/workspace  
  source /usr/bin/virtualenvwrapper.sh  
  workon py2  
      
## 5、安装Airflow  
  注意：用Python2，因为airflow[hdfs]依赖的snakebite不支持python3  
         
  安装airflow （kerberos模块，如果hadoop没使用kerberos认证服务，则不需安装）  
  pip install airflow[async,celery,crypto,druid,jdbc,hdfs,hive,kerberos,ldap,mysql,password,vertica]  
    
  使用CeleryExecutor模式（redis为broker）：  
  pip install futures  
  pip install redis  
  pip install -U "celery[redis]"  
  
  初始化db  
  airflow initdb  

## 6、增加Web UI登录用户  
  (py2) [airflow@AIRFLOW airflow]$ ipython  
  In [1]: import airflow  
  In [2]: from airflow import models, settings  
  In [3]: from airflow.contrib.auth.backends.password_auth import PasswordUser  
  In [4]: user = PasswordUser(models.User())  
  In [5]: user.username = 'airflow'  
  In [6]: user.email = 'airflow@airflow.com'  
  In [7]: user.password = '*******'  
  In [8]: session = settings.Session()  
  In [9]: session.add(user)  
  In [10]: session.commit()  
  In [11]: session.close()  
  In [12]: quit  
    
## 7、配置systemd来管理和监控airflow服务（start，stop，restart，status）  
     
  配置方法参考：https://github.com/apache/incubator-airflow/tree/master/scripts/systemd  
  或https://github.com/JazzChen/InstallAirflow/tree/master/airflow/script/systemd  
  
  (py2) [airflow@AIRFLOW systemd]$ ls  
    
  airflow  airflow.conf  airflow-flower.service  airflow-kerberos.service  airflow-scheduler.service  airflow-webserver.service  airflow-worker.service  
  调整依赖服务，用户/用户组，启动命令（注意使用python虚拟环境，启动命名较复杂）  

