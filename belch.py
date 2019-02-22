from __future__ import print_function
from impacket.ldap import ldap, ldapasn1
from datetime import datetime
import sys
import os
from dicttoxml import dicttoxml
import getpass
from submodules import *
import xml.etree.cElementTree as ET
import datetime
from colorama import Fore, Back, Style, init



class Belch:

    def __init__(self, u_name=None, passwd=None, domain=None, options=None):
        self.u_name = u_name
        self.passwd = passwd
        self.domain = domain
        self.options = options
        self.baseDN = ''
        self.lmhash = ''
        self.nthash = ''

        if options.hash is not None:
            self.lmhash, self.nthash = options.hash.split(':')

        self.spl = len(self.domain.split('.')) * -1

        for domainParts in domain.split('.'):
            self.baseDN += 'dc={},'.format(domainParts)
        self.baseDN = self.baseDN[:-1]

        self.objects = []

    def processRecord(self, data):
        if isinstance(data, ldapasn1.SearchResultEntry) is not True:
            return

        info = []
        for _,attribute in enumerate(data['attributes']):
            if attribute['type'] == 'distinguishedName':
                self.generatePath(attribute['vals'][0])

            values = {}
            values[str(attribute['type'])] = str(attribute['vals']).strip('SetOf:').lstrip()
            info.append(values)

        self.generateXml(info)

    def generatePath(self, dn):
        path = ''
        for _ in reversed(str(dn).split('=')[:self.spl]):
            path = '{}/'.format(self.domain)

            for y in list(reversed(str(dn).split('=')[:self.spl])):
                path += y[:-3]+'/'
        
        for special in '\:*?"<>|':
            path = path.replace(special, "")

        try:
            os.makedirs(path)
        except Exception as _:
            pass


    def generateXml(self, info):
        domainMap = open('domainMap', 'a')
        newDict = {}
        for dic in info:
            newDict[dic.keys()[0]] = dic.values()[0]

        dn = newDict['distinguishedName']
        path = '{}/'.format(self.domain)
        for _ in reversed(str(dn).split('=')[:self.spl]):
            path = '{}/'.format(self.domain)
            for y in list(reversed(str(dn).split('=')[:self.spl])):
                path += y[:-3] + '/'
        for special in '\:*?"<>|':
            path = path.replace(special, "")
        path = path[:-1] + 'index.xml'

        domainMap.write(path + "\n")
        domainMap.close()
        file = open(path, 'w')
        xml = dicttoxml(newDict)
        file.write(xml.decode())
        file.close()

        return

    def printUsers(self):
        cacheSearch = XmlSearch.printUsers(self.domain)

        computerAccounts = cacheSearch['computerAccounts']
        userAccounts = cacheSearch['userAccounts']

        if options.xml:
            root = ET.Element("{}".format(self.domain))
            accounts = ET.SubElement(root, "accounts")
            for user in userAccounts:
                ET.SubElement(accounts, "userAccount", type='userAccount').text = user
            for computer in computerAccounts:
                ET.SubElement(accounts, "computerAccount", type='computerAccounts').text = computer

            tree = ET.ElementTree(root)
            tree.write('{}_accounts.xml'.format(self.domain))
        elif options.xls:
            print("xls options")

        else:
            print(running, end='')
            print("All user accounts registered in the {} domain".format(self.domain))
            for i, user in enumerate(userAccounts):
                i +=1
                l = []
                [l.append(len(x)) for x in userAccounts]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(user, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(user, pad=pad), end='\n')

            print('\n'+running, end='')
            print("All system accounts registered in the {} domain".format(self.domain))
            for i, user in enumerate(computerAccounts):
                i +=1
                l = []
                [l.append(len(x)) for x in computerAccounts]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(user, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(user, pad=pad), end='\n')

    def getUser(self, user):

        if options.xml:
            cacheSearch = XmlSearch.getUser(user, self.domain)
            for attributes in cacheSearch:
                file = open('{}_{}.xml'.format(self.domain, user), 'w')
                xml = dicttoxml(attributes)
                file.write(xml.decode())
                file.close()

        elif options.xls:
            print("XLS option")

        else:
            cacheSearch = XmlSearch.getUser(user, self.domain)
            if len(cacheSearch) == 0:
                print(error, end='')
                sys.exit('Error: No objects were found')
            print(running, end='')
            print("Informaiton about the user: {}".format(user))
            for attributes in cacheSearch:
                l = []
                [l.append(len(x)) for x in attributes.keys()]
                pad = max(l)
                for attr, value in attributes.items():
                    print("{:{pad}}:{}".format(attr, value, pad=pad))


    def printGroups(self):

        cacheSearch = XmlSearch.getGroups(self.domain)

        if options.xml:
            root = ET.Element("{}".format(self.domain))
            groups = ET.SubElement(root, "groups")
            for group in cacheSearch:
                ET.SubElement(groups, "group", name=group).text = group
            tree = ET.ElementTree(root)
            tree.write('{}_groups.xml'.format(self.domain))

        elif options.xls:
            print("XLS option")

        else:
            print(running, end='')
            print("Groups within the {} domain:".format(self.domain))
            for i, group in enumerate(cacheSearch):
                i +=1
                l = []
                [l.append(len(x)) for x in cacheSearch]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(group, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(group, pad=pad), end='\n')

    def groupMembership(self, group):
        cacheSearch = XmlSearch.groupMembership(group, self.domain)
        if len(cacheSearch) == 0:
            print(Fore.RED + '[!]', end='')
            sys.exit('Error: No group has been found')

        if options.xml:
            root = ET.Element("{}".format(self.domain))
            groupName = ET.SubElement(root, group)
            for user in cacheSearch:
                userElement = ET.SubElement(root, "member", name=user['cn'])
                for key in user:
                    ET.SubElement(userElement, key, name=key).text = user[key]
            tree = ET.ElementTree(root)
            tree.write('{}_{}.xml'.format(self.domain, group))

        elif options.xls:
            print("XLS option")

        else:
            print(running, end='')
            print('Membership for: {}'.format(group))
            for i, user in enumerate(cacheSearch):
                i +=1
                l = []
                [l.append(len(x['cn'])) for x in cacheSearch]

                pad = max(l) + 5
                if i % 3 != 0:
                    print("{:{pad}}|".format(user["cn"], pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(user["cn"], pad=pad), end='\n')
            print('\n'+waiting, end='')
            print('Caution, some of these might be other groups...')

    def keywordSearch(self, keyword): 
        cacheSearch = XmlSearch.getByKeyword(keyword)
        ##print(cacheSearch)
        if len(cacheSearch) == 0:
            print(error, end='')
            print("Nothing was found matching the keyword: {}".format(keyword))
            return

        print(running, end='')
        if options.xml:
            print(error, end='')
            print("This funciton does not yet work.")
            return
            #root = ET.Element("{}".format(self.domain))
            #groupName = ET.SubElement(root, group)
            root = ET.Element("{}".format(self.domain))
            if len(cacheSearch) > 1:
                for x in cacheSearch:
                    searchReturn = ET.SubElement(root, keyword)
                    for attributes in x:
                        userElement = ET.SubElement(root, "member", name=attributes['cn'])
                        for key in attributes:
                            ET.SubElement(userElement, key, name=key).text = attributes[key]
                tree = ET.ElementTree(root)
                tree.write('{}_{}.xml'.format(self.domain, keyword))
            return

        print("Informaiton about the on the keyword: {}".format(keyword))
        if len(cacheSearch) > 1:
            for x in cacheSearch:
                for attributes in x:
                    l = []
                    ##print(attributes)
                    [l.append(len(x)) for x in attributes.keys()]
                    pad = max(l)
                    for attr, value in attributes.items():
                        print("{:{pad}}:{}".format(attr, value, pad=pad))
                    print("~" * 50)
        else:
            for attributes in cacheSearch[0]:
                l = []
                [l.append(len(x)) for x in attributes.keys()]
                pad = max(l)
                for attr, value in attributes.items():
                    print("{:{pad}}:{}".format(attr, value, pad=pad))
                print("~" * 50)

    def run(self):

        try:
            ldapConnection = ldap.LDAPConnection('ldap://%s' % self.domain, self.baseDN)
            ldapConnection.login(self.u_name, self.passwd, self.domain, self.lmhash, self.nthash)
            print(running, end='')
            print('Connected to {} as {}'.format(self.domain, self.u_name))
            os.mkdir(self.domain)
        except Exception as err:
            if 'invalidCredentials' in str(err):
                print(error, end='')
                sys.exit('Error: Invalid credentials')
            if 'Connection error' in str(err):
                print(error, end='')
                sys.exit('Error: Cannot connect to server')


        if self.options.users:
            filter = "(&(objectCategory=Person)(sAMAccountName=*))"
        elif self.options.computers:
            filter = "(&(objectCategory=Computer)(objectClass=*))"
        elif self.options.username:
            filter = "(&(objectCategory=Person)(sAMAccountName={}))".format(self.options.username)
        elif self.options.computerName:
            filter = "(&(objectCategory=Computer)(cn={}))".format(self.options.computerName)
        else:
            filter = "(&(objectCategory=*)(objectClass=*))"



        sc = ldap.SimplePagedResultsControl(size=100)

        print(Fore.YELLOW + '[-]', end='')
        print("Starting to map the domain, this could take a while...")
        ldapConnection.search(searchFilter = filter, searchControls=[sc], perRecordCallback=self.processRecord)


if __name__ == "__main__":
    start_time = datetime.datetime.now()

    init(autoreset=True)
    running = Fore.GREEN + "[+]"
    waiting = Fore.YELLOW + "[-]"
    error = Fore.RED + "[!]"

    options = Args.getArgs()

    if len(sys.argv) < 3:
        print(error, end='')
        sys.exit('Please specify an option')
        
    

    if '/' not in options.target:
        domain = options.target
        executer = Belch(domain=domain, options=options)
    else:
        domain = options.target.split('/')[0]
        if os.path.exists(domain) and os.path.exists('domainMap'):
            print(waiting, end='')
            answer = str(raw_input('Domain mapping already exists, would you like to rename?[Y/n]'))
            if answer.lower() == 'n':
                print(error, end='')
                sys.exit('Error: Domain map already exists, please rename or delete before running again')
            elif answer.lower() == 'y' or answer == '':
                os.rename(domain, domain+'.bak')
                os.rename('domainMap', domain+'.map')
            else:
                print(error, end='')
                sys.exit('Error: That is not a valid option')

        if ':' in options.target.split('/')[1]:
            u_name = options.target.split('/')[1].split(':')[0]
            passwd = options.target.split('/')[1].split(':')[1]
        else:
            u_name = options.target.split('/')[1]
            print(waiting, end='')
            passwd = getpass.getpass('Password:')
        executer = Belch(u_name, passwd, domain, options)
        

    if options.all or options.users or options.computers or options.username or options.computerName:
        executer.run()
        print(running, end='')
        print("Belch has finished, run 'belch.py -h' to view more options")
    else:
        if os.path.exists(domain):
            parseLen = sum(1 for _ in open('domainMap'))
            if options.print_users:
                print(waiting, end="")
                print("Parsing {} files for all user information".format(parseLen))
                executer.printUsers()
            elif options.get_user:
                print(waiting, end="")
                print("Getting information for: {}".format(options.get_user))
                executer.getUser(options.get_user)
            elif options.print_groups:
                print(waiting, end="")
                print("Parsing {} files for all group information".format(parseLen))
                executer.printGroups()
            elif options.group_membership:
                print(waiting, end="")
                print("Retrieving membership for the group: {}".format(options.group_membership))
                executer.groupMembership(options.group_membership)
            elif options.keyword:
                print(waiting, end="")
                print("Parsing {} files for the keyword {}".format(parseLen, options.keyword))
                executer.keywordSearch(options.keyword)
        else:
            sys.exit(Fore.RED + '[!]Error: Cannot locate domain directory')

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print(waiting, end='')
    print("Time elapsed: ", elapsed_time.seconds, ":", elapsed_time.microseconds)
