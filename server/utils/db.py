import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from threading import Lock
from pgvector.psycopg2 import register_vector

_pool = None
_pool_lock = Lock()

def _db_dsn() -> str:
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    user = os.getenv("PGUSER", os.getenv("USER", "postgres"))
    password = os.getenv("PGPASSWORD", "")
    dbname = os.getenv("PGDATABASE", "myapp")
    
    if password:
        return f"host={host} port={port} dbname={dbname} user={user} password={password}"
    else:
        return f"host={host} port={port} dbname={dbname} user={user}"

def _init_db():
    global _pool
    with _pool_lock:
        if _pool is None:
            _pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=_db_dsn())

def _conn():
    global _pool
    if _pool is None:
        _init_db()
    conn = _pool.getconn()
    conn.autocommit = True
    try:
        register_vector(conn)
    except:
        pass
    return conn

def _put_conn(conn):
    global _pool
    if _pool:
        _pool.putconn(conn)