def get_connection_string():
    username = 'postgres'
    password = 'Postgres1979!'
    host = 'localhost'
    port = '5432'
    database = 'sample_pipeline_database1'
    return f'postgresql+psycopg2:/{username}:{password}@{host}:{port}/{database}'