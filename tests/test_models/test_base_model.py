#!/usr/bin/python3
""" """
import unittest
import datetime
import json
import os
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.name = 'BaseModel'
        self.value = BaseModel

    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertIsNot(new, i)

    def test_kwargs_int(self):
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        i = self.value()
        expected_str = '[{}] ({}) {}'.format(self.name, i.id, i.__dict__)
        self.assertEqual(str(i), expected_str)

    def test_todict(self):
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        n = {'name': 'test'}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        new = self.value()
        self.assertIsInstance(new.id, str)

    def test_created_at(self):
        new = self.value()
        self.assertIsInstance(new.created_at, datetime.datetime)

    def test_updated_at(self):
        new = self.value()
        self.assertIsInstance(new.updated_at, datetime.datetime)
        original_updated_at = new.updated_at
        new.save()
        self.assertNotEqual(original_updated_at, new.updated_at)


if __name__ == '__main__':
    unittest.main()
