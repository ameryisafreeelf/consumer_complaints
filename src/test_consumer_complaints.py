import unittest

import consumer_complaints

class TestParseLine(unittest.TestCase):

    def setUp(self):
        self.my_list = []

    def test_parseLine_simple(self):
        my_string = "Hello,my,name,is,Amery"
        consumer_complaints.parseLine(my_string, self.my_list)
        self.assertEqual( len(self.my_list[0]), 5 )

    def test_parseLine_with_quotes(self):
        my_string = "\"Hello,my,name,is,Amery\""
        consumer_complaints.parseLine(my_string, self.my_list)
        self.assertEqual( len(self.my_list[0]), 1 )

    def test_parseLine_mixed(self):
        my_string = "Hello,my,name,is,Amery,\"Hello,my,name,is,Amery\"" 
        consumer_complaints.parseLine(my_string, self.my_list)
        self.assertEqual( len(self.my_list[0]), 6 )


class TestGetOutputList(unittest.TestCase):

    def setUp(self):
        self.my_dict = { ('a','b') : {'c' : 1, 'd' : 2} }
        self.my_dict2 = { ('a','b') : {'c' : 1, 'd' : 2}, ('x','y') : {'e' : 3, 'f' : 4} }
        self.my_dict3 = { ('a','b') : {'c' : 1, 'd' : 2}, ('a','z') : {'e' : 3, 'f' : 4} }

    def test_simple(self):
        my_list = consumer_complaints.getOutputList(self.my_dict)
        self.assertEqual( ['a,b,3,2,67'], my_list )

    def test_simple2(self):
        # Rounding seems to work properly
        my_list = consumer_complaints.getOutputList(self.my_dict2)
        self.assertEqual( ['a,b,3,2,67', 'x,y,7,2,57'], my_list )

    def test_same_complaint_diff_year(self):
        my_list = consumer_complaints.getOutputList(self.my_dict3)
        self.assertEqual( ['a,b,3,2,67', 'a,z,7,2,57'], my_list )


if __name__ == '__main__':
    unittest.main()
