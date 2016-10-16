import os
import sys
import json

# Read the path of the data directory from command line
#rootdir = sys.argv[1]
rootdir = "."
vocalbulary = set()

def createDic(dir,folders,wordDict,classCount,wordCnt):
    Folder = os.path.join(dir,folders)
    #Recursively get the files from the ham directory and build a dictionary consisting of word counts.
    for Dir,SubDir,Files in os.walk(Folder):

                 for i, file in enumerate(Files):

                  if ".txt" in file:

                     classCount += 1
                     #open the file and read the contents of the file in a string
                     filePath = os.path.join(Dir,file)
                     with open(filePath,"r", encoding="latin1") as fileObj:
                        for line in fileObj:

                           line = line.strip('\n')

                           eachword = line.split()

                           for word in eachword:
                               vocalbulary.add(word)
                               if word not in wordDict:
                                   wordDict[word] = 1
                                   wordCnt += 1
                               else:
                                   wordDict[word] += 1
                                   wordCnt += 1

                     fileObj.close()
    return wordDict,classCount, wordCnt

def filewrite(hamCount,hamWordDict,spamCount,spamWordDict,hamWordCnt,spamWordCnt):

   # Name of the output file
   outputFile = os.path.join(rootdir,"nbmodel.txt")
   fileObj = open(outputFile, "w",encoding='latin1')
   fileObj.write("HamCount:")
   fileObj.write(str(hamCount))
   fileObj.write("\n")
   fileObj.write("HamWordCnt:")
   fileObj.write(str(hamWordCnt))
   fileObj.write("\n")
   fileObj.write("SpamCount:")
   fileObj.write(str(spamCount))
   fileObj.write("\n")
   fileObj.write("SpamWordCnt:")
   fileObj.write(str(spamWordCnt))
   fileObj.write("\n")
   fileObj.write("VocabularySize:")
   fileObj.write(str(len(vocalbulary)))
   fileObj.write("\n")
   fileObj.write("Ham Word Count")
   fileObj.write("\n")
   for key in hamWordDict:
       fileObj.write(key + " " + str(hamWordDict[key]) + "\n")


   fileObj.write("Spam Word Count")
   fileObj.write("\n")
   for key2 in spamWordDict:
        fileObj.write(key2 + " " + str(spamWordDict[key2]) + "\n")
   fileObj.close()

def main():

   #Get the path to the training data folder
   trainData = os.path.join(rootdir,"newtrain")
   hamWordDict =  {}
   spamWordDict = {}
   hamCount = 0
   spamCount = 0
   hamWordCount = 0
   spamWordCount = 0


   # Read the subdirectories recurssively from the training folder.
   for dir, subdir, files in os.walk(trainData):

           for folders in subdir:

              #Folders belonging to ham
              if folders == "ham":
                  hamWordDict,hamCount,hamWordCount = createDic(dir,folders,hamWordDict,hamCount,hamWordCount)
              elif folders == "spam":
                  spamWordDict,spamCount,spamWordCount = createDic(dir,folders,spamWordDict,spamCount,spamWordCount)

   #write the output to a output file.
   filewrite(hamCount,hamWordDict,spamCount,spamWordDict,hamWordCount,spamWordCount)

main()
