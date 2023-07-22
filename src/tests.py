import unittest
from construction_tree import ConstructionTree
from utils import smart_split, get_tokens, syntax_analysis
from storage import Storage
from yer_builtins import BUILTINS



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



class TreeTests(unittest.TestCase):

    def test_tree_0(self):
        text = '''
        Func(countdown){
            tmp = $argv0 + [$argv1]	
            If($argv1 > 1){
                countdown(tmp, $argv1-1);
            }
            return tmp;
        }

        return countdown([], 3);
        '''
        storage = Storage(BUILTINS)
        tree = ConstructionTree(text, storage)
        res = tree.run()
        res = [obj.data for obj in res.obj.data]
        self.assertEqual(res, [3, 2, 1])

    def test_tree_1(self):
        text = '''
        Func(fib){
            a = 0;
            b = 1;
            c = 0;
            For(i=0;i<$argv0;i=i+1){
                c = a + b;
                a = b;
                b = c;
            }
            return c;
        }
        return fib(5);
        '''
        storage = Storage(BUILTINS)
        tree = ConstructionTree(text, storage)
        res = tree.run()
        self.assertEqual(res.obj.data, 8)

    def test_tree_2(self):
        text = '''
        return get(["a", "b", "c"], len([1]));
        '''
        storage = Storage(BUILTINS)
        tree = ConstructionTree(text, storage)
        res = tree.run()
        self.assertEqual(res.data, 'b')





if __name__ == '__main__':
    unittest.main()
