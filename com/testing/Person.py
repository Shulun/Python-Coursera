'''
Created on Aug 10, 2016

@author: Paul
'''
class Person(object):
    def __init__(self, firstname="", lastname=""):
        self.firstname = firstname
        self.lastname = lastname
    def __str__(self):
        return self.firstname + " " + self.lastname
    


if __name__ == '__main__':
    p = Person("Paul", "Chen")
    print(p)
        