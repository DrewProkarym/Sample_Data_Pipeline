def get_connection_string():
    username = ''
    password = ''
    host = ''
    port = ''
    database = ''
    return f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
