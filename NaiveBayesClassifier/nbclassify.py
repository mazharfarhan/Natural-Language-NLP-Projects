import os
import math

rootdir = "."

spamWordDict = {}
hamWordDict = {}
# function for reading the model.txt file
def main():
    print ("Inside the nbclassify function")
    # Path to model.text file for reading model parameters.
    modelFilePath = os.path.join(rootdir,"nbmodel.txt")

    #fileObj for opening the model.txt file and reading line by line
    modelFileObj = open(modelFilePath,"r",encoding="latin1")
    hamFlag = 0
    spamFlag = 0

    for line in modelFileObj:
        if 'HamCount' in line:
            countHamFiles = int(line.split(':')[1].strip('\n'))

        elif 'SpamCount' in line:
            countSpamFiles = int(line.split(':')[1].strip('\n'))
            
        elif 'HamWordCnt' in line:
            CountWordsHam = int(line.split(':')[1].strip('\n'))

        elif 'SpamWordCnt' in line:
            CountWordsSpam = int(line.split(':')[1].strip('\n'))

        elif 'VocabularySize' in line:
            vocabularyCnt = int(line.split(':')[1].strip('\n'))

        elif 'Ham Word Count' in line:
            hamFlag = 1
            spamFlag = 0

        elif 'Spam Word Count' in line:
            spamFlag = 1
            hamFlag = 0

        elif hamFlag == 1 and spamFlag == 0:
            vals = line.split()
            vals[1] = vals[1].strip('\n')
            hamWordDict[vals[0]] = int(vals[1])

        elif hamFlag == 0 and spamFlag == 1:
            vals = line.split(' ')
            vals[1] = vals[1].strip('\n')
            spamWordDict[vals[0]] = int(vals[1])


    modelFileObj.close()
    testing(hamWordDict,spamWordDict,countHamFiles,countSpamFiles,CountWordsHam,CountWordsSpam,vocabularyCnt)

# function to compute the conditional probabiliity of a word given class
def condprobWord(wordCnt, totalCnt, vocabSize ):
    return math.log((wordCnt+1) / (totalCnt + vocabSize))

#Output write
def outputWrite(txt):
    outputfilepath = os.path.join(rootdir,"nboutput.txt")
    if os.path.isfile(outputfilepath):
        os.remove(outputfilepath)

    with open(outputfilepath,"w",encoding="latin1") as out:
         out.write(txt)

    out.close()

# function for testing the classifier on the development folder.
def testing(hamWordDict,spamWordDict,countHamFiles,countSpamFiles,CountWordsHam,CountWordsSpam,vocabularyCnt):
    # calculate the prior probability.
    totalCount = countSpamFiles + countHamFiles
    # priorSpam = math.log2(countSpamFiles) - math.log2(totalCount)
    # priorHam = math.log2(countHamFiles) -  math.log2(totalCount)
    priorSpam = countSpamFiles / totalCount
    priorHam = countHamFiles / totalCount

    output = ""
    classifiedHamFiles = 0
    classifiedSpamFiles = 0
    actualHamFiles = 0
    actualSpamFiles = 0
    correctClassifiedSpam = 0
    correctClassifiedHam = 0

    # Recursively get the txt files from the development data folder.
    testdatapath = os.path.join(rootdir,"dev1")
    for dir,subdir,files in os.walk(testdatapath):
        for file in files:
            # check if the name of the file is txt file
            if ".txt" in file:

                spamFileProb = math.log(priorSpam)
                hamFileProb = math.log(priorHam)


                #open the file and read the content line by line.
                # get the path of the file and open that file and read each token one by one.
                filepath = os.path.join(dir,file)

                with open(filepath, "r", encoding="latin1") as f:

                    for line in f:
                        words = line.split()


                        for word in words:

                            if word in spamWordDict:
                                wordCntSpam = spamWordDict[word]
                            else:
                                wordCntSpam = 0


                            if word in hamWordDict:
                                wordCntHam = hamWordDict[word]
                            else:
                                wordCntHam = 0

                            if word not in spamWordDict and word not in hamWordDict:
                                continue

                            spamFileProb += math.log((wordCntSpam + 1)/(CountWordsSpam + vocabularyCnt))
                            hamFileProb += math.log((wordCntHam + 1)/ (CountWordsHam + vocabularyCnt))


                # Number of files that were correctly classified and total number of files classified in each class
                if(hamFileProb > spamFileProb):

                    if "ham" in file:
                        correctClassifiedHam += 1
                    classifiedHamFiles += 1
                    output += "ham" + " " + filepath + "\n"

                elif(spamFileProb > hamFileProb):

                    if "spam" in file:
                        correctClassifiedSpam += 1
                    classifiedSpamFiles += 1
                    output += "spam" + " " + filepath + "\n"

                if "ham" in file:
                    actualHamFiles += 1
                elif "spam" in file:
                    actualSpamFiles += 1




    # calculate the precision , recall and f1 score
    precisionHam = correctClassifiedHam /  classifiedHamFiles
    precisionSpam = correctClassifiedSpam / classifiedSpamFiles

    recallHam = correctClassifiedHam / actualHamFiles
    recallSpam = correctClassifiedSpam /actualSpamFiles

    f1scoreHam =  (2* precisionHam *recallHam) / (precisionHam + recallHam)
    f1scoreSpam = (2 * precisionSpam *recallSpam)/ (precisionSpam + recallSpam)


    print ("precision Ham:",precisionHam, " precision Spam:",precisionSpam)
    print ("recall Ham:",recallHam," recall Spam:", recallSpam)
    print ("f1 Ham:",f1scoreHam," f1 Spam:", f1scoreSpam)


    outputWrite(output)

main()
