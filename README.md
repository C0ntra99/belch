# Belch

This program was built with the idea of mapping active directories. Belch will take domain credentials and proceed to either dump out everything on the AD or specified objects. Belch uses the ldap library from impacket (https://github.com/CoreSecurity/impacket)

## What it does

Belch will create a mapping of any active directory network. Active directories consitst of many organizational units(OU) and containers within those OUs. What belch will do by default is query the active directory for everything it has, and then proceed to craft folders for everything that it revcieves. Another cool thing with AD is there are attributes for just about anything that is stored on the AD, so belch will take all attributes that are related to that OU or container and create a index.xml within the folder related to it. After belch is finished there will be a mapping of the everything on the active directory network for future use.

## Getting Started

How to get everything started up and going before running. Currently this has only been tested on a linux machine, I will update the readme when windows has been tested.

### Prerequisites

Programs to have before installation

#### Python 2.7

This program is written using the Impacket LDAP libreary which is written in python 2.7, so the program is self has to be written in python 2.7. If the program is run with python 3 it will error out.

#### pipenv

Pipenv is used to keep everything in one place and to make sure belch's dependencies don't clash with any other dependencies that are installed on your machine.

### Installing

Make sure you are in the belch directory and run:

```
pipenv install
'''
To install all of belch's dependencies, and then run:
'''
pipenv shell
```

To get into the virtual environment. After this you can run `python belch.py -h` to view the arguments.

## Using belch

### Mapping a domiain

To map everything on a domain simply enter:

```
python belch.py -a domain/username[:password]
```

Will the `-a` option it will pull everything from the domain and create folders for all the OUs and CNs, and also create corresponding 'index.xml' files to store all the attributes for the object. If a password is not provided it will prompt for one.

Example:

```
python belch.py -a example.com/user:user
```

It is also possible to only grab user or only grab computer. To do that all you need to do is replace `-a` with `-u` for users or `-c` for computers with the command.

Example:

```
python belch -u example.com/user:user
```

If you are wanting to only grab one specific user of one specific computer use the `-uN USERNAME` or `-cN COMPUTERNAME` flags.

### Searching

The search function requires an already mapped domain. So far the only things you can search for are: Single users, all users, group membership for one group, all the groups, and keyword search. In the future you will be able to craft your own LDAP query, and use regex

When specifying the domain just exclude the username and password.

Examples:

```
python belch.py example.com -pU
```

```
python belch.py example.com -gM "Domain admins"
```

The keyword search is a little different. It will search the domainMap for all objects that math the keyword you provide. Note that this does not search inside the XML files, just the domainMap.
'''
python belch.py example.com -k "Test User"
'''

#### Xml output

With the searching function in belch you can store the output into an xml file. The xml files will usually have more information and just regular stdout.

To do this just put the `-x` on the end of your search command:

```
python belch.py example.com -gU testUser -x
```

## Future plans

Currently there are plans to add the following:

- Maybe a flask frontend....maybe
- Allow for a user to specify path of the mapped domain
- More search options
- Output options like excel
- Fix time from unix time when printing, but not when storing
- Maybe try and write a program to recreate the domain from the mapped domain...

## Disclaimer

This program is extremly loud on a network and is not considered opsec safe. Run at your own risk.
