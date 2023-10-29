#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """this will test the FileStorage"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/engine/file_storage.py"])
        self.assertEqual(p.total_errors, 5, "fix pep8")

    def test_all(self):
        """tests if all works in File Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_filestorage(self):
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "models/engine/file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except Exception:
            pass
        self.storage.save()
        with open(path, "r") as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except Exception:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    def test_get(self):
        """Test get() method"""
        # Create a new user object and save it to the database
        user = User(name="John Doe")
        user.save()
        # Get the user object from the database using the get() method
        retrieved_user = self.storage.get(User, user.id)
        # Check that the retrieved user object is the same as the original
        self.assertEqual(user.id, retrieved_user.id)
        self.assertEqual(user.name, retrieved_user.name)

    def test_count(self):
        """Test count() method"""
        # Create some new objects and save them to the database
        state1 = State(name="California")
        state1.save()
        state2 = State(name="New York")
        state2.save()
        city1 = City(name="San Francisco", state_id=state1.id)
        city1.save()
        city2 = City(name="New York City", state_id=state2.id)
        city2.save()
        city3 = City(name="Los Angeles", state_id=state1.id)
        city3.save()
        # Check that the count() method returns the correct number of objects
        self.assertEqual(self.storage.count(State), 2)
        self.assertEqual(self.storage.count(City), 3)
        self.assertEqual(self.storage.count(), 5)


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
