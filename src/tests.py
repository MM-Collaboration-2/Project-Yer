import unittest
from construction_tree import ConstructionTree
from utils import smart_split, get_tokens



class UtilsTests(unittest.TestCase):
    
    def test_smart_split_0(self):
        text = 'var1, [["huh"], s]'
        res = smart_split(text)
        self.assertEqual(res, ['var1', ' [["huh"], s]'])
    
    def test_smart_split_1(self):
        text = '[], fn(), 14'
        res = smart_split(text)
        self.assertEqual(res, ['[]', ' fn()', ' 14'])
    
    def test_smart_split_2(self):
        text = 'foo([a, b], 0), "str"'
        res = smart_split(text)
        self.assertEqual(res, ['foo([a, b], 0)', ' "str"'])


    def test_get_tokens_0(self):
        text = 'var1 + [["huh"], s]'
        res = get_tokens(text)
        self.assertEqual(res, ['var1', '+', '[["huh"],s]'])

    def test_get_tokens_1(self):
        text = '[] * fn() - 14'
        res = get_tokens(text)
        self.assertEqual(res, ['[]', '*', 'fn()', '-', '14'])

    def test_get_tokens_2(self):
        text = 'foo([a, b], 0) / "str"'
        res = get_tokens(text)
        self.assertEqual(res, ['foo([a, b], 0)', '/', '"str"'])



if __name__ == '__main__':
    unittest.main()
