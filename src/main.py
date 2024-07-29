from textnode import TextNode

import os
import shutil


def main():
    setup()

def recursive_copy(dir, destination):
    if dir == None or dir == "":
        raise Exception("dir is empty or None")
    
    if os.path.exists(dir):
        contents = os.listdir
        

def setup():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

    print(os.path.isfile("static"))
main()