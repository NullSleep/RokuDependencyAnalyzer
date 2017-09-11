import os
import json

location = '/Users/carlosarenas/Dropbox/Work/Zemoga/Projects/Roku/Hulu/cube-roku'
xmlfiles = [] #list to store all XML files found at location
parentNode = "BasePage"
basePageFiles = []
listScriptFunctions = []

def findChildNodes():
    counter = 0 #keep a count of all files found
    numberBasePageFiles = 0
    stringToFind = "extends=\"" + parentNode + "\""

    #Navigate through all the folders and files for a given location
    for root, dirs, files in os.walk(location, topdown=False):
        #Navigate through all the directories
        for name in dirs:
            directoryName = (os.path.join(root, name))
            # print "DIR: " + dirN
            #Navigate through all the files in a given directory
            for file in os.listdir(directoryName):
                try:
                    #Look for all the XML files
                    if file.endswith(".xml"):
                        xmlfiles.append(str(file))
                        counter = counter + 1
                        # print "XML file found:\t", file
                        filePath = '/'.join([directoryName, file])
                        #Open the file and look to see if it extends from BasePage
                        lines = [line.rstrip('\n') for line in open(filePath)]
                        if any(stringToFind in s for s in lines):
                            basePageFiles.append(filePath)
                            numberBasePageFiles += 1
                            # print str(file) + " extends from " + parentNode
                except Exception as e:
                    raise e
                    print "No files found here!"

    print "\nNumber of XML files found:\t", counter
    # print "((((((( XML FILES )))))))"
    # print xmlfiles
    print "\nNumber files that inherit from BasePage:\t", numberBasePageFiles
    # print "\nFiles that inherit from BasePage:"
    # print basePageFiles

def dependenciesForParentNode():
    #Dependencies used in the parent node
    paretnNodeLocation = location + '/components/base/BasePage.xml'
    fileContent = [line.rstrip('\n') for line in open(paretnNodeLocation)]
    scripts = [s for s in fileContent if "<script type=\"text/brightscript\" uri=" in s]
    #Go through all the different scripts and look for all the different fuctions in such file
    scriptUri = "pkg:"
    scriptExtension = ".brs"
    for script in scripts:
        startScript = script.find(scriptUri)
        endScript = script.find(scriptExtension)
        scriptName = script[startScript + len(scriptUri) : endScript + len(scriptExtension)]
        scriptToAnalize = location + scriptName
        # print "SCRIPT TO ANALYZE: " + scriptToAnalize
        scriptContent = [line.rstrip('\n') for line in open(scriptToAnalize)]
        # print "-------------------------- CURRENT SCRIPT: " + scriptName + " --------------------------"

        #Loop throug all the functions
        functions = [s for s in scriptContent if "function " in s.lower()]
        functionList = []
        for function in functions:
            function = cleanString(function)
            if function[:8] == "function":
                startFuction = function.find("function")
                endFuction = function.find("(")
                functionName = function[startFuction + 8 : endFuction]
                # print functionName
                functionList.append(str(functionName))

        #Loop throug all the subroutines
        subroutines = [s for s in scriptContent if "sub " in s.lower()]
        subList = []
        for sub in subroutines:
            sub = cleanString(sub)
            if sub[:3] == "sub":
                startSub = sub.find("sub")
                endSub = sub.find("(")
                subName = sub[startSub + 3 : endSub]
                # print subName
                subList.append(str(subName))

        scriptsFunction = {}
        scriptsFunction['script_name:'] = scriptName
        scriptsFunction['script_functions:'] = functionList
        scriptsFunction['script_subs:'] = subList
        listScriptFunctions.append(scriptsFunction)

        # print "---------------------------------------------------------"
        # print scriptsFunctions
        print json.dumps(listScriptFunctions)

def functionsUsedByChildren():
    for script in basePageFiles:
        lines = [line.rstrip('\n') for line in open(script)]
        for line in lines:
            print line
            # for functions in listScriptFunctions:
            #     print fuctions


def cleanString(stringToClean):
    stringToClean = stringToClean.strip()
    stringToClean = stringToClean.lstrip()
    stringToClean = stringToClean.rstrip()
    stringToClean = stringToClean.replace(" ", "")
    stringToClean = stringToClean.lower()
    return stringToClean

findChildNodes()
dependenciesForParentNode()
functionsUsedByChildren()
