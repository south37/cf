import csv
from database import Database
from io import StringIO
import numpy as np

class FeatureStorage:
    FEATURE_TABLE = "cf_features"

    DELETE_QUERY = """
        DELETE FROM {} WHERE key = %s
    """.format(FEATURE_TABLE)

    INSERT_QUERY = """
         INSERT INTO {} (key, y_list, y_features, x_list, x_features) VALUES (%s, %s, %s, %s, %s)
    """.format(FEATURE_TABLE)

    SELECT_QUERY = """
        SELECT
            y_list,
            y_features,
            x_list,
            x_features
        FROM {}
        WHERE key = %s
    """.format(FEATURE_TABLE)

    def __init__(self):
        self.connection = Database.get_connection()

    def save(self, key, y_list, y_features, x_list, x_features):
        self.delete(key)
        self.insert(key, y_list, y_features, x_list, x_features)
        # NOTE: Commit of transaction is necessary
        self.connection.commit()

    def load(self, key):
        result = self.select(key)
        y_list     = self.unnest(self.csv_to_list(result[0]))
        y_features = np.asarray(self.csv_to_list(result[1]), dtype=np.float32)
        x_list     = self.unnest(self.csv_to_list(result[2]))
        x_features = np.asarray(self.csv_to_list(result[3]), dtype=np.float32)
        return y_list, y_features, x_list, x_features

    def delete(self, key):
        cur = self.connection.cursor()
        cur.execute(FeatureStorage.DELETE_QUERY, (key,))
        cur.close()

    def insert(self, key, y_list, y_features, x_list, x_features):
        y_list_s     = self.list_to_csv(self.nest(y_list))
        y_features_s = self.list_to_csv(y_features)
        x_list_s     = self.list_to_csv(self.nest(x_list))
        x_features_s = self.list_to_csv(x_features)

        cur = self.connection.cursor()
        cur.execute(FeatureStorage.INSERT_QUERY, (
            key,
            y_list_s,
            y_features_s,
            x_list_s,
            x_features_s))
        cur.close()

    def select(self, key):
        cur = self.connection.cursor()
        cur.execute(FeatureStorage.SELECT_QUERY, (key,))
        result = cur.fetchone()
        cur.close()
        return result

    def list_to_csv(self, l):
        io = StringIO()
        writer = csv.writer(io)
        writer.writerows(l)
        return io.getvalue()

    def csv_to_list(self, s):
        return list(csv.reader(StringIO(s)))

    def nest(self, l):
        return list(map(lambda x: [x], l))

    def unnest(self, l):
        return list(map(lambda x: x[0], l))
