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

        try:
            self.file = options.get("file")
        except Exception, e:
            log_to_postgres('The file parameter is required.', ERROR)

        if 'table' not in options:
            log_to_postgres('table or query parameter is required.', ERROR)
        self.table = options.get("table", None)

        self.columns = columns
        self.sc = SparkContext(self.master, "pgSparky")
        self.sqlContext = SQLContext(self.sc)
        self.data = self.sqlContext.jsonFile(self.file)
        self.sqlContext.registerDataFrameAsTable(self.data, self.table)

    def execute(self, quals, columns):
        log_to_postgres(quals, DEBUG)

        def qualToString(qual):
            field = qual.field_name
            oper = qual.operator
            value = qual.value
            if isinstance(value, basestring):
                return field + oper + " '" + str(value) + "'"
            else:
                return field + oper + str(value)

        query = "SELECT " + ",".join(self.columns.keys()) + " FROM " + self.table
        whereClause = " AND ".join(map(str, quals))

        if not whereClause:
            query = query
        else:
            query = query + " WHERE " + whereClause

        result = self.sqlContext.sql(query)
        for row in result.collect():
            yield row
