import json
import os
import unittest
from io import StringIO
from unittest.mock import patch

from file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        FileStorage.__objects = {}
        self.file_storage = FileStorage()

    def test_all(self):
        self.assertEqual(self.file_storage.all(), {})

        obj1 = {"id": 1, "name": "object 1"}
        self.file_storage.new(obj1)
        self.assertEqual(self.file_storage.all(), {"object.1": obj1})

        obj2 = {"id": 2, "name": "object 2"}
        self.file_storage.new(obj2)
        self.assertEqual(self.file_storage.all(), {"object.1": obj1, "object.2": obj2})

    def test_new(self):
        obj = {"id": 1, "name": "object 1"}
        self.file_storage.new(obj)
        self.assertEqual(self.file_storage.all(), {"object.1": obj})

    @patch('sys.stdout', new_callable=StringIO)
    def test_save(self, mock_stdout):
        obj = {"id": 1, "name": "object 1"}
        self.file_storage.new(obj)

        self.file_storage.save()
        with open("file.json", 'r') as file:
            self.assertEqual(json.load(file), {"object.1": obj})

    @patch('sys.stdout', new_callable=StringIO)
    def test_reload(self, mock_stdout):
        obj = {"id": 1, "name": "object 1"}
        self.file_storage.new(obj)

        self.file_storage.save()

        self.file_storage = FileStorage()
        self.assertEqual(self.file_storage.all(), {})
        self.file_storage.reload()
        self.assertEqual(self.file_storage.all(), {"object.1": obj})

        os.remove("file.json")

if __name__ == '__main__':
    unittest.main()
