from PIL import Image
import sys
import os
from contextlib import closing
raw_file=sys.argv[1]
message=sys.argv[2]
msg_size=os.path.getsize(message)
img=Image.open(raw_file)
width,height=img.size
new_img=img.load()
if(msg_size*8>width*height*3):
    print('message is too big for this image')
    exit(0)

_ord=ord
def ord(i):
    if i=='':
        return 0
    return _ord(i)

class Msg():
    def __init__(self,path):
        self.file=open(path,'rb')
        self.bit=0
        self.now=bin(ord(self.file.read(1)))[2:].rjust(8,'0')
    def close(self):
        self.file.close()
    def get_binary(self):
        if(self.bit==8):
            self.now=bin(ord(self.file.read(1)))[2:].rjust(8,'0')
            self.bit=0
        self.bit+=1
        return int(self.now[self.bit-1])

def set_lsb(raw,msg):
    if msg==0:
        return raw&0xff-1
    else:
        return raw|1

with closing(Msg(message)) as m:
    for j in xrange(height):
        for i in xrange(width):
            if(i%200==0):
                print "%8d,%8d"%(i,j)
            r,g,b,a=new_img[i,j]
            r=set_lsb(r,m.get_binary())
            g=set_lsb(g,m.get_binary())
            b=set_lsb(b,m.get_binary())
            new_img[i,j]=r,g,b,a

img.save('new.png')