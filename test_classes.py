import unittest
import classes
# import time
# import os


class TestCredentials(unittest.TestCase):
    '''Tests Credentials class.'''

    def test_attributes_types(self):
        self.assertRaises(
            TypeError, classes.Credentials, 1111, 'test_pass', 'test_domain')
        self.assertRaises(
            TypeError, classes.Credentials, 'test_username', 11, 'test_domain')
        self.assertRaises(
            TypeError, classes.Credentials, 'test_username', 'test_pass', 1111)

    def test_correct_credentials(self):
        credentials = classes.Credentials('test_user', 'test_pass', 'test_dom')
        self.assertEqual(credentials.username, 'test_user')
        self.assertEqual(credentials.password, 'test_pass')
        self.assertEqual(credentials.domain, 'test_dom')


class TestMountPoint(unittest.TestCase):
    '''Tests MountPoint class.'''

    def test_attributes_types(self):
        self.assertRaises(TypeError, classes.MountPoint, 1, 111)
        self.assertRaises(TypeError, classes.MountPoint, 'C:\\', '111')

    def test_correct_mount_point(self):
        mount_point = classes.MountPoint('C:\\', 111)
        self.assertEqual(mount_point.mount_point_name, 'C:\\')
        self.assertEqual(mount_point.total_size, 111)


class TestWorkload(unittest.TestCase):
    '''Tests Workload class.'''

    TEST_IP: str = '192.168.0.1'

    @classmethod
    def setUpClass(cls):
        cls.credentials = classes.Credentials('user', 'password', 'domain')
        cls.mount_point_1 = classes.MountPoint('C:\\', 100)
        cls.mount_point_2 = classes.MountPoint('D:\\', 200)
        cls.storage = [cls.mount_point_1, cls.mount_point_2]
        cls.workload = classes.Workload(
            cls.TEST_IP, cls.credentials, cls.storage
        )

    def test_attributes_not_none(self):
        self.assertRaises(
            ValueError,
            classes.Workload,
            None,
            self.credentials,
            self.storage
        )
        self.assertRaises(
            ValueError,
            classes.Workload,
            self.TEST_IP,
            None,
            self.storage
        )
        self.assertRaises(
            ValueError,
            classes.Workload,
            self.TEST_IP,
            self.credentials,
            None
        )

    def test_attributes_types(self):
        self.assertRaises(
            TypeError,
            classes.Workload,
            1111,
            self.credentials,
            self.storage
        )
        self.assertRaises(
            TypeError,
            classes.Workload,
            self.TEST_IP,
            'user password domain',
            self.storage
        )
        self.assertRaises(
            TypeError,
            classes.Workload,
            self.TEST_IP,
            self.credentials,
            self.mount_point_1
        )
        self.assertRaises(
            TypeError,
            classes.Workload,
            self.TEST_IP,
            self.credentials,
            [1, 2, 3]
        )

    def test_correct_workload(self):
        self.assertEqual(self.workload.ip, self.TEST_IP)
        self.assertEqual(self.workload.credentials, self.credentials)
        self.assertEqual(self.workload.storage, self.storage)


class TestSource(unittest.TestCase):
    '''Tests Source class.'''

    TEST_USERNAME: str = 'test_username'
    TEST_PASSWORD: str = 'test_password'
    TEST_IP: str = '192.168.0.1'

    def test_attributes_not_none(self):
        self.assertRaises(
            ValueError,
            classes.Source,
            None,
            self.TEST_PASSWORD,
            self.TEST_IP
        )
        self.assertRaises(
            ValueError,
            classes.Source,
            self.TEST_USERNAME,
            None,
            self.TEST_IP
        )
        self.assertRaises(
            ValueError,
            classes.Source,
            self.TEST_USERNAME,
            self.TEST_PASSWORD,
            None
        )

    def test_attributes_types(self):
        self.assertRaises(
            TypeError, classes.Source, 1111, self.TEST_PASSWORD, self.TEST_IP)
        self.assertRaises(
            TypeError, classes.Source, self.TEST_USERNAME, 1111, self.TEST_IP)
        self.assertRaises(
            TypeError, classes.Source,
            self.TEST_USERNAME, self.TEST_PASSWORD, 1111
        )

    def test_correct_credentials(self):
        source = classes.Source(
            self.TEST_USERNAME, self.TEST_PASSWORD, self.TEST_IP
        )
        self.assertEqual(source.username, self.TEST_USERNAME)
        self.assertEqual(source.password, self.TEST_PASSWORD)
        self.assertEqual(source.ip, self.TEST_IP)


class TestMigrationTarget(unittest.TestCase):
    '''Tests MigrationTarget class.'''

    TEST_IP: str = '192.168.0.1'
    CLOUD_TYPE: str = 'aws'

    @classmethod
    def setUpClass(cls):
        cls.cloud_credentials = classes.Credentials(
            'user', 'password', 'domain'
        )
        cls.mount_point_1 = classes.MountPoint('C:\\', 100)
        cls.mount_point_2 = classes.MountPoint('D:\\', 200)
        cls.storage = [cls.mount_point_1, cls.mount_point_2]
        cls.target_vm = classes.Workload(
            cls.TEST_IP, cls.cloud_credentials, cls.storage
        )

    def test_cloud_type_not_in_set(self):
        self.assertRaises(ValueError,
                          classes.MigrationTarget,
                          'test_cloud',
                          self.cloud_credentials,
                          self.target_vm)

    def test_attributes_types(self):
        self.assertRaises(
            TypeError,
            classes.MigrationTarget,
            self.CLOUD_TYPE,
            'user password domain',
            self.target_vm
        )
        self.assertRaises(
            TypeError,
            classes.MigrationTarget,
            self.CLOUD_TYPE,
            self.cloud_credentials,
            self.storage
        )

    def test_correct_migration_target(self):
        migration_target = classes.MigrationTarget(
            self.CLOUD_TYPE, self.cloud_credentials, self.target_vm
        )
        self.assertEqual(migration_target.get_cloud_type(), self.CLOUD_TYPE)
        self.assertEqual(
            migration_target.cloud_credentials, self.cloud_credentials
        )
        self.assertEqual(migration_target.target_vm, self.target_vm)


class TestMigration(unittest.TestCase):
    '''Tests Migration class.'''

    TEST_IP_1: str = '192.168.0.1'
    TEST_IP_2: str = '192.168.0.2'
    CLOUD_TYPE: str = 'aws'

    @classmethod
    def setUpClass(cls):
        cls.credentials = classes.Credentials(
            'user', 'password', 'domain'
        )
        cls.cloud_credentials = cls.credentials
        cls.mount_point_1 = classes.MountPoint('C:\\', 100)
        cls.mount_point_2 = classes.MountPoint('D:\\', 200)
        cls.storage = [cls.mount_point_1, cls.mount_point_2]
        cls.target_vm = classes.Workload(
            cls.TEST_IP_1, cls.cloud_credentials, cls.storage
        )
        cls.migration_target = classes.MigrationTarget(
            cls.CLOUD_TYPE, cls.cloud_credentials, cls.target_vm
        )
        cls.selected_mount_points = [cls.mount_point_1]
        cls.source_storage = cls.storage
        cls.source_credentials = cls.credentials
        cls.source = classes.Workload(
            cls.TEST_IP_2, cls.source_credentials, cls.source_storage
        )
        cls.test_migration = classes.Migration(
            cls.selected_mount_points, cls.source, cls.migration_target
        )

    def test_attributes_types(self):
        self.assertRaises(
            TypeError,
            classes.Migration,
            1111,
            self.source,
            self.migration_target
        )
        self.assertRaises(
            TypeError,
            classes.Migration,
            [1, 2, 3],
            self.source,
            self.migration_target
        )
        self.assertRaises(
            TypeError,
            classes.Migration,
            self.selected_mount_points,
            self.source_credentials,
            self.migration_target
        )
        self.assertRaises(
            TypeError,
            classes.Migration,
            self.selected_mount_points,
            self.source,
            self.target_vm
        )

    def test_correct_migration(self):
        self.assertEqual(self.test_migration.selected_mount_points,
                         self.selected_mount_points)
        self.assertEqual(self.test_migration.source, self.source)
        self.assertEqual(self.test_migration.migration_target,
                         self.migration_target)
        self.test_migration.run()
        self.assertEqual(self.migration_target.target_vm.storage,
                         self.selected_mount_points)

    def test_migration_volume_c_is_not_allowed(self):
        self.test_migration.VOLUME_C_BAN = True
        self.test_migration.run()
        self.assertEqual(self.test_migration.migration_state, 'error')


class TestPersistanceLayer(unittest.TestCase):
    '''Tess PersistenceLayer class.'''

    @classmethod
    def setUpClass(cls):
        pass

    def test_create_file(self):
        pass

    def test_read_file(self):
        pass

    def test_update_file(self):
        pass

    def test_delete_file(self):
        pass

    def test_create_same_ip_sources(self):
        pass


if __name__ == '__main__':
    unittest.main()
