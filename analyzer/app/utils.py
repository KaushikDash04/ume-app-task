from django.db import connection

def create_querylog_table():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_querylog (
                id SERIAL PRIMARY KEY,
                query TEXT NOT NULL,
                tone VARCHAR(50),
                intent VARCHAR(50),
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                suggested_actions JSONB
            );
        ''')