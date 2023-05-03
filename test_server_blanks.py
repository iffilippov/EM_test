# Endpoint strings for requests
WORKLOADS_ENDPOINT: str = 'http://127.0.0.1:44777/workload'

WORKLOAD_1_ENDPOINT: str = 'http://127.0.0.1:44777/workload/1'
WORKLOAD_2_ENDPOINT: str = 'http://127.0.0.1:44777/workload/2'
WORKLOAD_3_ENDPOINT: str = 'http://127.0.0.1:44777/workload/3'
WORKLOAD_4_ENDPOINT: str = 'http://127.0.0.1:44777/workload/5'

MIGRATIONS_ENDPOINT: str = 'http://127.0.0.1:44777/migration'

MIGRATION_1_ENDPOINT: str = 'http://127.0.0.1:44777/migration/1'
MIGRATION_2_ENDPOINT: str = 'http://127.0.0.1:44777/migration/1'
MIGRATION_3_ENDPOINT: str = 'http://127.0.0.1:44777/migration/3'
MIGRATION_4_ENDPOINT: str = 'http://127.0.0.1:44777/migration/4'

RUN_MIGRATION_1_ENDPOINT: str = 'http://127.0.0.1:44777/migration/1/run'
RUN_MIGRATION_2_ENDPOINT: str = 'http://127.0.0.1:44777/migration/2/run'
RUN_MIGRATION_3_ENDPOINT: str = 'http://127.0.0.1:44777/migration/2/run'
RUN_MIGRATION_4_ENDPOINT: str = 'http://127.0.0.1:44777/migration/4/run'

MIGRATION_1_STATUS_ENDPOINT: str = 'http://127.0.0.1:44777/migration/1/status'
MIGRATION_2_STATUS_ENDPOINT: str = 'http://127.0.0.1:44777/migration/2/status'
MIGRATION_3_STATUS_ENDPOINT: str = 'http://127.0.0.1:44777/migration/3/status'
MIGRATION_4_STATUS_ENDPOINT: str = 'http://127.0.0.1:44777/migration/4/status'

# JSON for requests
WORKLOAD_1: dict = {
    "ip": "192.168.1.1",
    "credentials": {
        "username": "user1",
        "password": "pass1",
        "domain": "domain1"
    },
    "storage": [
        {
            "name": "c:",
            "size": "1000"
        },
        {
            "name": "d:",
            "size": "1000"
        }
    ]
}
WORKLOAD_2: dict = {
    "ip": "192.168.1.2",
    "credentials": {
        "username": "user2",
        "password": "pass2",
        "domain": "domain2"
    },
    "storage": [
        {
            "name": "c:",
            "size": "1000"
        },
        {
            "name": "d:",
            "size": "1000"
        }
    ]
}
WORKLOAD_3: dict = {
    "ip": "192.168.1.3",
    "credentials": {
        "username": "user3",
        "password": "pass3",
        "domain": "domain3"
    },
    "storage": [
        {
            "name": "c:",
            "size": "1000"
        },
        {
            "name": "d:",
            "size": "1000"
        }
    ]
}
WORKLOAD_4: dict = {
    "ip": "192.168.1.3",
    "credentials": {
        "username": "user3",
        "password": "pass3",
        "domain": "domain3"
    }
}
WORKLOAD_3_MODIFIED: dict = {
    "ip": "192.168.1.100",
    "credentials": {
        "password": "pass2",
        "domain": "domain2",
        "username": "user2"
    },
    "storage": [
        {
            "name": "c:",
            "size": "1000"
        },
        {
            "name": "d:",
            "size": "1000"
        }
    ]
}
WORKLOAD_2_NOT_MODIFIED: dict = {
    "ip": "192.168.1.2"
}
MIGRATION_1: dict = {
    "source ip": "192.168.1.2",
    "migration target": {
        "target ip": "192.168.1.1",
        "cloud credentials": {
            "username": "user",
            "password": "pass",
            "domain": "domain"
        },
        "cloud type": "aws"
    },
    "selected mount points": [
        {
            "name": "c:",
            "size": "1000"
        }
    ]
}
MIGRATION_2: dict = {
    "source ip": "192.168.1.1",
    "migration target": {
        "target ip": "192.168.1.2",
        "cloud credentials": {
            "username": "user",
            "password": "pass",
            "domain": "domain"
        },
        "cloud type": "aws"
    },
    "selected mount points": [
        {
            "name": "c:",
            "size": "1000"
        }
    ]
}
MIGRATION_3: dict = {
    "source ip": "192.168.1.2",
    "migration target": {
        "target ip": "192.168.1.1",
        "cloud credentials": {
            "username": "user",
            "password": "pass",
            "domain": "domain"
        },
        "cloud type": "aws"
    },
    "selected mount points": [
        {
            "name": "c:",
            "size": "1000"
        }
    ]
}
MIGRATION_4: dict = {
    "source ip": "192.168.1.3",
    "migration target": {
        "target ip": "192.168.1.1",
        "cloud credentials": {
            "username": "user",
            "password": "pass",
            "domain": "domain"
        },
        "cloud type": "aws"
    },
    "selected mount points": [
        {
            "name": "c:",
            "size": "1000"
        }
    ]
}
MIGRATION_5: dict = {
    "source ip": "192.168.1.3",
    "migration target": {
        "target ip": "192.168.1.1",
        "cloud credentials": {
            "username": "user",
            "password": "pass",
            "domain": "domain"
        },
        "cloud type": "aws"
    }
}
MIGRATION_3_MODIFIED: dict = {
    "source ip": "192.168.1.1",
    "migration target": {
        "target ip": "192.168.1.2",
        "cloud credentials": {
            "username": "user",
            "password": "pass",
            "domain": "domain"
        },
        "cloud type": "aws"
    },
    "selected mount points": [
        {
            "name": "c:",
            "size": "1000"
        }
    ]
}
