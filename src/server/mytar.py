#! /usr/bin/env python3

import os
from sys import argv, exit, stdout

debug = False
debugGif = False

def getfileName(fileName):
    fileNameEncoded = fileName.encode()
    return fileNameEncoded

def getContent(fdInput):
    fileContents = os.read(fdInput, os.fstat(fdInput).st_size)
    ###Test###
    if debugGif:
        outFile = os.open('outputtest/test.gif', os.O_CREAT | os.O_WRONLY)
        print('file contents is of type ' + str(type(fileContents)))
        byteArrayCont = bytearray(fileContents)
        print('file contents is of type ' + str(type(byteArrayCont)))
        os.write(outFile,byteArrayCont)
    #########
    return fileContents
# 
# def makeMyTarName(fileName):
#     parts = fileName.split('.')
#     return parts[0]

# Will use -| as the end of line data line
def frame(fdInput, fileName):
    fileNameEncoded = getfileName(fileName)
    fileContents = getContent(fdInput)
    
    if debug: print("The size of the file name " + str(fileNameEncoded))
    
    newByte = fileNameEncoded + '-|'.encode() + fileContents + '-|'.encode()
    if debug: print(newByte)
    
    return newByte

def createMyTar(newByte):
    #outFile = os.open(1, os.O_CREAT | os.O_WRONLY)
    os.write(1,newByte)
    os.close(1)

def framer(argv):
    newByte = ''.encode()
    for fileName in argv:
        inputFile = os.open(fileName, os.O_RDONLY)
        newByte = newByte + frame(inputFile, fileName)
    
    #createMyTar(newByte)
    return newByte

def puller(fileContents):
    filePart = []
    tempByte = bytearray()
    skip = False
    for i, byte in enumerate(fileContents):
        if i < len(fileContents)-1:
            nextByte = fileContents[i + 1]
            if byte == ord('-') and nextByte == ord('|'):
                filePart.append(tempByte)
                tempByte = bytearray()
                skip = True
            if skip == False:
                tempByte.append(byte)
            if skip and byte == ord('|'):
                skip = False
    return filePart

def createFromMyTar(filePart):
    for index, tarPart in enumerate(filePart):
        if index == 0 or index % 2 == 0:
            #Changed this for test purpose
            outFile = os.open('test-output/'+tarPart.decode(), os.O_CREAT | os.O_WRONLY)
        else:
            os.write(outFile,bytes(tarPart))
            os.close(outFile)

def deFramer():
    fileContents = os.read(0, os.fstat(0).st_size)
    filePart = puller(fileContents)
                
    if debug:
        print(filePart)
        print('file name: ' + filePart[0].decode())
    
    createFromMyTar(filePart)

#Commenting out so the import doesn't look for these checks
# # if len(argv) < 2:
# #     #print("Not a valid amount of inputs")
# #     exit

# if argv[1] == 'c':
#     argv.remove(argv[0])
#     argv.remove(argv[0])
#     #print("Creating a new .mytar file from given files")
#     framer(argv)
#     exit

# elif argv[1] == 'x':
#     #print('Extracting the files from the given .mytar file')
#     deFramer()

# else:
#     print("Not a function of mytar")
#     exit