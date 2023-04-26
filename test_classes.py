# import pytest
import unittest
import classes
# import time
# import os


class TestWorkload(unittest.TestCase):
    '''Testing Workload class.'''
    pass


class TestCredentials(unittest.TestCase):
    '''Testing Credentials class.'''
    def test_username_not_str(self):
        self.assertRaises(
            ValueError, classes.Credentials, 1111, 'test_pass', 'test_domain')


class TestMountPoint(unittest.TestCase):
    '''Testing MountPoint class.'''
    pass


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
