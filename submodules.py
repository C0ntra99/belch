import xml.etree.cElementTree
import argparse
from colorama import Fore

class Args:

    @staticmethod
    def getArgs():
        parser = argparse.ArgumentParser()

        parser.add_argument('target', action='store', help='domain/username[:password]')

        
        auth_group = parser.add_argument_group('Authentication')
        auth_group.add_argument('-ha', '--hash', action='store', help='NTML hash, format is LMHASH:NTHASH')

        control_group = parser.add_argument_group('Control Actions', description='Options when querying the domain')
        control_group.add_argument('-a', '--all', action='store_true', help='Query for all information on the domain')
        control_group.add_argument('-u', '--users', action='store_true', help='Only query for the user information on the domain')
        control_group.add_argument('-uN', '--username', action ='store', help='Only query for one specific user')
        control_group.add_argument('-c', '--computers', action='store_true', help='Only query for the computer information on the domain')
        control_group.add_argument('-cN', '--computerName', action='store', help='Only query for one specific computer')

        user_group = parser.add_argument_group('User Actions', description='Options when searching through a mapped domain')
        user_group.add_argument('-pU', '--print-users', action='store_true', help='Print all the users on the domain')
        user_group.add_argument('-gU', '--get-user', action='store', help='Print out the information of a specified user')

        group_group = parser.add_argument_group('Group Actions', description='Options when searching through a mapped domain')
        group_group.add_argument('-pG', '--print-groups', action='store_true', help='Print all the groups on the domain')
        group_group.add_argument('-gM', '--group-membership', action='store', help='Print all the members of the specified group')

        other_group = parser.add_argument_group('Other options', description='Other options for searching through a mapped domain')
        other_group.add_argument('-k', '--keyword', action='store', help='Search the domain for a specific objected named {keyword}')

        output_group = parser.add_argument_group('Output options', description='Decide how to output the information')
        output_group.add_argument('-x', '--xml', action='store_true', help='Store the output into a xml file')
        output_group.add_argument('-e', '--xls', action='store_true', help='Store the output into a xls file (THIS DOES NOT WORK)')

        return parser.parse_args()

class XmlSearch:

    @staticmethod
    def loadMap():
        with open('domainMap', 'r') as domainMap:
            return domainMap.readlines()

    @staticmethod
    def getPath(object_):
        indexes = XmlSearch.loadMap()
        return_list = []
        for index in indexes:
            if object_ in index:
                filepath = index.strip()
                if filepath not in return_list:
                    return_list.append(filepath)

        if len(return_list) > 1:
            return return_list
        elif len(return_list) == 1:
            return str(return_list[0])
        else:
            return return_list

    @staticmethod
    def multiParse(domain):
        parsedFiles = []

        map_ = XmlSearch.loadMap()
        for path in map_:
            path = path.strip()
            e = xml.etree.ElementTree.parse(path).getroot()

            newDict = {}
            for type in e:
                newDict[type.tag] = type.text
            parsedFiles.append(newDict)
        return parsedFiles

    @staticmethod
    def singleParse(filePath):
        parsedFiles = []
        e = xml.etree.ElementTree.parse(filePath).getroot()
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
        for attributes in XmlSearch.multiParse(domain):
            try:
                attributes['objectClass']
            except:
                continue
            if "user" in attributes['objectClass'].split(' ') and "person" in attributes['objectClass'].split(' '):
                try:
                    attributes['sAMAccountName']
                except:
                    continue

                try:
                    attributes['sAMAccountName'][-1]
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
        indexes = XmlSearch.loadMap()
        return_list = []
        for index in indexes:
            if user in index:
                filepath = index.strip()
        try:
            for attributes in XmlSearch.singleParse(filepath):
                return_list.append(attributes)
        except:
            return return_list
        return return_list


    @staticmethod
    def getGroups(domain):

        return_list = []
        for attributes in XmlSearch.multiParse(domain):
            try:
                attributes['objectClass']
            except:
                continue

            if "group" in attributes['objectClass'].split(' '):
                return_list.append(attributes['cn'])

        return return_list

    @staticmethod
    def groupMembership(group, domain):
        return_list = []
        path = XmlSearch.getPath(group)
        if len(path) == 0:
            return return_list

        for attributes in XmlSearch.singleParse(path):

            if attributes.get("objectClass") and "group" in attributes.get("objectClass"):
                try:
                    attributes['member']
                except:
                    continue
                if group in attributes['cn']:
                    for objectName in attributes['member'].split(','):
                        if 'CN=' in objectName:
                            userPath = XmlSearch.getPath(objectName.split('CN=')[1])
                            user_attr = XmlSearch.singleParse(userPath)
                            return_list.append(user_attr[0])

        return return_list

    @staticmethod
    def getByKeyword(keyword):
        return_list = []
        path = XmlSearch.getPath(keyword)
        if type(path) == list:
            for path in XmlSearch.getPath(keyword):
                for attributes in XmlSearch.singleParse(path):
                    return_list.append(attributes)
        else:
            return_list.append(XmlSearch.singleParse(path))
        return return_list


    @staticmethod
    def getPolicies(domain):
        pass
