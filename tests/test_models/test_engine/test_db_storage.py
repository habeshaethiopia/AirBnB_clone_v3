#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from os import getenv
import MySQLdb
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "NO DB")
class TestDBStorage(unittest.TestCase):
    """this will test the DBStorage"""

    @classmethod
    def setUpClass(self):
        """set up for test"""
        self.User = getenv("HBNB_MYSQL_USER")
        self.Passwd = getenv("HBNB_MYSQL_PWD")
        self.Db = getenv("HBNB_MYSQL_DB")
        self.Host = getenv("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(
            host=self.Host,
            user=self.User,
            passwd=self.Passwd,
            db=self.Db,
            charset="utf8",
        )
        self.query = self.db.cursor()
        self.storage = DBStorage()
        self.storage.reload()

    @classmethod
    def teardown(self):
        """at the end of the test this will tear it down"""
        self.query.close()
        self.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "NO DB")
    def test_pep8_DBStorage(self):
        """Test Pep8"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/engine/db_storage.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "NO DB")
    def test_read_tables(self):
        """existing tables"""
        self.query.execute("SHOW TABLES")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 7)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "NO DB")
    def test_no_element_user(self):
        """no elem in users"""
        self.query.execute("SELECT * FROM users")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "NO DB")
    def test_no_element_cities(self):
        """no elem in cities"""
        self.query.execute("SELECT * FROM cities")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "NO DB")
    def test_add(self):
        """Test same size between storage() and existing db"""
        self.query.execute("SELECT * FROM states")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 0)
        state = State(name="LUISILLO")
        state.save()
        self.db.autocommit(True)
        self.query.execute("SELECT * FROM states")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 1)

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
        # Check that the count() method returns the correct number of objects
        self.assertEqual(self.storage.count(State), 2)
        self.assertEqual(self.storage.count(City), 2)
        self.assertEqual(self.storage.count(), 4)


if __name__ == "__main__":
    unittest.main()
