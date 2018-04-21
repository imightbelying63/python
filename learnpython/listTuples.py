""" listTuples.py
    take a list containing 3-element tuples and create a new list of only the
    first two elemese of each tuple in the list
"""

list1 = [(1,2,3), (4,5,6), (7,8,9)]
list2 = [x[:2] for x in list1]

if __name__ == "__main__":
    print(list1, '\n', list2)
