import unittest
from .models import Blog

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_blog = Blog(category = 'Blog')

if __name__ =='__main__':
    unittest.main()