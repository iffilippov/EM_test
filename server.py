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
async def delete_workload(id: int):
    if id in database_mock['workloads'].keys():
        del database_mock['workloads'][id]
        return Response(
            200,
            content=Content(b"text/plain", b"Workload Deleted")
        )
    else:
        return Response(404, content=Content(b"text/plain", b"Not Found"))


@app.route("/migration", methods=["GET"])
async def get_migration():
    if len(database_mock['migrations']) > 0:
        return (
            'Mock database includes',
            len(database_mock['migrations']),
            'Migrations records'
        )
    else:
        return Response(204, content=Content(b"text/plain", b"No Content"))


@app.route("/migration", methods=["POST"])
async def add_migration(input: FromJSON[dict]):
    data = input.value
    keys: set = {'selected mount points', 'source ip', 'migration target'}

    if all(key in data.keys() for key in keys):
        selected_mount_points: list = []
        for mount_point in data['selected mount points']:
            selected_mount_points.append(
                classes.MountPoint(
                    mount_point['name'],
                    int(mount_point['size'])
                )
            )
        source: classes.Workload = None
        target_vm: classes.Workload = None
        for workload in database_mock['workloads'].values():
            if workload.ip == data['source ip']:
                source = workload
            elif workload.ip == data['migration target']['target ip']:
                target_vm = workload
        if not source or not target_vm:
            return Response(
                400,
                content=Content(b"text/plain", b"Bad Request")
            )
        try:
            cloud_credentials = classes.Credentials(
                data['migration target']['cloud credentials']['username'],
                data['migration target']['cloud credentials']['password'],
                data['migration target']['cloud credentials']['domain']
            )
            cloud_type: str = data['migration target']['cloud type']
        except Exception:
            return Response(
                    400,
                    content=Content(b"text/plain", b"Bad Request")
                )
        try:
            migration_target = classes.MigrationTarget(
                cloud_type,
                cloud_credentials,
                target_vm
            )
        except Exception:
            return Response(
                    400,
                    content=Content(b"text/plain", b"Bad Request")
                )
        if not database_mock['migrations']:
            id = 1
        else:
            id = max(database_mock['migrations'].keys()) + 1

        database_mock['migrations'][id] = classes.Migration(
            selected_mount_points,
            source,
            migration_target
        )
        return Response(
            201,
            content=Content(
                b"text/plain",
                b"Migration record succesfully created"
            )
        )
    else:
        return Response(400, content=Content(b"text/plain", b"Bad Request"))


@app.route("/migration/<int:id>", methods=["PUT"])
async def modify_migration(input: FromJSON[dict], id: int):
    data = input.value
    keys: set = {'selected mount points', 'source ip', 'migration target'}
    modification_flag: bool = False

    if id not in database_mock['workloads'].keys():
        return Response(404, content=Content(b"text/plain", b"Not Found"))
    else:
        migration_to_modify = database_mock['migrations'][id]

    # TBD. any or all
    if any(key in data.keys() for key in keys):
        if 'selected mount points' in data.keys():
            selected_mount_points: list = []
            for mount_point in data['selected mount points']:
                selected_mount_points.append(
                    classes.MountPoint(
                        mount_point['name'],
                        int(mount_point['size'])
                    )
                )
            migration_to_modify.selected_mount_points = selected_mount_points
            modification_flag = True

        if 'source ip' in data.keys():
            source: classes.Workload = None
            for workload in database_mock['workloads'].values():
                if workload.ip == data['source ip']:
                    source = workload
                    modification_flag = True
                    break
            migration_to_modify.source = source
            if not source:
                return Response(
                    400,
                    content=Content(b"text/plain", b"Bad Request")
                )

        if 'migration target' in data.keys():
            target_vm: classes.Workload = None
            for workload in database_mock['workloads'].values():
                if workload.ip == data['migration target']['target ip']:
                    target_vm = workload
                    break
            if not target_vm:
                return Response(
                    400,
                    content=Content(b"text/plain", b"Bad Request")
                )
            try:
                cloud_credentials = classes.Credentials(
                    data['migration target']['cloud credentials']['username'],
                    data['migration target']['cloud credentials']['password'],
                    data['migration target']['cloud credentials']['domain']
                )
                cloud_type: str = data['migration target']['cloud type']
            except Exception:
                return Response(
                        400,
                        content=Content(b"text/plain", b"Bad Request")
                    )
            try:
                migration_target = classes.MigrationTarget(
                    cloud_type,
                    cloud_credentials,
                    target_vm
                )
            except Exception:
                return Response(
                        400,
                        content=Content(b"text/plain", b"Bad Request")
                    )
            migration_to_modify.migration_target = migration_target
            modification_flag = True
    else:
        return Response(400, content=Content(b"text/plain", b"Bad Request"))

    if modification_flag is True:
        return Response(
            200,
            content=Content(b"text/plain", b"Migration Modified")
        )
    else:
        return Response(
            304,
            content=Content(b"text/plain", b"Migration Not Modified")
        )


@app.route("/migration/<int:id>", methods=["DELETE"])
async def delete_migration(id: int):
    if id in database_mock['migrations'].keys():
        del database_mock['migrations'][id]
        return Response(
            200,
            content=Content(b"text/plain", b"Migration Deleted")
        )
    else:
        return Response(
            404,
            content=Content(b"text/plain", b"Migration Not Found")
        )


@app.route("/migration/<int:id>/run", methods=["GET"])
async def run_migration(id: int):
    if id in database_mock['migrations'].keys():
        database_mock['migrations'][id].run()
        return Response(
            200,
            content=Content(b"text/plain", b"Migration Started")
        )
    else:
        return Response(
            404,
            content=Content(b"text/plain", b"Migration Not Found")
        )


@app.route("/migration/<int:id>/status", methods=["GET"])
async def check_migration_status(id: int):
    if id in database_mock['migrations'].keys():
        if database_mock['migrations'][id].migration_state == 'not started':
            return Response(
                200,
                content=Content(b"text/plain", b"Migration Not Started")
            )
        elif database_mock['migrations'][id].migration_state == 'running':
            return Response(
                200,
                content=Content(b"text/plain", b"Migration Running")
            )
        elif database_mock['migrations'][id].migration_state == 'success':
            return Response(
                200,
                content=Content(b"text/plain", b"Migration Finished")
            )
        else:
            return Response(
                500,
                content=Content(b"text/plain", b"Migration Error")
            )
    else:
        return Response(
            404,
            content=Content(b"text/plain", b"Migration Not Found")
        )
