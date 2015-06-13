###piggy
-----

A PostgreSQL plugin that lets you load data and execute queries using PySpark and SparkSQL.

####Setup

Currently, installation is only possible from source.

#####Pre-requisites

1. Oracle Java JDK 7
2. [Python v2.7.8](https://www.python.org/)
3. [PostgreSQL v9.1+](http://www.postgresql.org/)
4. [Multicorn v1.1.1](http://multicorn.readthedocs.org/en/latest/)
5. [Apache Spark v1.3.1](https://spark.apache.org/)

#####Installation
   
1. Export environment variables SPARK_HOME and PYTHONPATH to PostgreSQL,

    ```
    export SPARK_HOME=path to spark-1.3.1-bin-hadoop2.6
    export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
    ```
    
    Hack for yum installation of PostgreSQL is to update the file `/lib/systemd/system/postgresql.service`.
    Add the following,

    ```
    Environment=SPARK_HOME=path to spark-1.3.1-bin-hadoop2.6
    Environment=PYTHONPATH=path to spark-1.3.1-bin-hadoop2.6/python/:/python/:
    ```
2. Clone the repo and from the project directory, execute the following

    ```
    sudo python setup.py install
    ```
    
####Usage

1. Start PostgreSQL.
2. Create multicorn extension and spark server, execute
 
    ```
    CREATE EXTENSION IF NOT EXISTS multicorn;
    CREATE SERVER multicorn_spark_srv 
        foreign data wrapper multicorn options (
            wrapper 'pgsparky.SparkSQLWrapper');
    ```

3. Load data from Json file or Parquet File,
    
    ```
    CREATE FOREIGN TABLE people ( name varchar (50), age int) 
        server multicorn_spark_srv options(
         master 'local',
         sourceType 'jsonFile',
         file '/opt/data/people.json',
         table 'people');
    ```

    The possible options are:
    1. master - path to Spark master (required for creating SparkConf). Defaults to 'local'.
    2. sourceType - format of source to load data from.
       Currently, only two types are supported - 'jsonFile' and 'parquetFile'.
       Defaults to 'jsonFile'.
    3. file (required) - file path to load data from
    4. table (required) - the name of the table. 
    
4. Query the data
    
    ```
    SELECT * FROM people;
    ```



