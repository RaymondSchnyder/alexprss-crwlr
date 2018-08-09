import requests, json
import os
import urllib
import asyncio
from time import sleep
from pyrogram import Client, Filters
from pyrogram.api.errors import (
    BadRequest, Flood, FloodWait, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)
app = Client("fuck off alda xd")




def send_nude(path,user):
    sleep(2)
    #"-1001335524344
    try:
        app.send_photo(chat_id="aliexpressbitches", photo=path, caption=user)
    except FloodWait as e:
        print("sleeping now for" + str(e.x))
        sleep(e.x)
        pass

def download_pic(link,filename):
    try:
     request = requests.get(link, allow_redirects=True)
     open(filename, 'wb').write(request.content)
    except Exception as inst:
        print(inst)
        print('  Encountered unknown error. Continuing.')
        exit(500)
DOWNLOADS_DIR = 'downloaded/'

url = "https://fun.aliexpress.com/promotion/bikini-contest/teams/"
id = [50000627002,50000636004,50000627003,50000627004,50000639002]
url2= "/feeds?sort=1"


@app.on_message(Filters.incoming & Filters.private)
def main(client,message):
    print("Start downloading...")
    download()

def download():
    sleep(2)
    f = open('links.txt', 'r')
    lines = [line.rstrip('\n') for line in f]
    f.close()
    for index,value in enumerate(id):
        #print(value)
        request_url=url + str(value) + url2
        r = requests.get(request_url)
        json_data = r.json()
        for x in json_data["body"]["list"]:
            picid=str(x["id"])
            picurl=x["mainPic"]
            picusername=x["nickName"]
            print("ID: " + picid)
            print("ImageURL: " + picurl)
            print("Username: " + picusername)
            filename=DOWNLOADS_DIR+picid+".jpg"
            if picid not in lines:
                print("file " + picid + " doesnt exists! Downloading...")
                download_pic(picurl,filename)
                print("file " + picid + " fully downloaded!")
                print("file " + picid + " sending now nude!")
                send_nude(filename,picusername)
                print("file " + picid + " nude sent!")
                w = open('links.txt', 'a+')
                w.write(picid + "\r\n")
                w.close()
            else:  # not found
                print("file " + picid + " already exists")

app.run()
