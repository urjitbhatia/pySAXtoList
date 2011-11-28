'''
Created on November 09, 2011

@author:    urjit singh bhatia
@email:     urjitsb87@gmail.com

'''

import time
import sys
import os
import urllib
import xml.sax
from datetime import timedelta, datetime
from pprint import pprint
from types import ListType, DictionaryType

class Data():
    masterList = []

class GrubHubSaxParser(xml.sax.ContentHandler):

    def __init__(self, data):
        self.root = None
        self.stack = []
        self.currentCharacters = ''
        self.data = data
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if self.root is None:
            self.root = name
        #======================================================================
        # Push each element name as it opens onto the stack
        #======================================================================
        self.stack.append(name)

    def endElement(self, name):

        #=====================================================================
        # element = self.stack.pop() - - -This is the element on top of the stack
        #
        #=====================================================================
        # # if element == name:- - -This means the end was fired for the most recent element, thus it has no children...
        # #    The end event was fired on an element name and its starting tag was on top of the stack,
        # #    that means its a plain element without children...
        #=====================================================================
        #
        #=====================================================================
        # # else if element != name:- - -This means this element has children
        # #   So we will collect the children from the stack by popping each element till its head is found
        # #   when the head is found, create a dictionary for itself with the element name as key and list of children as value
        #=====================================================================
        #=====================================================================

        temp = []
        while True:
            element = self.stack.pop()
            if element != name:
                if len(temp) > 0:
                    t = temp.pop()
                    if isinstance(t, DictionaryType):
                        if t.keys() == element.keys():
                            temp.append([t, element])
                        else:
                            t.update(element)
                            temp.append(t)
                    else:
                        if isinstance(t, ListType):
                            t.append(element)
                        else:
                            temp.append(element)
                        temp.append(t)
                else:
                    temp.append(element)
            else:
                if len(temp) == 0:
                    self.stack.append({name:self.currentCharacters.strip()})
                else:
                    if len(temp) == 1:
                        self.stack.append({name:temp.pop()})
                    else:
                        self.stack.append({name:temp})
                break
        self.currentCharacters = ''
        if name == self.root:
            self.data.masterList = self.stack[0][self.root]

    def characters(self, content):
        self.currentCharacters += content.strip()

def main(sourceFile):
    source = open(sourceFile)
    data = Data()
    t = time.clock()
    print "Start: ", t

    xml.sax.parseString(source, handler=GrubHubSaxParser(data))
    print "Time taken: ", time.clock() - t
    print "The final dict is: ", len(data.masterList)
    pprint(data.masterList)

if __name__ == "__main__":
    print "Parsing..."
    main(sourceFile='your-file-path-here')

