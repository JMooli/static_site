from textnode import TextNode

import os
import shutil
from utils import *


def main():
    setup()

def recursive_copy(source, destination):
    if source == None or source == "":
        raise Exception("source is empty or None")
    
    if os.path.exists(source):
        contents = os.listdir(source)

        for file in contents:
            source_and_file = os.path.join(source, file)
            destination_and_file = os.path.join(destination, file)
            if os.path.isfile(source_and_file):
                shutil.copy(source_and_file, destination_and_file)
            else:
                os.mkdir(destination_and_file)
                recursive_copy(source_and_file, destination_and_file)
        
 
def setup():

    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    
    recursive_copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()