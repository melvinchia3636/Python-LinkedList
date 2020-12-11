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

class LinkedList:
    def __init__(self, lst: Optional[list] = None):
        self.head = None
        if lst:
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
        node = self.head
        if index < 0: index = len(self) + index
        for i in range(index):
            node = node.next
            if i < index-1 and not node.next:
                raise IndexError('LinkedList index out of range')
        return node

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

    def print_list(self) -> list:
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
        while index > 1 and node.next:
            node = node.next
            index -= 1
        new_node.next = node.next
        node.next = new_node

    def remove(self, data):
        node = self.head
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

    def sort(self, reverse=False, key=None):
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

if __name__ == '__main__':
    lst = LinkedList([random.randint(0, 10) for i in range(20)])
    print(lst) #return representation of linkedlist
    print(lst.print_list()) #return normal list
    print([i.data for i in lst]) #list comprehension
    print(len(lst)) #return length of the linkedlist
    print(lst[5]) #get item of the linked list
    print(reversed(lst)) #reverse the linked list (lst.reverse() also works but it will change the whole list)
    lst.sort() #sort the linkedlist
    print(lst)
    lst.extend(list(range(10))) #extend the linkedlist
    print(lst)
    lst.append('5555') #append the linkedlist
    print(lst)
    del lst[-1] #delete an element with correspond index in the linkedlist
    print(lst)
    lst.remove(6)#delete an element with correspons data in the linkedlist
    print(lst) 
    lst[-2] = [8, 8, 8, 8] #modify an element in the linkedlist
    print(lst)
    lst.insert(1, 'this is the new second element') #insert a new element into specific index
    print(lst)
    print(lst.pop(-2)) #pop from linkedlist
    print(lst)
    print(lst.count(10)) #return the count of an element
    print(lst.index(10)) #return the index of an element in the list
    lst.clear() #clear the whole linkedlist
    print(lst)