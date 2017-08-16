import os #os module imported here

location = '/Users/carlosarenas/Dropbox/Work/Zemoga/Projects/Roku/Hulu/cube-roku'
counter = 0 #keep a count of all files found
xmlfiles = [] #list to store all XML files found at location
parentNode = "BasePage"
stringToFind = "extends=\"" + parentNode + "\""
basePageFiles = []
numberBasePageFiles = 0

def findChildNodes():
    global location
    global counter
    global xmlfiles
    global parentNode
    global stringToFind
    global basePageFiles
    global numberBasePageFiles

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
                            basePageFiles.append(str(file))
                            numberBasePageFiles += 1
                            print str(file) + " extends from " + parentNode
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
    global location
    #Dependencies used in the parent node
    paretnNodeLocation = '/Users/carlosarenas/Dropbox/Work/Zemoga/Projects/Roku/Hulu/cube-roku/components/base/BasePage.xml'
    fileContent = [line.rstrip('\n') for line in open(paretnNodeLocation)]
    scripts = [s for s in fileContent if "<script type=\"text/brightscript\" uri=" in s]
    #Go through all the different scripts and look for all the different fuctions in such file
    for script in scripts:
        startScript = script.find("pkg:")
        endScript = script.find(".brs")
        scriptToAnalize = location + script[startScript+4:endScript+4]
        # print "SCRIPT TO ANALYZE: " + scriptToAnalize
        scriptContent = [line.rstrip('\n') for line in open(scriptToAnalize)]
        functions = [s for s in scriptContent if "function " in s.lower()]
        print functions


# findChildNodes()
dependenciesForParentNode()
