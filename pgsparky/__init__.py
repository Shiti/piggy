from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres, ERROR, WARNING, DEBUG
from pyspark import SparkContext
from pyspark.sql import SQLContext


class SparkSQLWrapper(ForeignDataWrapper):
    def __init__(self, options, columns):
        super(SparkSQLWrapper, self).__init__(options, columns)

        if 'master' not in options:
            log_to_postgres('The master parameter is required and the default is local.', WARNING)
        self.master = options.get("master", "local")

        if 'sourceType' not in options:
            log_to_postgres('The sourceType parameter is required and the default is jsonFile.', WARNING)
        self.sourceType = options.get("sourceType", "jsonFile")

        try:
            self.file = options.get("file")
        except Exception, e:
            log_to_postgres('The file parameter is required.', ERROR)

        if 'table' not in options:
            log_to_postgres('The table parameter is required.', ERROR)
        self.table = options.get("table", None)

        self.columns = columns
        self.sc = SparkContext(self.master, "pgSparky")
        self.sqlContext = SQLContext(self.sc)

        if self.sourceType == 'jsonFile':
            self.data = self.sqlContext.jsonFile(self.file)
        elif self.sourceType == 'parquetFile':
            self.data = self.sqlContext.parquetFile(self.file)
        else:
            log_to_postgres('jsonFile and parquetFile are the only supported types.', ERROR)

        self.sqlContext.registerDataFrameAsTable(self.data, self.table)

    def execute(self, quals, columns):
        def qual_to_string(qual):
            value = qual.value
            if isinstance(value, basestring):
                return str(qual).replace(value, "'"+value+"'")
            else:
                return str(qual)

        query = "SELECT " + ",".join(self.columns.keys()) + " FROM " + self.table
        where_clause = " AND ".join(map(qual_to_string, quals))

        if not where_clause:
            query = query
        else:
            query = query + " WHERE " + where_clause

        log_to_postgres(query, DEBUG)
        result = self.sqlContext.sql(query)
        for row in result.collect():
            yield row
