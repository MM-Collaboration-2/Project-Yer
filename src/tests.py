import unittest

from construction_tree import ConstructionTree

from utils import smart_split_comma, get_tokens, syntax_analysis

from storage import Storage

from yer_builtins import BUILTINS

from operation import Operation

from integer import Integer
from string import String
from list import List
from float import Float



class UtilsTests(unittest.TestCase):
    
    def test_smart_split_0(self):
        text = 'var1, [["huh"], s]'
        res = smart_split_comma(text)
        self.assertEqual(res, ['var1', ' [["huh"], s]'])
    
    def test_smart_split_1(self):
        text = '[], fn(), 14'
        res = smart_split_comma(text)
        self.assertEqual(res, ['[]', ' fn()', ' 14'])
    
    def test_smart_split_2(self):
        text = 'foo([a, b], 0), "str"'
        res = smart_split_comma(text)
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
        self.assertEqual(res, ['foo([a,b],0)', '/', '"str"'])



class OperationTests(unittest.TestCase):

    def test_add_ints(self):
        lop = Integer(1)
        rop = Integer(2)
        op = '+'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 3)

    def test_sub_ints(self):
        lop = Integer(1)
        rop = Integer(2)
        op = '-'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, -1)

    def test_mul_ints(self):
        lop = Integer(1)
        rop = Integer(2)
        op = '*'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 2)

    def test_div_ints(self):
        lop = Integer(1)
        rop = Integer(2)
        op = '/'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 0)

    def test_add_floats(self):
        lop = Float(1.2)
        rop = Float(0)
        op = '+'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        #self.assertEqual(res, )

    def test_sub_floats(self):
        lop = Float(1.2)
        rop = Float(0)
        op = '-'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        #self.assertEqual(res, )

    def test_mul_floats(self):
        lop = Float(1.2)
        rop = Float(2.0)
        op = '*'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 2.4)

    def test_div_floats(self):
        lop = Float(2.25)
        rop = Float(1.5)
        op = '/'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 1.5)

    def test_div_zero(self):
        lop = Float(5)
        rop = Float(0)
        op = '/'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 0)

    def test_add_strings(self):
        lop = String("abo")
        rop = String("ba")
        op = '+'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 'aboba')

    def test_sub_strings(self):
        lop = String("abo")
        rop = String("ba")
        op = '-'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        self.assertEqual(res.data, 0)

    def test_sum_lists(self):
        lop = List([Integer(0), String("cc")])
        rop = List([List([])])
        op = '+'
        storage = Storage({})
        res = Operation.operate(lop, rop, op, storage)
        res = [obj.data for obj in res.data]
        self.assertEqual(res, [0, 'cc', []])


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

    def test_tree_3(self):
        text = '''
        l = [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]];
        i = 0;
        While(len(get(l, i)) != 4) {
            i = i + 1;
        }
        return i;
        '''
        storage = Storage(BUILTINS)
        tree = ConstructionTree(text, storage)
        res = tree.run()
        self.assertEqual(res.obj.data, 4)





if __name__ == '__main__':
    unittest.main()
