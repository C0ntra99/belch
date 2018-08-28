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
Since there is no requirements.txt yet you might run into some dependency issues, just keep running it and instal all the missing depencies.
If both python 2.7 and 3.6 are installed on your system please run this

```
python2 belch.py -h
```
Otherwise run

```
python belch.py -h
```
If all goes well you should be presented with the usage page.

## Using belch

As of right now the only way to use belch is to use the following command:
```
python2 belch.py all domain/username[:password]
```
The ```-v``` and ```--stdout``` flags will also work with this command.
Will the ```all``` option it wil pull everything from the domain and create folders for everything, and create coresponding 'index.xml' files to store all the attributes. If a password is not provided it will prompt for one.

Example:
```
python2 belch.py all example.com/user:user
```

If you already have a mapped domain in the same directory of the main program you can print it out to the screen buy using
``` 
python2 belch.py print -d domain
```
Example:
```
python2 belch.py print -d example.com
```

## Future plans
Currently there are plans to add the following:
* SQL database for easy searching
* This might have to be a eperate program
* Querying for only computers or users
* Querying for only one computer or user
* Maybe even a flask frontend....maybe
* Built in XML parser

This is why you may see flags that do not work. Once they do work I will update the readme.

## Acknowledgments

* Could have done this without the help of the people at coresecurity (https://github.com/CoreSecurity)
