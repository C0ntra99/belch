import xml.etree.cElementTree

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
        else:
            return str(return_list[0])

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
        for attributes in XmlSearch.singleParse(filepath):
            return_list.append(attributes)
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
        for attributes in XmlSearch.singleParse(XmlSearch.getPath(group)):

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
        for path_ in XmlSearch.getPath(keyword):
            for attributes in XmlSearch.singleParse(path_):
                return_list.append(attributes)
        return return_list


    @staticmethod
    def getPolicies(domain):
        pass
