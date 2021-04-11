import re
import plistlib
import yaml
import os, sys
import cv2
import argparse

def divide(value):
    return "{" + str(round(int(re.search("(?<={)(.*)(?=})",value).group(1).split(',')[0])/2)) +"," +str(round(int(re.search("(?<={)(.*)(?=})",value).group(1).split(',')[1])/2)) + "}"

def divideFloat(value):
    return "{" + str((float(re.search("(?<={)(.*)(?=})",value).group(1).split(',')[0])/2)) +"," +str((float(re.search("(?<={)(.*)(?=})",value).group(1).split(',')[1])/2)) + "}"

input_file = ""

parser = argparse.ArgumentParser(description='Foo')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input', help='Input file name', required=True)
requiredNamed.add_argument('-o', '--output', help='Output file name', required=True)


args = parser.parse_args()

print(args.__dict__["input"])

fileI = args.__dict__["input"]
fileO = args.__dict__["output"]

filenameInput, file_extensionInput = os.path.splitext(fileI)
filenameOutput, file_extensionOutput = os.path.splitext(fileO)

if file_extensionInput == ".plist":
    try:
        with open(fileI, 'rb') as f:
            plist_data = plistlib.load(f)
    except IndexError:
            plist_file = '<stdin>'
            plist_data = plistlib.loads(sys.stdin.buffer.read())
            exit()

    dictionary = plist_data.get("frames").items()
    for key in dictionary:
        try:
            value = key[1]["textureRect"]
            key[1]["textureRect"] = "{{" + str(round(int(re.search("(?<={{)(.*)(?=},)",value).group(1).split(',')[0])/2)) + "," + str(round(int(re.search("(?<={{)(.*)(?=},)",value).group(1).split(',')[1])/2)) +"},{" + str(round(int(re.search("(?<=,{)(.*)(?=}})",value).group(1).split(',')[0])/2)) + "," + str(round(int(re.search("(?<=,{)(.*)(?=}})",value).group(1).split(',')[1])/2)) + "}}"
            if  key[1]["spriteOffset"] != '' :
                key[1]["spriteOffset"] = divideFloat(key[1]["spriteOffset"])
            if  key[1]["spriteSize"] != '':
                key[1]["spriteSize"] = divide(key[1]["spriteSize"])
            if  key[1]["spriteSourceSize"] != '':
                key[1]["spriteSourceSize"] = divide(key[1]["spriteSourceSize"])
        except Exception as e:
            print(e)
            print(key)

    plist_data["metadata"]["size"] = divide(plist_data["metadata"]["size"])
    plist_data["metadata"]["realTextureFileName"] = plist_data["metadata"]["realTextureFileName"].replace("uhd","hd")
    plist_data["metadata"]["textureFileName"] = plist_data["metadata"]["textureFileName"].replace("uhd","hd")


    f = open(fileO, 'wb')

    plistlib.dump(plist_data,f)



    im = cv2.imread(filenameInput+".png",cv2.IMREAD_UNCHANGED)

    width = int(im.shape[1] / 2 )
    height = int(im.shape[0] / 2 )
    dim = (width, height)
    resized = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite(filenameOutput + ".png",resized)
else:
    print("Invalid file")