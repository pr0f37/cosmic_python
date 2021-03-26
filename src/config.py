def get_api_url():
    host = "127.0.0.1"
    port = "5000"
    return f"http://{host}:{port}"


def get_postgres_uri():
    user = "postgres"
    db_name = "cosmic"
    password = "pwd"
    host = "127.0.0.1"
    port = "5432"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
