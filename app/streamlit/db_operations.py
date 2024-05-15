from sqlalchemy.exc import SQLAlchemyError
import constants as CONSTANTS
from sqlalchemy import create_engine, text

def create_database_engine():
    """
    Creates and returns a SQLAlchemy engine using a connection string from constants.
    """
    try:
        connection_string = CONSTANTS.CONNECTION_STRING
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Failed to create database engine: {e}")
        return None

def remove_table():
    """
    Drops a specified table if it exists.
    """
    engine = create_database_engine()
    if engine:
        try:
            with engine.connect() as conn:
                with conn.begin():
                    drop_sql = f"DROP TABLE IF EXISTS {CONSTANTS.TABLE_NAME}"
                    conn.execute(text(drop_sql))
            return True
        except SQLAlchemyError as e:
            print(f"Failed to drop table: {e}")
            return False
    return False

def create_data_table():
    """
    Creates a new table with specified schema.
    """
    engine = create_database_engine()
    if engine:
        try:
            with engine.connect() as conn:
                with conn.begin():
                    create_sql = f"CREATE TABLE {CONSTANTS.TABLE_NAME} (text VARCHAR(1200), text_vector VECTOR(DOUBLE, 384))"
                    conn.execute(text(create_sql))
            return True
        except SQLAlchemyError as e:
            print(f"Failed to create table: {e}")
            return False
    return False

def verify_table_existence():
    """
    Checks if the specified table exists in the database.
    """
    engine = create_database_engine()
    if engine:
        try:
            with engine.connect() as conn:
                with conn.begin():
                    check_sql = f"SELECT 1 FROM {CONSTANTS.TABLE_NAME} WHERE 1=0"
                    conn.execute(text(check_sql))
            return True
        except SQLAlchemyError as e:
            print(f"Table check: Table does not exist")
            return False
    return False

def insert_table_data(df):
    """
    Inserts data from a DataFrame into the specified table.
    """
    engine = create_database_engine()
    if engine:
        try:
            with engine.connect() as conn:
                with conn.begin():
                    for index, row in df.iterrows():
                        insert_sql = text("""
                                INSERT INTO {table_name}
                                (text, text_vector)
                                VALUES (:text, TO_VECTOR(:text_vector))
                            """.format(table_name=CONSTANTS.TABLE_NAME))
                        conn.execute(insert_sql, {
                            'text': row['text'],
                            'text_vector': str(row['text_vector'])
                        })
            return True
        except SQLAlchemyError as e:
            print(f"Data insertion failed: {e}")
            return False
    return False

def perform_vector_search(question_embedding):
    """
    Searches the database table using vector search with the given question embedding.
    """
    engine = create_database_engine()
    if engine:
        try:
            search_sql = text("""
                SELECT TOP 10 text FROM {table_name}
                ORDER BY VECTOR_DOT_PRODUCT(text_vector, TO_VECTOR(:search_vector)) DESC
            """.format(table_name=CONSTANTS.TABLE_NAME))
            with engine.connect() as conn:
                with conn.begin():
                    results = conn.execute(search_sql, {'search_vector': str(question_embedding)}).fetchall()
                    return [result[0] for result in results]
        except SQLAlchemyError as e:
            print(f"Vector search failed: {e}")
            return []
    return []

def count_table_records():
    """
    Returns the count of records in the specified table.
    """
    engine = create_database_engine()
    if engine:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {CONSTANTS.TABLE_NAME}"))
            count = result.fetchone()[0]
            return count
    return 0

if __name__ == "__main__":
    if verify_table_existence():
        print("Table exists.")
    else:
        print("Table does not exist.")

    print("Attempting to remove existing table:", remove_table())
    print("Attempting to create table:", create_data_table())
    print("Verify table creation:", verify_table_existence())
    print("Record count in table:", count_table_records())
