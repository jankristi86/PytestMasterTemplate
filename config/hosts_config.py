API_HOSTS = {
    "test": "http://localhost:10005/wp-json/wc/v3/",
    "dev": "",
    "prod": ""
}

WOO_API_HOSTS = {
    "test": "http://localhost:10005",
    "dev": "",
    "prod": ""
}

DB_HOST = {
    'machine1': {
        "test": {"host": "localhost",
                 "database": "local",
                 "table_prefix": "wp_",
                 "socket": None,
                 "port": 10006
                 },
        "dev": {
            "host": "localhost",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 10006
        },
        "prod": {
            "host": "localhost",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 10006
        },
    },
    'docker': {
        "test": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 10006
        },
        "dev": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 10006
        },
        "prod": {
            "host": "host.docker.internal",
            "database": "local",
            "table_prefix": "wp_",
            "socket": None,
            "port": 10006
        },
    },
}
