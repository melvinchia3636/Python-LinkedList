from typing import Optional
import sys
import random
from copy import deepcopy

sys.setrecursionlimit(2147483647)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return '<{} with data {}>'.format(self.__class__.__name__, self.data, self.next)

class LinkedList(object):
    def __init__(self, lst = None):
        self.head = None
        if lst:
            lst = list(lst)
            self.head = node = Node(lst.pop(0))
            for i in lst:
                node.next = Node(i)
                node = node.next

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, ' --> '.join(list(map(str, self.print_list()))) if self.print_list() else 'Empty')

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next

    def __len__(self) -> int:
        count = 0
        node = self.head
        while node:
            count += 1
            node = node.next
        return count

    def __getitem__(self, index):
        if isinstance(index, int):
            node = self.head
            if index < 0: index = len(self) + index
            for i in range(index):
                node = node.next
                if i < index-1 and not node.next:
                    raise IndexError('LinkedList index out of range')
            return node
        elif isinstance(index, slice):
            new = LinkedList()
            if not index.step:
                node = deepcopy(self.head)
                if not index.start: start = 0
                elif index.start < 0: start = 0-index.start
                else: start = index.start
                for _ in range(start):
                    if node.next: node = node.next
                    else: raise IndexError('LinkedList index out of range')
                new.head = node

                if not index.stop: stop = len(self)
                elif index.stop < 0: stop = len(self) + index.stop
                else: stop = index.stop
                length = stop - start
                if stop - start < 0: raise IndexError('Start should be smaller than stop')
                curr = new.head
                for _ in range(length-1):
                    if curr.next: curr = curr.next
                    else: break
                curr.next = None
                return new

    def __setitem__(self, index, data):
        node = self.head
        if index < 0: index = len(self) + index
        for i in range(index):
            node = node.next
            if i < index-1 and not node.next:
                raise IndexError('LinkedList index out of range')
        node.data = data

    def __delitem__(self, index):
        node = self.head
        if index < 0: index = len(self) + index
        if not index:
            self.head = self.head.next if self.head else None
            return
        for i in range(index-1):
            node = node.next
            if i < index-1 and not node.next:
                raise IndexError('LinkedList index out of range')
        node.next = node.next.next if node.next else None

    def __reversed__(self):
        copy = self.copy()
        copy.reverse()
        return copy

    def extend(self, lst):
        for node in self:
            pass
        for i in lst:
            node.next = Node(i)
            node = node.next

    def print_list(self):
        nodes = []
        node = self.head
        while node:
            nodes.append(node.data)
            node = node.next
        return nodes
    
    def append(self, data):
        node = Node(data)
        for i in self:
            pass
        i.next = node

    def insert(self, index, data):
        new_node = Node(data)
        node = self.head
        if index < 0: index = len(self) + index
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            while index > 1 and node.next:
                node = node.next
                index -= 1
            new_node.next = node.next
            node.next = new_node

    def remove(self, data):
        node = self.head
        if node.data == data:
            self.head = node.next
            return
        while node and node.next:
            if node.next.data == data:
                node.next = node.next.next if node.next else None
                return
            node = node.next
        raise ValueError('LinkedList.remove(data): data not in LinkedList')

    def pop(self, index=-1):
        if index < 0: index = len(self) + index
        node = self[index] if index < len(self) else None
        if not node: raise IndexError('Pop index out of range')
        del self[index]
        return node

    def clear(self):
        self.head = None

    def index(self, data, start=None, end=None) -> int:
        node = self.head
        index = 0
        if start:
            if start > len(lst)-1 : raise IndexError('{} is not in LinkedList'.format(data))
            for node in self:
                if index == start: break
                index += 1
        while node:
            if node.data == data:
                return index
            node = node.next
            index += 1
            if index == end: break
        raise IndexError('{} is not in LinkedList'.format(data))

    def count(self, data) -> int:
        count = 0
        node = self.head
        while node:
            if node.data == data:
                count += 1
            node = node.next
        return count

    def lazySort(self, reverse=False, key=None):
        sorted_list = [Node(i) for i in sorted(self.print_list(), reverse=reverse, key=key)]
        self.clear()
        self.head = sorted_list.pop(0)
        node = self.head
        for i in sorted_list:
            node.next = i
            node = node.next

    def reverse(self):
        node = self.head
        prev = None
        while node:
            next = node.next
            node.next = prev
            prev = node
            node = next
        self.head = prev

    def copy(self):
        return deepcopy(self)
    
    def min(self):
        curr = self.head
        res = curr.data
        index = 0
        res_index = 0
        while curr:
            if curr.data < res:
                res = curr.data
                res_index = index
            index += 1
            curr = curr.next
        return res_index, res
        
    def max(self):
        curr = self.head
        res = curr.data
        index = 0
        res_index = 0
        while curr:
            if curr.data > res:
                res = curr.data
                res_index = index
            index += 1
            curr = curr.next
        return res_index, res

    def swap(self, index):
        if index >= len(self): return
        curr = 0 
        prev = self.head
        if index:
            while prev and curr != index-1:
                curr += 1
                prev = prev.next
        if not prev.next and prev.next.next: return
        curr = prev.next
        _next = curr.next
        prev.next = _next
        if index:
            curr.next = _next.next
            _next.next = curr
        else:
            curr.next = prev
            self.head = curr

    def bubbleSort(self, logging=False, logging_type='normal'):
        log_text = '{} Current Index: {}, Value: {}, Next Index: {}, {}'
        run = True
        length = len(self)-1
        curr = length
        swap_amount = 0
        while curr > 0 and run:
            run = False
            for i in range(curr):
                is_swapped = False
                if self[i].data > self[i+1].data:
                    self.swap(i)
                    run = True
                    is_swapped = True
                    swap_amount += 1
                if logging: print(log_text.format(self.print_list() if logging_type=='list' else self, i, self[i].data, i+1, ("Performed swap on index: {} and {}".format(i, i+1)) if is_swapped else 'No swap is performed'))   
            curr -= 1   
        if logging: print(f'Number of swaps: {swap_amount}')

    def _getInsertLocation(self, i):
        for k in range(i):
            if self[k].data > self[i].data: return k

    def insertionSort(self, logging=False, logging_type='normal'):
        logging_text = '{} Current Index: {}, Value: {}, Need Change: {}, Insert To: {}'
        insert_amount = 0
        for i in range(1, len(self)):
            k = self._getInsertLocation(i)
            if k != None: insert_amount += 1
            if logging: print(logging_text.format(self.print_list() if logging_type=='list' else self, i, self[i].data, k != None, k))
            if k != None: self.insert(k, self.pop(i).data)
        if logging: print(f'Number of insertions: {insert_amount}')
    
    def selectionSort(self, logging=False, logging_type='normal'):
        log_text = '{} Selected min value from index {} to index {}: {} at index {}, {}'
        changes_amount = 0
        for i in range(len(self)):
            index, min_val = self[i:].min()
            if index+i != i: 
                self.insert(i, self.pop(i+index).data)
                log_text_2 = 'Inserted min value to index {}'.format(i)
                changes_amount += 1
            else: log_text_2 = 'No changes happened'
            if logging: print(log_text.format(self.print_list() if logging_type=='list' else self, i, len(self), min_val, index+i, log_text_2))
        if logging: print(f'Number of actions: {changes_amount}')


if __name__ == '__main__':

    #bubble sort algorithm on linked list by The Silly Coder :D
    print('Bubble Sort')
    lst = LinkedList([7,3,1,5,4])
    print(lst)
    lst.bubbleSort(logging=True, logging_type='list')
    print(lst)
    print()

    #insertion sort algorithm on linked list by The Silly Coder :D
    print('Insertion Sort')
    lst = LinkedList([7,3,1,5,4])
    print(lst)
    lst.insertionSort(logging=True, logging_type='list')
    print(lst)
    print()

    #selection sort on linked list by The Silly Coder :D
    print('Selection Sort')
    lst = LinkedList([7,3,1,5,4])
    print(lst)
    lst.selectionSort(logging=True, logging_type='list')
    print(lst)
    print()
    
    #basic functionality
    lst = LinkedList(range(10))
    sorted(lst, key=lambda x: x.data) #sort linked list using python builtin sort function
    lst.print_list() #return normal list
    [i.data for i in lst] #list comprehension
    len(lst) #return length of the linkedlist
    lst[5] #get item of the linked list
    lst[5:], lst[:5], lst[:], lst[-5:], lst[:-5] #slice the linked list (stepping is currently not supported)
    lst.min() #get the minimum value of the linked list and its index
    lst.max() #get the maximum value of the linked list and its index
    reversed(lst) #reverse the linked list (lst.reverse() also works but it will change the whole list)
    lst.lazySort() #sort the linkedlist with python built-in function lol I'm just simply lazy to apply sorting algorithm
    lst.extend(range(10)) #extend the linkedlist
    lst.append('5555') #append the linkedlist
    del lst[-1] #delete an element with correspond index in the linkedlist
    lst.remove(6)#delete an element with correspons data in the linkedlist
    lst[-2] = [8, 8, 8, 8] #modify an element in the linkedlist
    lst.insert(1, 'this is the new second element') #insert a new element into specific index
    lst.pop(-2) #pop from linkedlist
    lst.count(10) #return the count of an element
    lst.index(9) #return the index of an element in the list
    lst.clear() #clear the whole linkedlist