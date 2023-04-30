import os
import pickle
import time


class Credentials():
    '''Implements Credentials.'''

    def __init__(
            self,
            username: str,
            password: str,
            domain: str,
    ):
        if (
            isinstance(username, str)
            and isinstance(password, str)
            and isinstance(domain, str)
        ):
            self.username = username
            self.password = password
            self.domain = domain
        else:
            raise TypeError('Wrong attributes types')

    def __repr__(self):
        return (
            f'username - {self.username};'
            f' password - {self.password};'
            f' domain - {self.domain}'
        )


class MountPoint():
    '''Implements MountPoint.'''

    def __init__(
            self,
            mount_point_name: str,
            total_size: int,
    ):
        if isinstance(mount_point_name, str) and isinstance(total_size, int):
            self.mount_point_name = mount_point_name
            self.total_size = total_size
        else:
            raise TypeError('Wrong attributes types')

    def __repr__(self):
        return (
            f' mount point name - {self.mount_point_name};'
            f' total size - {self.total_size} '
        )


class Workload():
    '''Impements Workload.'''

    def __init__(
            self,
            ip: str,
            credentials: Credentials,
            storage: list[MountPoint],
    ):
        if not ip or not credentials or not storage:
            raise ValueError('Missing required fields')
        elif (
            isinstance(ip, str)
            and isinstance(credentials, Credentials)
            and isinstance(storage, list)
            and all(isinstance(item, MountPoint) is True for item in storage)
        ):
            self.ip = ip
            self.credentials = credentials
            self.storage = storage
        else:
            raise TypeError('Wrong attributes types')

    def __repr__(self):
        return (
            f'Workloads\n'
            f'IP: {self.ip};\n'
            f'Credentials: {self.credentials};\n'
            f'Storage: {self.storage}'
        )


class Source():
    '''Implements Source.
    Not sure for what. It is not used in business logic.
    Should it be connected/inherited with Workload class
    and Source object in the Migration class? TBD'''

    def __init__(
            self,
            username: str,
            password: str,
            ip: str,
    ):
        if not ip or not username or not password:
            raise ValueError(
                'Attributes of the Source class cannot be of type None'
            )
        elif (
            isinstance(username, str)
            and isinstance(password, str)
            and isinstance(ip, str)
        ):
            self.username = username
            self.password = password
            self.ip = ip
        else:
            raise TypeError('Wrong attributes types')

    def __repr__(self):
        return (
            f' source username: {self.username};'
            f' source password: {self.password};'
            f' source IP: {self.ip};'
        )

    # def change_ip(self, ip):
    #     if ip is None:
    #         raise ValueError
    #     if self.__change_ip_possible:
    #         self.__ip = ip

    # def change_username(self, username):
    #     if username is None:
    #         raise ValueError
    #     self.__username = username

    # def change_password(self, password):
    #     if password is None:
    #         raise ValueError
    #     self.__password = password

    # def get_ip(self):
    #     return self.ip

    # def get_username(self):
    #     return self.__username

    # def get_password(self):
    #     return self.__password


class MigrationTarget():
    '''Implements Migration target.'''

    __CLOUD_TYPES: set[str] = {'aws', 'azure', 'vsphere', 'vcloud'}

    def __init__(
            self,
            cloud_type: str,
            cloud_credentials: Credentials,
            target_vm: Workload,
    ):
        if cloud_type not in self.__CLOUD_TYPES:
            raise ValueError('Unknown cloud type')
        elif (
            isinstance(cloud_credentials, Credentials)
            and isinstance(target_vm, Workload)
        ):
            self.__cloud_type = cloud_type
            self.cloud_credentials = cloud_credentials
            self.target_vm = target_vm
        else:
            raise TypeError('Wrong attributes types')

    def get_cloud_type(self):
        return self.__cloud_type

    def __repr__(self):
        return (
            f'* cloud type - {self.__cloud_type};\n'
            f'* cloud credentials: {self.cloud_credentials};\n'
            f'* target virtual machine:\n'
            f'{self.target_vm}'
        )


class Migration():
    '''Implements Migration.'''

    VOLUME_C_BAN: bool = False

    __MIGRATION_STATE: tuple[str] = (
        'not started',
        'running',
        'error',
        'success'
    )

    SLEEP_TIME: int = 1

    def __init__(
            self,
            selected_mount_points: list[MountPoint],
            source: Workload,
            migration_target: MigrationTarget,
    ):
        if (
            isinstance(selected_mount_points, list)
            and all(isinstance(item, MountPoint) is True
                    for item in selected_mount_points)
            and isinstance(source, Workload)
            and isinstance(migration_target, MigrationTarget)
        ):
            self.selected_mount_points = selected_mount_points
            self.source = source
            self.migration_target = migration_target
            self.migration_state = self.__MIGRATION_STATE[0]
        else:
            raise TypeError('Wrong attributes types')

    def run(self):
        self.migration_state = self.__MIGRATION_STATE[1]

        ''' Simple implementation of the business logic:
        ban migrations when volume C:\\ is not allowed. '''
        if self.VOLUME_C_BAN is True:
            self.migration_state = self.__MIGRATION_STATE[2]
        else:
            self.migration_target.target_vm.ip = self.source.ip
            self.migration_target.target_vm.credentials =\
                self.source.credentials
            self.migration_target.target_vm.storage = [
                mp for mp in self.source.storage
                if mp in self.selected_mount_points
            ]
            time.sleep(self.SLEEP_TIME)
            self.migration_state = self.__MIGRATION_STATE[3]

    def __repr__(self):
        return (
            f'Migrations\n'
            f'Selected mount points: {self.selected_mount_points};\n'
            f'Source:\n'
            f'{self.source};\n'
            f'Migration target:\n'
            f'{self.migration_target};\n'
            f'Migration state: {self.migration_state}\n'
        )


class PersistenceLayer():
    '''Implements Persistence layer for classes objects.'''
    # https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence

    def __init__(self, object_list: list, dumpfile: str):
        self.object_list = object_list
        self.dumpfile = dumpfile

    def create(self):
        with open(self.dumpfile, 'wb') as file:
            pickle.dump(self.object_list, file)

    def read(self):
        with open(self.dumpfile, 'rb') as input:
            self.object_list = pickle.load(input)
        return self.object_list

    def update_with_object(self, object_to_append):
        new_object_list: list = self.read()
        if object_to_append not in new_object_list:
            new_object_list.append(object_to_append)
        self.create()

    def update_all(self):
        new_object_list: list = self.object_list[:]
        saved_object_list = self.read()
        for object in saved_object_list:
            if object not in new_object_list:
                new_object_list.append(object)
        self.object_list = new_object_list
        self.create()

    def delete_object(self, object_to_delete):
        new_object_list: list = []
        saved_object_list = self.read()
        for object in saved_object_list:
            if str(object) != str(object_to_delete):
                new_object_list.append(object)
        self.object_list = new_object_list
        self.create()

    def delete_all(self):
        os.remove(self.dumpfile)
