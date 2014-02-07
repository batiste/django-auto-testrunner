from django.test import TestCase
import time

# Create your tests here.
class DummyTestCase(TestCase):
    def setUp(self):
    	pass

    def test_1(self):
        """Dummy test 1"""
        self.assertEqual(1, 1)
        time.sleep(1)

    def test_2(self):
        """Dummy test 2"""
        self.assertEqual(2, 2)
        time.sleep(1)

    def test_3(self):
        """Dummy test 3"""
        self.assertEqual(2, 2)
        time.sleep(1)
