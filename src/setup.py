from database import Database

CREATE_TABLE_QUERY = """
CREATE TABLE cf_features (
    id         integer PRIMARY KEY,
    key        text    NOT NULL,
    y_list     text    NOT NULL,
    y_features text    NOT NULL,
    x_list     text    NOT NULL,
    x_features text    NOT NULL
);
CREATE INDEX index_cf_features_on_key ON cf_features (key);
"""

def run_query(query):
    connection = Database.get_connection()
    print("Running create table query...\n{}".format(CREATE_TABLE_QUERY))
    cur = connection.cursor()
    cur.execute(query)
    cur.close()
    connection.commit()
    print("Finish creation of cf_features table!")

run_query(CREATE_TABLE_QUERY)
