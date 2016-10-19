"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if list1 == []:
        new_list = []
    else:
        if list1[0] not in list1[1:]:
            new_list = [list1[0]] + remove_duplicates(list1[1:])
        else:
            new_list = remove_duplicates(list1[1:])
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if list1 == []:
        intersect_list = []
    else:
        if list1[0] not in list2:
            intersect_list = intersect(list1[1:], list2)
        else:
            intersect_list = [list1[0]] + intersect(list1[1:], list2)
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    merge_list = []
    index_i = 0
    index_j = 0
    while index_i < len(list1) and index_j < len(list2):
        if list1[index_i] <= list2[index_j]:
            merge_list.append(list1[index_i])
            index_i += 1
        else:
            merge_list.append(list2[index_j])
            index_j += 1
    while index_i < len(list1):
        merge_list.append(list1[index_i])
        index_i += 1
    while index_j < len(list2):
        merge_list.append(list2[index_j])
        index_j += 1    
    return merge_list
    
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    sorted_list = []
    if len(list1) <= 1:
        return list1
    mid = len(list1)/2
    left = merge_sort(list1[:mid])
    right = merge_sort(list1[mid:])
    sorted_list = merge(left, right)
    return sorted_list

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):  
    """ 
    Generate all strings that can be composed from the letters in word 
    in any order. 
 
    Returns a list of all strings that can be formed from the letters 
    in word. 
 
    This function should be recursive. 
    """  
    if len(word) == 0:
        return ['']
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    rest_strings_copy = list(rest_strings)
    for item in rest_strings_copy:
        for index in range(len(item)):
            new_word = item[:index] + first + item[index:]
            rest_strings.append(new_word)
        rest_strings.append(item + first)
    return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    res = []  
    url = codeskulptor.file2url(filename)  
    netfile = urllib2.urlopen(url)  
    for line in netfile.readlines():  
        res.append(line[:-1])  
    return res 

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()
#lst1 = [1, 2, 4, 5, 9]
#lst2 = [2, 3, 4, 7, 7, 8, 10]
#print intersect(lst1, lst2)
#print merge(lst1, lst2)

#lst3 = [1, 4, 2, 5, 9, 2, 1]
#print merge_sort(lst3)

#print gen_all_strings('dota')
    
