# piggy
-----



Setup
=====

Currently, installation is only possible from source.

###pre-requisites

1. Oracle Java JDK 7
2. [Python v2.7.8](https://www.python.org/)
3. [Postgresql v9.1+](http://www.postgresql.org/)
4. [Multicorn v1.1.1](http://multicorn.readthedocs.org/en/latest/)
5. [Apache Spark v1.3.1](https://spark.apache.org/)

###installation
   
1. Export environment variables SPARK_HOME and PYTHONPATH to PostgreSQL,

    ```
       export SPARK_HOME=path to spark-1.3.1-bin-hadoop2.6
       export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
    ```
    
    Hack for yum installation of PostgreSQL is to update the file /lib/systemd/system/postgresql.service.
    Add the following,

    ```
    Environment=SPARK_HOME=path to spark-1.3.1-bin-hadoop2.6
    Environment=PYTHONPATH=path to spark-1.3.1-bin-hadoop2.6/python/:/python/:
    ```
2. Clone the repo and from the project directory, execute the following

    ```
        sudo python setup.py install
    ```
    
3. Start PostgreSQL, create a server with wrapper as 'pgsparky.SparkSQLWrapper'. 
 This can then be used to define a foreign table which uses json/parquet data
        
