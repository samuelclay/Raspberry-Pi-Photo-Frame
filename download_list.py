/usr/bin/env python

import os
import flickrapi
import requests
import psutil

FLICKR_KEY = "**************"
USER_ID = "**************"
restart = 'tmp'
pid = 'tmp'
flickrList = []
dirList = []

def make_url(photo):
    photo['filename'] = "%(id)s_%(secret)s_z.jpg" % photo
    url = ("http://farm%(farm)s.staticflickr.com/%(server)s/%(filename)s"
          % photo)
    return url, photo['filename']

def dir_list():
    global dirList
    dir = '/home/pi/photoframe/flickr/'
    files = os.listdir(dir)
    for file in files:
        if file.endswith(".jpg"):
           dirList.append(file)

def download_files():
    #print " ---> Requesting photos..."
    flickr = flickrapi.FlickrAPI(FLICKR_KEY)
    photos = flickr.walk_set('**************')
    global flickrList
    for photo in photos:
        url, filename = make_url(photo.__dict__['attrib'])
        path = '/home/pi/photoframe/flickr/%s' % filename
        flickrList.append(filename)
        try:
            image_file = open(path)
            #print " ---> Already Have %s" % url
        except IOError:
            #print " ---> Downloading %s" % url
            r = requests.get(url)
            image_file = open(path, 'w')
            image_file.write(r.content)
            image_file.close()
            global restart
            restart = 'restart'

def compare_list():
    global dirList
    global flickrList
    global restart
    a = []
    a = list(set(dirList) - set(flickrList))
    dir = "/home/pi/photoframe/flickr"
    files = os.listdir(dir)
    for file in a:
        if file.endswith(".jpg"):
           os.remove(os.path.join(dir,file))
           restart = 'restart'

def restart_slideshow():
    if (restart == 'restart'):
       PROCNAME = "fbi"
       global pid
       for proc in psutil.process_iter():
           if proc.name == PROCNAME:
              pid = proc.pid
       pidPath = "/proc/" + str(pid)
       if (os.path.exists(pidPath)):
          cmdKill = "pkill fbi"
          cmd = "fbi -T 1 -noverbose -m 640x480 -a -u -t 6 /home/pi/photoframe/flickr/**"
          os.system(cmdKill)
          os.system(cmd)

if __name__ == "__main__":
 dir_list()
 download_files()
 compare_list()
 restart_slideshow()
