from __future__ import print_function
from impacket.ldap import ldap, ldapasn1
from datetime import datetime
import sys
import os
from dicttoxml import dicttoxml
import argparse
import getpass
from submodules import *
import xml.etree.cElementTree as ET
import datetime

'''Things to do'''
'''
Please thread the xml parsing holy FUCK
Update readme to reflect the new output formats
xml output for groupMembership
xls output for all

if xml output:
parse EVERYTHING and create xml attributes with EVERYTHING and what values and attributes it holds

'''

class Belch:

    def __init__(self, u_name=None, passwd=None, domain=None, options=None):
        self.u_name = u_name
        self.passwd = passwd
        self.domain = domain
        self.options = options
        self.baseDN = ''
        self.spl = len(self.domain.split('.')) * -1

        for domainParts in domain.split('.'):
            self.baseDN += 'dc={},'.format(domainParts)
        self.baseDN = self.baseDN[:-1]

        self.objects = []

    def processRecord(self, data):
        if isinstance(data, ldapasn1.SearchResultEntry) is not True:
            return

        info = []
        for i,attribute in enumerate(data['attributes']):
            if attribute['type'] == 'distinguishedName':
                self.generatePath(attribute['vals'][0])

            values = {}
            values[str(attribute['type'])] = str(attribute['vals']).strip('SetOf:').lstrip()
            info.append(values)

        self.generateXml(info)

    ##Create Directories based off of the distinguishedName
    def generatePath(self, dn):
        path = ''
        for x in reversed(str(dn).split(',')[:self.spl]):
            path = '{}/'.format(self.domain)
            for y in list(reversed(str(dn).split(',')[:self.spl])):
                path += y[3:]+'/'

        try:
            os.makedirs(path)
        except Exception as err:
            ##Will have a bunch of file already exists error due to how path creation works
            pass


    def generateXml(self, info):
        newDict = {}
        for dic in info:
            newDict[dic.keys()[0]] = dic.values()[0]

        dn = newDict['distinguishedName']
        path = '{}/'.format(self.domain)
        for x in reversed(str(dn).split(',')[:self.spl]):
            path = '{}/'.format(self.domain)
            for y in list(reversed(str(dn).split(',')[:self.spl])):
                path += y[3:]+'/'
        path += 'index.xml'

        file = open(path, 'w')
        xml = dicttoxml(newDict)
        file.write(xml.decode())
        file.close()

        return

    def printUsers(self):
        cacheSearch = XmlSearch.printUsers(self.domain)

        computerAccounts = cacheSearch['computerAccounts']
        userAccounts = cacheSearch['userAccounts']

        if options.stdout:
            print("[+]All user accounts registered in the {} domain".format(self.domain))
            for i, user in enumerate(userAccounts):
                i +=1
                l = []
                [l.append(len(x)) for x in userAccounts]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(user, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(user, pad=pad), end='\n')

            print("\n[+]All system accounts registered in the {} domain".format(self.domain))
            for i, user in enumerate(computerAccounts):
                i +=1
                l = []
                [l.append(len(x)) for x in computerAccounts]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(user, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(user, pad=pad), end='\n')
        elif options.xml:
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

    def getUser(self, user):
        ##Print information for the specified group
        cacheSearch = XmlSearch.getUser(user, self.domain)
        if options.stdout:
            print("[+]Informaiton about the user: {}".format(user))
            for attributes in cacheSearch:
                l = []
                [l.append(len(x)) for x in attributes.keys()]
                pad = max(l)
                for attr, value in attributes.items():
                    print("{:{pad}}:{}".format(attr, value, pad=pad))

        elif options.xml:
            cacheSearch = XmlSearch.getUser(user, self.domain)
            for attributes in cacheSearch:
                file = open('{}_{}.xml'.format(self.domain, user), 'w')
                xml = dicttoxml(attributes)
                file.write(xml.decode())
                file.close()

        elif options.xls:
            print("XLS option")


    def printGroups(self):
        ##print all the print Groups

        ##Parse the objectClass to figure if somthing is a group
        cacheSearch = XmlSearch.getGroups(self.domain)
        if options.stdout:
            print("[+]Groups within the {} domain:".format(self.domain))
            for i, group in enumerate(cacheSearch):
                i +=1
                l = []
                [l.append(len(x)) for x in cacheSearch]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(group, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(group, pad=pad), end='\n')
        elif options.xml:
            root = ET.Element("{}".format(self.domain))
            groups = ET.SubElement(root, "groups")
            for group in cacheSearch:
                ET.SubElement(groups, "group", name=group).text = group
            tree = ET.ElementTree(root)
            tree.write('{}_groups.xml'.format(self.domain))

        elif options.xls:
            print("XLS option")

    def groupMembership(self, group):
        cacheSearch = XmlSearch.groupMembership(group, self.domain)

        if options.stdout:
            print('[+]Membership for: {}'.format(group))
            for i, user in enumerate(cacheSearch):
                i +=1
                l = []
                [l.append(len(x)) for x in cacheSearch]

                pad = max(l)
                if i % 3 != 0:
                    print("{:{pad}}|".format(user, pad=pad), end=' ')
                else:
                    print("{:{pad}}|".format(user, pad=pad), end='\n')

            print('\n[+]Caution, some of these might be other groups...')

        elif options.xml:
            root = ET.Element("{}".format(self.domain))
            groupName = ET.SubElement(root, group)
            for user in cacheSearch:
                ET.SubElement(groupName, "user", name=user).text = user
                ##Print out type={group, user}
                ##Print out attributes of each user once it gets created in submodules
            tree = ET.ElementTree(root)
            tree.write('{}_{}.xml'.format(self.domain, group))

        elif options.xls:
            print("XLS option")


    def run(self):

        ldapConnection = ldap.LDAPConnection('ldap://%s' % self.domain, self.baseDN)

        try:
            ldapConnection.login(self.u_name, self.passwd, self.domain)
            print('[+]Connected to {} as {}'.format(self.domain, self.u_name))
        except Exception as err:
            print(err)


            if self.options.users:
                ##Filter to grab only users
                filter = "(&(objectCategory=Person)(sAMAccountName=*))"
            elif self.options.computers:
                ##Filter to grab only computers
                filter = "(&(objectCategory=Computer)(objectClass=*))"
            elif self.options.username:
                ##Filter to grab only information for specified user
                filter = "(&(objectCategory=Person)(sAMAccountName={}))".format(self.options.username)
            elif self.options.computerName:
                ##Filter to grab only information for specified computer
                filter = "(&(objectCategory=Computer)(cn={}))".format(self.options.computerName)
            else:
                filter = "(&(objectCategory=*)(objectClass=*))"


        filter = "(&(objectCategory=*)(objectClass=*))"
        sc = ldap.SimplePagedResultsControl(size=100)

        ldapConnection.search(searchFilter = filter, searchControls=[sc], perRecordCallback=self.processRecord)

        #if self.options.stdout:
        #    tree(self.domain, ' ')

#executer = Belch("user", "user","Rose.Labs")


#executer.run()

#executer.groupMembership("Enterprise Admins")
#executer.printGroups()
#executer.printUsers()
#executer.getUser("STLCC0$")

if __name__ == "__main__":
    start_time = datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('target', action='store', help='domain/username[:password]')


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

    #other_group = parser.add_argument_group('Other options', description='Other options for searching through a mapped domain')
    ##keyword
    ##regex
    ##query

    output_group = parser.add_argument_group('Output options', description='Decide how to output the information')
    output_group.add_argument('--stdout', action='store_true', help='Print the output to the console')
    output_group.add_argument('-x', '--xml', action='store_true', help='Store the output into a xml file')
    output_group.add_argument('-e', '--xls', action='store_true', help='Store the output into a xls file')

    options = parser.parse_args()
    if '/' not in options.target:
        domain = options.target
        executer = Belch(domain=domain, options=options)
    else:
        domain = options.target.split('/')[0]
        if ':' in options.target.split('/')[1]:
            u_name = options.target.split('/')[1].split(':')[0]
            passwd = options.target.split('/')[1].split(':')[1]
        else:
            u_name = options.target.split('/')[1]
            passwd = getpass.getpass('Password:')

        if os.path.exists(domain):
            sys.exit('[!]Error: Domain map already exists, please delete before running again')

        executer = Belch(u_name, passwd, domain, options)

    if options.all or options.users or options.computers or options.username or options.computerName:
        if os.path.exists(domain):
            sys.exit('[!]Error: Domain map already exists, please delete before running again')
        else:
            os.mkdir(domain)
        executer.run()
    else:
        if os.path.exists(domain):
            if options.print_users:
                executer.printUsers()
            elif options.get_user:
                executer.getUser(options.get_user)
            elif options.print_groups:
                executer.printGroups()
            elif options.group_membership:
                executer.groupMembership(options.group_membership)
        else:
            sys.exit('[!]Error: Cannot locate domain directory')

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print("Time elapsed: ", elapsed_time.seconds, ":", elapsed_time.microseconds)
