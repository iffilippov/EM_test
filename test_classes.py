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

    def setUp(self):
        self.credentials = classes.Credentials('user', 'password', 'domain')
        self.mount_point_1 = classes.MountPoint('C:\\', 100)
        self.mount_point_2 = classes.MountPoint('D:\\', 200)
        self.storage = [self.mount_point_1, self.mount_point_2]
        self.workload = classes.Workload(
            self.TEST_IP, self.credentials, self.storage
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
    '''Testing Source class.'''
    pass


class TestMigrationTarget(unittest.TestCase):
    '''Testing MigrationTarget class.'''
    pass


class TestMigration(unittest.TestCase):
    '''Testing Migration class.'''
    pass


class TestPersistanceLayer(unittest.TestCase):
    '''Testing PersistenceLayer class.'''
    pass


if __name__ == '__main__':
    unittest.main()
