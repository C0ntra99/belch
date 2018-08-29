# Belch

This program was built with the concept of spitting out information, in our case Active Directory information. Belch will take a domain credentials and proceded to either dump out everything on the AD or certain things. There will be a few options for storing this information, with the current release the only options is to create a mapping with folders and XML files.

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
* Maybe I forgot a dependency, just install manually
* Make sure you have the right permission to run these commands, if not run as sudo

## Using belch

### Mapping a domiain
To map everything on a domain simply enter:
```
python2 belch.py all domain/username[:password]
```
The ```-v``` and ```--stdout``` flags will also work with this command.
Will the ```all``` option it wil pull everything from the domain and create folders for everything, and create corresponding 'index.xml' files to store all the attributes. If a password is not provided it will prompt for one.

Example:
```
python2 belch.py all example.com/user:user
```

With the latest release it is possible to only grab user or only grab computer. To do that all you need to do is use the ```-u``` or ```-c``` flags with the command.

Example:
```
python2 belch all -u example.com/user:user
```

### Printing
If you already have a mapped domain in the same directory of the main program you can print it out various attributes of that domain buy using ```print```.

To print out the groups:
```
python2 belch.py print -d domain -g
```

To print out the users:
```
python2 belch.py print -d domain -u
```

Examples:
```
python2 belch.py print -d example.com -g
```
```
python2 belch.py print -d example.com -u
```

### Searching
Similar to the print function the search funtion requires an already mapped domain. So far the only things you can search for are: Group membership, users, and keywords. In the future you will be able to craft your own LDAP query.

To start type:
```
python2 belch.py search -h
```

Examples:
```
python2 belch.py search -d example.com -u jdoe
```
```
python2 belch.py search -d example.com -g "Domain admins"
```

Please note that the searching is not yet complete, the only flags that currently work are ```-u``` and ```-g```. 

## Future plans
Currently there are plans to add the following:
* Maybe even a flask frontend....maybe


## Acknowledgments

* Could have done this without the help of the people at coresecurity (https://github.com/CoreSecurity)
