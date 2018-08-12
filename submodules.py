from os import listdir, sep
from os.path import abspath, basename, isdir
import xml.etree.cElementTree
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



class XmlSearch:

    @staticmethod
    def xmlParse(domain):
        parsedFiles = []
        print domain
        for root, dir, files in os.walk('{}/'.format(domain)):
            for file_ in files:
                e = xml.etree.ElementTree.parse(os.path.join(root, file_)).getroot()

                newDict = {}
                for type in e:
                    newDict[type.tag] = type.text
                parsedFiles.append(newDict)

        return parsedFiles

    @staticmethod
    def printUsers(domain):
        return_dict = {}
        computerAccounts = []
        userAccounts = []
        for attributes in XmlSearch.xmlParse(domain):
            try:
                attributes['objectClass']
            except:
                continue
            if "user" in attributes['objectClass'].split(' ') and "person" in attributes['objectClass'].split(' '):
                try:
                    attributes['sAMAccountName']
                except:
                    continue

                if attributes['sAMAccountName'][-1] == '$':
                    computerAccounts.append(attributes['sAMAccountName'])
                else:
                    userAccounts.append(attributes['sAMAccountName'])

        return_dict['computerAccounts'] = computerAccounts
        return_dict['userAccounts'] = userAccounts
        return return_dict

    @staticmethod
    def getUser(user, domain):
        for attributes in XmlSearch.xmlParse(domain):
            return_list = []
            if attributes.get('sAMAccountName') == user:
                return_list.append(attributes)
                break
        return return_list

    @staticmethod
    def getGroups(domain):
        return_list = []
        for attributes in XmlSearch.xmlParse(domain):
            try:
                attributes['objectClass']
            except:
                continue

            if "group" in attributes['objectClass'].split(' '):
                return_list.append(attributes['cn'])

        return return_list

    @staticmethod
    def groupMembership(group, domain):
        ##Return a list of dictionaries to hold all the attributes of each user
        return_list = []
        for attributes in XmlSearch.xmlParse(domain):

            if attributes.get("objectClass") and "group" in attributes.get("objectClass"):
                ##Make sure it is that one group
                try:
                    attributes['member']
                except:
                    continue
                if group in attributes['cn']:
                    for objectName in attributes['member'].split(','):
                        if 'CN=' in objectName:
                            return_list.append(objectName.split('CN=')[1])
                    #return_list.append(attributes['member'])

        return return_list

    ##This one is going to take a sec
    @staticmethod
    def getPolicies(domain):
        pass
