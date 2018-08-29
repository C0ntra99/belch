from __future__ import print_function
from impacket.ldap import ldap, ldapasn1
from datetime import datetime
import sys
import os
from dicttoxml import dicttoxml
import argparse
import getpass
from submodules import *

###This is will create a full file structure of the Active Directory

##Create a folder for each OU
##Create a file for each thing inside OU
##Write the attributes and values of the CN to the file maybe in XML

'''Things that dont work'''
'''Anything with the SQL flag
    Write search ArgumentParser
        -given a chached domain will search for like thing
        -if no chached domain attempt to run main function on all the domain
        -walk through directories, if contents of index.xml meet the search criteria, then add path to a list
'''

class Belch:

    def __init__(self, u_name, passwd, domain, options):
        self.u_name = u_name
        self.passwd = passwd
        self.domain = domain
        self.options = options
        self.baseDN = ''
        self.spl = len(self.domain.split('.')) * -1

        ##Create the base directory
        os.mkdir(self.domain)

        for domainParts in domain.split('.'):
            self.baseDN += 'dc={},'.format(domainParts)
        self.baseDN = self.baseDN[:-1]

        self.objects = []

    def thing(self, data):
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
            print(err)

        if self.options.verbose:
            print("Path: ", path)

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

        if self.options.verbose:
            print("Path: ", path)
        file = open(path, 'w')
        xml = dicttoxml(newDict)
        file.write(xml.decode())
        file.close()

        ##Change time from unix times to human times
        ##Maybe I should do this before putting it in xml....maybe
        ##Parse group membership
        ##Maybe I should do this before putting it in xml....maybe
        return

    def run(self):

        ldapConnection = ldap.LDAPConnection('ldap://%s' % self.domain, self.baseDN)

        try:
            ldapConnection.login(self.u_name, self.passwd, self.domain)
            print('[+]Connected to {} as {}'.format(self.domain, self.u_name))
        except Exception as err:
            print(err)

        try:
            if self.options.users:
                ##Filter to grab only users
                filter = "(&(objectCategory=Person)(sAMAccountName=*))"
            elif self.options.computers:
                ##Filter to grab only computers
                filter = "(&(objectCategory=Computer)(objectClass=*))"
            else:
                filter = "(&(objectCategory=*)(objectClass=*))"
        except:
            if self.options.username:
                ##Filter to grab only information for specified user
                filter = "(&(objectCategory=Person)(sAMAccountName={}))".format(self.options.username)
            elif self.options.computer:
                ##Filter to grab only information for specified computer
                filter = "(&(objectCategory=Computer)(cn={}))".format(self.options.computer)
            else:
                sys.exit('[!]Please specify a target when using the "one" option.')


        sc = ldap.SimplePagedResultsControl(size=100)

        ldapConnection.search(searchFilter = filter, searchControls=[sc], perRecordCallback=self.thing)

        if self.options.stdout:
            tree(self.domain, ' ')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser.add_argument('-v', '--verbose', action='store_true', help='Print out paths as they are being created')
    parser_a = subparser.add_parser('all', help='Query a domain controller for all information unless otherwise specified')
    parser_a.set_defaults(which='all')

    parser_a.add_argument('target', action='store', help='domain/username[:password]')
    parser_a.add_argument('-u','--users', action='store_true', help='Pull all user information.', required=False)
    parser_a.add_argument('-c', '--computers', action='store_true', help='Pull all computer information.', required=False)

    group_a = parser_a.add_argument_group('output')
    group_a.add_argument('--stdout', action='store_true', help='Prints out a directory tree of the active directory network after the active directory gets mapped.')

    parser_b = subparser.add_parser('one', help='Query a domain controller for one user or computer')
    parser_b.set_defaults(which='one')

    parser_b.add_argument('target', action='store', help='domain/username[:password]')
    parser_b.add_argument('-u','--username', action='store', help='Pull information on specific user.')
    parser_b.add_argument('-c', '--computer', action='store', help='Pull information on a specific computer.')

    group_b = parser_b.add_argument_group('output')
    group_b.add_argument('--stdout', action='store_true', help='Prints out a directory tree of the active directory network after the active directory gets mapped.')

    parser_c = subparser.add_parser('print', help='Print from a previously cached domain')
    parser_c.set_defaults(which='print')

    parser_c.add_argument('-d', '--domain', action='store', help='Print out a previously mapped domain to stdout')
    parser_c.add_argument('-g', '--groups', action='store_true', help='Print out all the groups')
    parser_c.add_argument('-o', '--ou', action='store_true', help='Print out all OUs of the domain')
    parser_c.add_argument('-u', '--users', action='store_true', help='Print out all the users on a domain')

    parser_d = subparser.add_parser('search', help='Search from a previously cached domain')
    parser_d.set_defaults(which='search')

    parser_d.add_argument('-d', '--domain', action='store', help='Domain to search through')
    ##This might need to be moved to print, idk ye
    parser_d.add_argument('-g', '--group', action='store', help='Print all users in the specified group', required=False)
    parser_d.add_argument('-u', '--user', action='store', help='Search for the user specified', required=False)
    parser_d.add_argument('-re', '--regex', action='store', help='Search through everything and return items that match the regular expression', required=False)
    parser_d.add_argument('-k', '--keyword', action='store', help='Return everything that matches the keyword', required=False)
    parser_d.add_argument('-q', '--query', action='store', help='Queries a previously mapped domain similar to a real domain. Will return any matching')

    options = parser.parse_args()

    ##Fix how this is figured
    ##Multiple try excepts is unreliable
    if options.which == 'all' or options.which == 'one':
        domain = options.target.split('/')[0]
        if ':' in options.target.split('/')[1]:
            u_name = options.target.split('/')[1].split(':')[0]
            passwd = options.target.split('/')[1].split(':')[1]
        else:
            u_name = options.target.split('/')[1]
            passwd = getpass.getpass('Password:')

        if os.path.exists(domain):
            sys.exit('[!]Domain map already exists, please delte before running again')
        else:
            executer = Belch(u_name, passwd, domain, options)
            executer.run()

    elif options.which == 'print':
        if os.path.exists(options.domain):
            tree(options.domain, ' ')
        else:
            sys.exit("[!]Domain map does not exist.")

    elif options.which == 'search':
        ##Do cool searching shit with xml shit and other cool shit
        ##Parse though the search options
        cacheSearch = xmlSearch(options)
        if options.user:
            print("[+]Informaiton about the user: {}".format(options.user))
            for attributes in cacheSearch:
                l = []
                [l.append(len(x)) for x in attributes.keys()]
                pad = max(l)
                for attr, value in attributes.items():
                    print("{:{pad}}:{}".format(attr, value, pad=pad))

        if options.group:
            print('[+]Membership for: {}'.format(options.group))
            l = []
            [l.append(len(x['cn'])) for x in cacheSearch]
            pad = max(l)
            for i, x  in enumerate(cacheSearch):
                if i % 3 == 0:
                    print("{:{pad}}".format(x['sAMAccountName'], pad=pad), end='\n')
                else:
                    print("{:{pad}}".format(x['sAMAccountName'], pad=pad), end = '\t')

        if options.keyword:
            print(cacheSearch)
