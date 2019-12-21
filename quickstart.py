#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import codecs
from apiclient import errors
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import re, time
#enabling the terminal to print unicode characters.
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)

#determining what information will the app try to access.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
#this is where the tokens received from the api will be stored.
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))


def make_html_name(folder_name):
    folder_name_striped = folder_name.strip()
    folder_name_list = folder_name_striped.split()
    folder_name_joined = '_'.join(folder_name_list)
    to_file = "results/" + folder_name_joined + ".html"
    return to_file

def make_html_link_name(folder_name):
    folder_name_striped = folder_name.strip()
    folder_name_list = folder_name_striped.split()
    folder_name_joined = '_'.join(folder_name_list)
    to_file = folder_name_joined + ".html"
    return to_file

def elim_ext(c):
    #eliminating the file extension with regular expressions 
    pattern = re.compile(r'\.\w+\b')  # creating a pattern.
    b = ''
    for f in c:
        match = pattern.search(f['name']) # searching for a match.
        if match is not None:
            a = f['name'].replace(match.group(), b) # creating a new string
            f['name'] = a # replacing the value of the key with the new string.
    return c


def sort_f(c):
    #sorting the files' metadata according to the alpahbetic order of the file names.
    d = []
    for f in c:
        d.append(f['name'].upper())
    g = sorted(d)

    # checking for duplicate items.
    #print ("List count:", len(g))
    f = set(g)
    #print ("Set count:", len(f))

    # adding urls to file names
    e = []
    count = 0
    for item in g:
        for f in c:
            if item == f['name'].upper():
                e.append(f)
                i = c.index(f)
                del c[i]
                count +=1
                break  #stops loop after first match is found (necessary because there repeated items)
    return e


def write_to_file(e, to_file, folder_name):
    # writting data to a .txt file. If there iscurrently no file it creates a new one.
    count = 0
    with open(to_file, 'wb+') as f:
        #for line in range(9):
            #reader = f.readline()
        # = f.tell()
        #print (current_position)
        #f.seek(current_position) 
        #page_title = "<h1>Sadržaj drive-a/folder: {}</h1><hr><br>\n<div>".format(folder_name)
        #page_title = page_title.encode('utf-8')
        #f.write(page_title)
        for item in e:
            if type(item) == dict:
                content = "<a href='"
                thing1 = item['webViewLink']
                thing2 = "'>"
                thing3 = item['name']
                thing4 = "</a><br>"
                my_str = "\n"
                line = content + thing1 + thing2 + thing3 + thing4 + my_str
                line = line.encode('utf-8')
                f.write(line)
                count += 1
            else:
                my_str = "\n"
                line = item + my_str
                print (line)
                line = line.encode('utf-8')
                f.write(line)
                count += 1
    print ("File count:", count)
    print ("Your files have been successfully listed!")

   
def get_folder_data(folder_id, folder_name):
    page_token = None
    c = []
    d = []
    count = 0
    check = 0
    while True:
    #parameters to the list function determine what data in the given scope will be retrieved.
        files = DRIVE.files().list(q="'{}' in parents".format(folder_id), pageSize = 100, fields = 'nextPageToken, files(name, webViewLink, id, mimeType)',
            pageToken = page_token).execute()

        for file in files.get('files', []):
            #print (file.get('name'), file.get('id'), file.get('webViewLink'))
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                #print (file['mimeType'])
                #print (file['id'])

                file['webViewLink'] = make_html_link_name(file['name'])
                d.append(file)
                get_folder_data(file['id'], file['name'])
                check += 1

            else:
                c.append(file)
                count += 1

        page_token = files.get('nextPageToken', None)
        if page_token is None:
            break
    c = elim_ext(c)
    e = sort_f(c)
    d = elim_ext(d)
    d = sort_f(d)
    l = ["<br>"]
    h = d + l + e
    to_file = make_html_name(folder_name)
    write_to_file(h, to_file, folder_name )

#print (len(c))

folder_name = input("Enter folder name:")

time.sleep(1)

folder_id = input("Enter the folder id:")

get_folder_data(folder_id, folder_name)





    

           