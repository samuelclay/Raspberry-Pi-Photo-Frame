#!/usr/bin/env python

import flickrapi
import requests

FLICKR_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
USER_ID = "25704617@N04"

def make_url(photo):
    # url_template = "http://farm{farm-id}.staticflickr.com/
    #                 {server-id}/{id}_{secret}_[mstzb].jpg"
    photo['filename'] = "%(id)s_%(secret)s_z.jpg" % photo
    url = ("http://farm%(farm)s.staticflickr.com/%(server)s/%(filename)s" 
           % photo)
    return url, photo['filename']

def main():
    print " ---> Requesting photos..."
    flickr = flickrapi.FlickrAPI(FLICKR_KEY)
    photos = flickr.walk(user_id=USER_ID)
    for photo in photos:
        url, filename = make_url(photo.__dict__['attrib'])
        path = '/home/pi/photoframe/flickr/%s' % filename
        try:
            image_file = open(path)
            print " ---> Already have %s" % url
        except IOError:
            print " ---> Downloading %s" % url
            r = requests.get(url)      
            image_file = open(path, 'w')
            image_file.write(r.content)
            image_file.close()

if __name__ == '__main__':
    main()
