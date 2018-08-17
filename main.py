import requests, json
import os
import asyncio
from time import sleep
from pyrogram import Client, Filters
from concurrent import futures
from pyrogram.api.errors import (
    BadRequest, Flood, FloodWait, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)
dir = "config/"
c = open(dir + 'api.conf', 'r')
api_config = [line.rstrip('\n') for line in c]
print(api_config[0])
c.close()
app = Client(api_config[0])


def send_nude(path, user):
    sleep(2)
    # "-1001335524344
    try:
        app.send_photo(chat_id="aliexpressbitches", photo=path, caption=user)
    except FloodWait as e:
        print("sleeping now for" + str(e.x))
        sleep(e.x)
        pass


def download_pic(link, filename):
    try:
        print("downloading: " + link + " to file: " + filename)
        request = requests.get(link, allow_redirects=True)
        request.raw.decode_content = True
        open(filename, 'wb').write(request.content)
    except Exception as inst:
        print(inst)
        print('  Encountered unknown error. exiting.')
        exit(500)


DOWNLOADS_DIR = 'downloaded/'

url = "https://fun.aliexpress.com/promotion/bikini-contest/teams/"
id = [50000627002, 50000636004, 50000627003, 50000627004, 50000639002]
url2 = "/feeds?sort=1"


@asyncio.coroutine
def looper(loop):
    while loop.is_running():
        print("\n\r Starting loop task \n\r")
        tasks = [
            download()
        ]
        print("\n\r Closing loop task \n\r")
        yield from asyncio.wait(tasks)

@app.on_message(Filters.incoming & Filters.private & Filters.command("start"))
def start(client, message):
    print("Start downloading...")
    event_loop.run_forever()
    #download()


@app.on_message(Filters.incoming & Filters.private & Filters.command("stop"))
def stop(client, message):
    print("Stopping bot...")
    event_loop.stop()
    exit(200)

@asyncio.coroutine
def download():
    asyncio.sleep(2)
    f = open(dir + 'links.txt', 'r')
    lines = [line.rstrip('\n') for line in f]
    f.close()
    for index, value in enumerate(id):
        print("\r\nSearching now in " + str(index) + " " + str(value) + " \r\n")
        request_url = url + str(value) + url2
        r = requests.get(request_url)
        json_data = r.json()
        for x in json_data["body"]["list"]:
            picid = str(x["id"])
            picurl = x["mainPic"]
            picusername = x["nickName"]
            print("ID: " + picid)
            print("ImageURL: " + picurl)
            print("Username: " + picusername)
            filename = DOWNLOADS_DIR + picid + ".jpg"
            if picid not in lines:
                print("file " + picid + " doesnt exists! Downloading...")
                download_pic(picurl, filename)
                print("file " + picid + " fully downloaded!")
                print("file " + picid + " sending now nude!")
                send_nude(filename, picusername)
                print("file " + picid + " nude sent!")
                w = open('links.txt', 'a+')
                w.write(picid + "\r\n")
                w.close()
            else:  # not found
                print("file " + picid + " already exists")

    print("Done with downloading")
    print("\r\n Waiting now for 15minutes :-) \r\n")
    sleep_time=400
    timer=0
    while (timer != sleep_time):
        timer = timer + 100
        sleep(timer)
        print("\r\n " + str(sleep_time - timer) + " Seconds left :-)" + " \r\n")

    return print("im back fellas")

event_loop = asyncio.new_event_loop()
event_loop.create_task(looper(event_loop))
app.run()
