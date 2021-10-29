import psycopg2


def get_db():
    return psycopg2.connect(host="localhost", dbname="books" , user="loki2", password="test123")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )
    db.commit()
    return db, cur 

