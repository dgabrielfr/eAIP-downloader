import psycopg2

# Caution to set the correct database name!
# On Windows, default user is "postgres" with the "postgres" database
def postgresql_connection():
    """
    Test the connection to PostgreSQL

    Args:
        

    Return:
          

    """
    conn = None
    try: 
        conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="psql")
        print('Connecting to PostgreSQL server')
        cur = conn.cursor()
        
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')