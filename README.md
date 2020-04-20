Python scripts used to perform various bulk actions via the ArchivesSpace API
## Authenticating to the API

Because these scripts are mostly edited scripts from different sources, they require different authentication methods. Some require a secrets.py file in the same directory that must contain the following text:

  baseURL='[ArchivesSpace API URL]'
  user='[user name]'
  password='[password]'
  repository='[repository]'

Some will request login information within the command line after starting running a script, some require the ArchivesSpace module written by Tristan Chambers for authentication, and some require ArchivesSnake.
