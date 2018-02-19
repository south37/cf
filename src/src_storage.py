from database import Database
import numpy as np
import re

class SrcStorage:
    def __init__(self):
        self.connection = Database.get_connection()

    def fetch_matrix(self, src, x, y, v):
        rows = self.fetch(src=src, x=x, y=y, v=v)
        return self.fetch_matrix_impl(rows=rows)

    def fetch_matrix_impl(self, rows):
        y_set = set()
        x_set = set()
        v_dict = {}
        for i, row in enumerate(rows):
            # NOTE(south37): prev is y, next is x.
            y = row[0]
            x = row[1]
            v = float(row[2])

            y_set.add(y)
            x_set.add(x)

            if y not in v_dict:
                v_dict[y] = {}
            v_dict[y][x] = v

        y_list = sorted(list(y_set))
        x_list = sorted(list(x_set))

        matrix = np.zeros((len(y_list), len(x_list)), dtype=np.float32)
        # NOTE: Used only for accesing index faster
        y_indices = dict([(y, i) for i, y in enumerate(y_list)])
        x_indices = dict([(x, i) for i, x in enumerate(x_list)])
        for y in v_dict:
            for x in v_dict[y]:
                i = y_indices[y]
                j = x_indices[x]
                matrix[i][j] = v_dict[y][x]

        return matrix, y_list, x_list

    def fetch(self, src, x, y, v):
        query = self.get_query(src=src, x=x, y=y, v=v)
        self.print_running_query(query)
        result = self.fetch_impl(query)
        self.print_finish_query()

        if v:
            return result
        else:
            return [(row[0], row[1], 1.0) for row in result]

    def fetch_impl(self, query):
        cur = self.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result

    # NOTE(south37): prev is y, next is x.
    SELECT_QUERY = """
        SELECT
            {},  -- y
            {}   -- x
        FROM
            {}   -- src
    """

    SELECT_V_QUERY = """
        SELECT
            {},  -- y
            {},  -- x
            {}   -- v
        FROM
            {}   -- src
    """

    def get_query(self, src, x, y, v):
        if v:
            return SrcStorage.SELECT_V_QUERY.format(
                    y,
                    x,
                    v,
                    src)
        else:
            return SrcStorage.SELECT_QUERY.format(
                    y,
                    x,
                    src)

    def print_running_query(self, query):
        splitted = query.split("\n")
        elimminated = map(lambda s: self.eliminate_pre8s(s), splitted)
        q = "\n".join(elimminated)
        print("Running query...\n{}".format(q))

    def eliminate_pre8s(self, s):
        return re.sub(r'^\s{8}', '', s)

    def print_finish_query(self):
        print("Finish query")
