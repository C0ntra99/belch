from os import listdir, sep
from os.path import abspath, basename, isdir
import xml.etree.ElementTree
import os

def tree(dir, padding):
    print padding[:-1] + '+-' + basename(abspath(dir)) + '/'
    padding = padding + ' '
    files = []

    files = [x for x in listdir(dir) if isdir(dir + sep + x)]
    count = 0
    for file in files:
        count += 1
        print padding + '|'
        path = dir + sep + file
        if isdir(path):
            if count == len(files):
                tree(path, padding + ' ')
            else:
                tree(path, padding + '|')
        else:
            print padding + '+-' + file



def xmlSearch(options):

    return_list = []
    ##Walk through the folders and parse the xml
    for root, dir, files in os.walk('{}/'.format(options.domain)):
        for file_ in files:
            e = xml.etree.ElementTree.parse(os.path.join(root, file_)).getroot()

            newDict = {}
            for type in e:
                newDict[type.tag] = type.text

            ##If a value matches a query then add to return_list
            try:
                ##Parse through the options if the dict needs to be returned
                if options.user:
                    if newDict['sAMAccountName'] == options.user:
                        return_list.append(newDict)
                elif options.group:
                    if options.group in newDict['memberOf']:
                        return_list.append(newDict)
                elif options.query:
                    ##gonna need to think through This
                    pass
                elif options.keyword:
                    if options.keyword in newDict.values() or options.keyword in newDict.keys():
                        return_list.append(newDict)
            except:
                pass
    return return_list
