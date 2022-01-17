from __future__ import print_function
import json
import requests
import cv2
import PIL
from PIL import Image
import binascii
import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import os.path

wallString = open("update.json", "r")
wall = json.loads(wallString.read())

NUM_CLUSTERS = 5




i = 1
output = []
print(len(wall))
for x in wall:
    print(i)
    i=i+1

    #Getting the image
    response = requests.get(x['url'])

    #Get file extension
    extension = os.path.splitext(x['url'])[1]
    print(extension)
    if extension=='':
        extension='.jpg'
    FILENAME = 'sample_image' + extension
    print(FILENAME)

    try:
        #Saving the image
        file = open(FILENAME, "wb")
        file.write(response.content)
        file.close()

        # loading the image
        img = PIL.Image.open(FILENAME)

        # fetching the dimensions
        wid, hgt = img.size

        # displaying the dimensions
        x['resolution'] = str(wid) + " x " + str(hgt)
        img.close()
        print(x['resolution'])

        #Converting all fileformat to jpg
        img = cv2.imread(FILENAME)
        cv2.imwrite('sample_image.jpg', img)

        im = Image.open('sample_image.jpg')
        im = im.resize((300, 300))      # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        print(type(shape))
        print("TEST\n\n\n")
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

        print('finding clusters')
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        print('cluster centres:\n', codes)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences

        index_max = np.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        print('most frequent is %s (#%s)' % (peak, colour))
        x['dominantColor'] = '#' + colour
    except:
        print("Failed to do it. Continuing with the next")
    output.append(x)
    print(len(output))
    

og = open("MadWallz.json", 'r')
orig = json.loads(og.read())
o = output + orig
og.close()
print(len(orig))
print(len(output))
print(len(o))


og = open("MadWallz.json", 'w')
og.write(json.dumps(o))
og.close()
