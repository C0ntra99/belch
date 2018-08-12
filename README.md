# Belch

This program was built with the concept of spitting out information, in our case Active Directory information. Belch will take domain credentials and proceed to either dump out everything on the AD or specified objects. There will be a few options for storing this information, with the current release the only options is to create a mapping with folders and XML files.

## What it does
Belch will create a mapping of any active directory network. Active directories consitst of many organizational units(OU) and containers within those OUs. What belch will do by default is query the active directory for everything it has, and then proceed to craft folders for everything that it revcieves. Another cool thing with AD is there are attributes for just about anything that is stored on the AD, so belch will take all attributes that are related to that OU or container and create a index.xml within the folder related to it. After belch is finished there will be a mapping of the everything on the active directory network for future use.

## Getting Started

How to get everything started up and going before running. Currently this has only been tested on a linux machine, I will update the readme when windows has been tested.

### Prerequisites

Programs to have before installation

#### Python 2.7
This program is written using the Impacket LDAP libreary which is written in python 2.7, so the program is self has to be written in python 2.7. If the program is run with python 3 it will error out.

#### Impacket
```
git clone https://github.com/CoreSecurity/impacket
pip install .
```
If this does not work please refer to the Impacket documentation located at https://github.com/CoreSecurity/impacket

### Installing

Now the fun part. Installing belch for yourself!

```
git clone https://github.com/C0ntra99/belch
cd belch
```

If both python 2.7 and 3.6 are installed on your system please run this

```
pip2 install -r requirements.txt
python2 belch.py -h
```
Otherwise run

```
pip install -r requirements.txt
python belch.py -h
```

If all goes well you should be presented with the usage page. If not check the following things:
* You are using pip2 and python2
* Maybe I forgot a dependency, if this is the case just install manually
* Make sure you have the right permission to run these commands, if not run as sudo

## Using belch

### Mapping a domiain
To map everything on a domain simply enter:
```
python2 belch.py -a domain/username[:password]
```

Will the ```-a``` option it will pull everything from the domain and create folders for all the OUs and CNs, and also create corresponding 'index.xml' files to store all the attributes for the object. If a password is not provided it will prompt for one.

Example:
```
python2 belch.py -a example.com/user:user
```

It is also possible to only grab user or only grab computer. To do that all you need to do is replace ```-a``` with ```-u``` for users or ```-c``` for computers with the command.

Example:
```
python2 belch -u example.com/user:user
```

If you are wanting to only grab one specific user of one specific computer use the ```-uN USERNAME``` or ```-cN COMPUTERNAME``` flags.

### Searching
The search function requires an already mapped domain. So far the only things you can search for are: Single users, all users, group membership for one group, and all the groups. In the future you will be able to craft your own LDAP query, search by keyword, and use regex

When specifying the domain just exclude the username and password.  

Examples:
```
python2 belch.py example.com -pU
```
```
python2 belch.py example.com -gM "Domain admins"
```

## Future plans
Currently there are plans to add the following:
* Maybe a flask frontend....maybe
* Allow for a user to specify path of the mapped domain
* More search options
* Output options like excel or xml
* Fix time from unix time when printing, but not when storing
* Maybe try and write a program to recreate the domain from the mapped domain...

## Disclaimer
This program has blueteams in mind, that being said this is extremely loud on the network and is not considered opsec safe. Run at your own risk.
