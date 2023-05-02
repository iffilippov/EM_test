from datetime import datetime

from blacksheep import Application, Response, Content, FromJSON

import classes


app = Application()
test_ip: str = '192.168.0.1'
test_credentials = classes.Credentials('user', 'password', 'domain')
test_mount_point_1 = classes.MountPoint('C:\\', 100)
test_mount_point_2 = classes.MountPoint('D:\\', 200)
test_storage = [test_mount_point_1, test_mount_point_2]
test_workload = classes.Workload(test_ip, test_credentials, test_storage)
workload_list = [test_workload]

database_mock: dict = {'workloads': {}, 'migrations': {}}


@app.route("/workload", methods=["GET"])
async def get_workload():
    if len(database_mock['workloads']) > 0:
        return (
            'Mock database includes',
            len(database_mock['workloads']),
            'Workload records'
        )
    else:
        return Response(204, content=Content(b"text/plain", b"No Content"))


@app.route("/workload", methods=["POST"])
async def add_workload(input: FromJSON[dict]):

    data = input.value
    keys: set = {'ip', 'credentials', 'storage'}

    if all(key in data.keys() for key in keys):
        ip = data['ip']
        credentials = classes.Credentials(
            data['credentials']['username'],
            data['credentials']['password'],
            data['credentials']['domain']
        )
        storage = []
        for mount_point in data['storage']:
            storage.append(classes.MountPoint(
                mount_point['name'],
                int(mount_point['size'])
                )
            )

        if not database_mock['workloads']:
            id = 1
        else:
            id = max(database_mock['workloads'].keys()) + 1

        database_mock['workloads'][id] = classes.Workload(
            ip,
            credentials,
            storage
        )

        return Response(
            201,
            content=Content(
                b"text/plain",
                b"Workload record succesfully created"
            )
        )
    else:
        return Response(400, content=Content(b"text/plain", b"Bad Request"))


@app.route("/workload/{int:id}", methods=["PUT"])
async def modify_workload(input: FromJSON[dict], id: int):
    data = input.value
    modification_flag: bool = False
    ip = database_mock['workloads'][id].ip

    if id in database_mock['workloads'].keys():
        if 'credentials' in data.keys():
            credentials = classes.Credentials(
                data['credentials']['username'],
                data['credentials']['password'],
                data['credentials']['domain']
            )
            modification_flag = True

        if 'storage' in data.keys():
            storage = []
            for mount_point in data['storage']:
                storage.append(classes.MountPoint(
                    mount_point['name'], int(mount_point['size'])
                ))

        database_mock['workloads'][id] = classes.Workload(
            ip,
            credentials,
            storage
        )
    else:
        modification_flag = False
        return Response(404, content=Content(b"text/plain", b"Not Found"))

    if modification_flag is True:
        # print(database_mock['workloads'][id])
        return Response(
            200,
            content=Content(b"text/plain", b"Workload Modified")
        )
    else:
        return Response(
            304,
            content=Content(b"text/plain", b"Not Modified")
        )


@app.route("/workload/<int:id>", methods=["DELETE"])
async def delete_workload():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration", methods=["GET"])
async def get_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration", methods=["POST"])
async def add_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>", methods=["PUT"])
async def modify_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>", methods=["DELETE"])
async def delete_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>/run", methods=["GET"])
async def run_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>/status", methods=["GET"])
async def check_migration_status():
    return f"Hello, World! {datetime.utcnow().isoformat()}"
