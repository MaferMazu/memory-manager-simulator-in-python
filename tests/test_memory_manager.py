import unittest
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from memory_manager import *

class TestMemoryManager(unittest.TestCase):
    def test_creation(self):
        memory_manager=MemoryManager(10)
        self.assertEqual(memory_manager.free_blocks,[[],[8],[],[0]])

    def test_fit_insert(self):
        memory_manager=MemoryManager(10)
        memory_manager.reserve("var",2)
        self.assertEqual(memory_manager.free_blocks,[[],[],[],[0]])
        self.assertEqual(memory_manager.used_blocks,[["var",8,2]])

    def test_try_insert_same_name(self):
        memory_manager=MemoryManager(10)
        memory_manager.reserve("var",2)
        memory_manager.reserve("var",2)
        self.assertEqual(memory_manager.free_blocks,[[],[],[],[0]])
        self.assertEqual(memory_manager.used_blocks,[["var",8,2]])

    def test_odd_insert(self):
        memory_manager=MemoryManager(10)
        memory_manager.reserve("var",3)
        self.assertEqual(memory_manager.free_blocks,[[9],[7],[3],[]])
        self.assertEqual(memory_manager.used_blocks,[["var",0,3]])

    def test_out_of_memory(self):
        memory_manager=MemoryManager(10)
        memory_manager.reserve("var",11)
        self.assertEqual(memory_manager.free_blocks,[[],[8],[],[0]])
        self.assertEqual(memory_manager.used_blocks,[])

    def test_two_odds_insertions(self):
        memory_manager=MemoryManager(10)
        memory_manager.reserve("var",3)
        memory_manager.reserve("var2",5)
        self.assertEqual(memory_manager.free_blocks,[[],[8],[],[]])
        self.assertEqual(memory_manager.used_blocks,[["var",0,3],["var2",3,5]])

    def test_two_insertion_one_deletion(self):
        memory_manager=MemoryManager(10)
        memory_manager.reserve("var",3)
        memory_manager.reserve("var2",5)
        memory_manager.remove("var")
        self.assertEqual(memory_manager.free_blocks,[[2],[0,8],[],[]])
        self.assertEqual(memory_manager.used_blocks,[["var2",3,5]])

    def test_playing_with_interesting_things(self):
        memory_manager=MemoryManager(15)
        memory_manager.reserve("var",3)
        memory_manager.reserve("var1",7)
        memory_manager.remove("var")
        memory_manager.remove("var1")
        memory_manager.reserve("var2",11)
        memory_manager.reserve("var2",2)
        self.assertEqual(memory_manager.free_blocks,[[6],[],[0],[7]])
        self.assertEqual(memory_manager.used_blocks,[["var2",4,2]])

class TestMemoryManagerFunctions(unittest.TestCase):
    def test_is_free_false(self):
        memory_manager=MemoryManager(15)
        memory_manager.reserve("var",7)
        memory_manager.reserve("var1",3)
        result=memory_manager.is_free(3)
        self.assertEqual(result,(-1,-1))
    
    def test_is_free(self):
        memory_manager=MemoryManager(15)
        memory_manager.reserve("var",7)
        memory_manager.reserve("var1",3)
        result=memory_manager.is_free(7)
        self.assertEqual(result,(0,0))

    def test_distribution(self):
        memory_manager=MemoryManager(15)
        memory_manager.reserve("var",7)
        memory_manager.distribution(0,7)
        self.assertEqual(memory_manager.free_blocks,[[14],[12],[8],[0]])


class TestBinarySearch(unittest.TestCase):
    def test_binary_search(self):
        arr=[0,1,2,3,4]
        result=binary_search(arr,0,len(arr)-1,4)
        self.assertEqual(result,4)

    def test_binary_search(self):
        arr=[0,1,2,3,4]
        result=binary_search(arr,0,len(arr)-1,8)
        self.assertEqual(result,-1)



if __name__ == "__main__":
    unittest.main()