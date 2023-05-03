import requests
import unittest
import test_server_blanks as blanks


class TestAPI(unittest.TestCase):

    def test_01_add_workload(self):
        response = requests.get(blanks.WORKLOADS_ENDPOINT)
        self.assertEqual(response.status_code, 204)

        response = requests.post(
            blanks.WORKLOADS_ENDPOINT,
            json=blanks.WORKLOAD_1
        )
        self.assertEqual(response.status_code, 201)

        response = requests.post(
            blanks.WORKLOADS_ENDPOINT,
            json=blanks.WORKLOAD_2
        )
        self.assertEqual(response.status_code, 201)

        response = requests.post(
            blanks.WORKLOADS_ENDPOINT,
            json=blanks.WORKLOAD_3
        )
        self.assertEqual(response.status_code, 201)

        response = requests.post(
            blanks.WORKLOADS_ENDPOINT,
            json=blanks.WORKLOAD_4
        )
        self.assertEqual(response.status_code, 400)

    def test_02_get_workload(self):
        response = requests.get(blanks.WORKLOADS_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[1], 3)

    def test_03_modify_workload(self):
        response = requests.put(
            blanks.WORKLOAD_3_ENDPOINT,
            json=blanks.WORKLOAD_3_MODIFIED
        )
        self.assertEqual(response.status_code, 200)

        response = requests.put(
            blanks.WORKLOAD_4_ENDPOINT,
            json=blanks.WORKLOAD_3_MODIFIED
        )
        self.assertEqual(response.status_code, 404)

        response = requests.put(
            blanks.WORKLOAD_2_ENDPOINT,
            json=blanks.WORKLOAD_2_NOT_MODIFIED
        )
        self.assertEqual(response.status_code, 304)

    def test_04_delete_workload(self):
        response = requests.delete(blanks.WORKLOAD_3_ENDPOINT)
        self.assertEqual(response.status_code, 200)

        response = requests.delete(blanks.WORKLOAD_4_ENDPOINT)
        self.assertEqual(response.status_code, 404)

    def test_05_add_migration(self):
        response = requests.get(blanks.MIGRATIONS_ENDPOINT)
        self.assertEqual(response.status_code, 204)

        response = requests.post(
            blanks.MIGRATIONS_ENDPOINT,
            json=blanks.MIGRATION_1
        )
        self.assertEqual(response.status_code, 201)

        response = requests.post(
            blanks.MIGRATIONS_ENDPOINT,
            json=blanks.MIGRATION_2
        )
        self.assertEqual(response.status_code, 201)

        response = requests.post(
            blanks.MIGRATIONS_ENDPOINT,
            json=blanks.MIGRATION_3
        )
        self.assertEqual(response.status_code, 201)

        response = requests.post(
            blanks.MIGRATIONS_ENDPOINT,
            json=blanks.MIGRATION_4
        )
        self.assertEqual(response.status_code, 400)

        response = requests.post(
            blanks.MIGRATIONS_ENDPOINT,
            json=blanks.MIGRATION_5
        )
        self.assertEqual(response.status_code, 400)

    def test_06_get_migration(self):
        response = requests.get(blanks.MIGRATIONS_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[1], 3)

    def test_07_modify_migration(self):
        response = requests.put(
            blanks.MIGRATION_3_ENDPOINT,
            json=blanks.MIGRATION_3_MODIFIED
        )
        self.assertEqual(response.status_code, 200)

        response = requests.put(
            blanks.MIGRATION_4_ENDPOINT,
            json=blanks.MIGRATION_3_MODIFIED
        )
        self.assertEqual(response.status_code, 404)

        response = requests.put(
            blanks.MIGRATION_3_ENDPOINT,
            json=blanks.MIGRATION_5
        )
        self.assertEqual(response.status_code, 400)

    def test_08_run_migration(self):
        response = requests.get(blanks.RUN_MIGRATION_1_ENDPOINT)
        self.assertEqual(response.status_code, 200)

        response = requests.get(blanks.RUN_MIGRATION_4_ENDPOINT)
        self.assertEqual(response.status_code, 404)

    def test_09_check_migration_status(self):
        response = requests.get(blanks.MIGRATION_1_STATUS_ENDPOINT)
        self.assertEqual(response.status_code, 200)

        response = requests.get(blanks.MIGRATION_4_STATUS_ENDPOINT)
        self.assertEqual(response.status_code, 404)

    def test_10_delete_migration(self):
        response = requests.delete(blanks.MIGRATION_3_ENDPOINT)
        self.assertEqual(response.status_code, 200)

        response = requests.delete(blanks.MIGRATION_4_ENDPOINT)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
