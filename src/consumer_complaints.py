#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys

def parseLine(line, records):
    """
    Input: One line (record) in a CSV file, one list that we want to append to
    Output: Void, the side-effect is that a line is parsed and added to records (a list of lists)
    
    This parses a line of the CSV without calling any functions outside of standard Python. The edge case we need to check for 
    is values in quotation marks. If one of our values is "Mark, the data engineer, says hi", this has to be parsed as one value 
    and we clearly cannot split at commas within the quotations. We handle this by essentially using ad-hoc parsing to look for 
    quotation mark. 
    
    Testing- check that all lists within records are the same length. Since the first length denotes column headers, ensure that
    they are all the same length as the first list in records.
    """
    fields = []                  # Holds the parsed CSV values for one line
    i = 0                        # "Pointer"
    buff = ""                    # Temporary string builder for holding parsed fields
    while i < len(line):
        # If the line begins with a quotation, then everything from this quotation mark to the next is one value
        if line[i] == '"':
            i += 1
            while i != len(line)and line[i] != '"':
                buff += line[i]
                i += 1
            i += 1
        else:
            # If not, the value we extract either goes until the next comma, or the end of the line
            while i != len(line) and line[i] != ',':
                buff += line[i]
                i += 1
        fields.append(buff)
        buff = ""
        i += 1
    records.append(fields)


def getOutputList(records):
    """
    Input: Dictionary where Key = Tuple<String,String>, Value = Dictionary of <String,Int>
    Output: Sorted list of strings in the expected format

    Takes the output of parseLine(), which is a nested dictionary. The key will be a tuple denoting complaint type and year,
    and the value will itself be a dictionary where key is the company name, and value is the number of complaints.

    For each <ComplaintType,Year> calculates the total number of complaints , the max number of complaints that one single company 
    incurred, and the ratio of total complaints that the max represents (rounded up), expressed as a whole number percentage.
    """
    outputList = []
    line = ""
    for k, v in records.items():
        if ',' in k[0]:
            line += '"' + k[0].lower() + '",' + k[1] + ","
        else:
            line += k[0].lower() + "," + k[1] + ","
        totalComplaints = 0
        maxComplaints = 0
        companyCounter = 0
        for i in v.values():
            totalComplaints += i
            if i > maxComplaints:
                maxComplaints = i
            companyCounter += 1    
        # Calculate the ratio of maxComplaints to totalComplaints 
        # This denotes the highest number of complaints against one company
        ratio = maxComplaints/totalComplaints
        ratio *= 100
        ratio = round(ratio)
        ratio = int(ratio)
        complaintsAgainstMax = ratio
        line += str(totalComplaints) + "," + str(companyCounter) + "," + str(complaintsAgainstMax)
        outputList.append(line)
        line = ""
    return sorted(outputList)


def getYear(dateField):
    """
    Input: String representing date 
    Output: Extracted year from date

    We assume that the date has a format such that the year is the first 4 characters
    """
    return dateField[0:4]


def main(inputFile, outputFile):

    tupes = []

    try:
        f = open(inputFile, 'r', encoding="latin-1")
        contents = f.read()
        # Hold lines split by n in tupes
        for i in contents.split('\n'):
            tupes.append(i)
    except:
        print("Error: Cannot open input file. Exiting.")
        exit(1)

    # List for holding parsed tupes
    myRecords = []
    for i in tupes:
        parseLine(i, myRecords)
  
    # Data validation
    # If there were any stray newline tokens in the file, they'll produce an empty list here, so we remove them. The list comp filters these out.
    # Or, if any record did not consist of 18 comma-deliminated fields, remove it
    myRecords = filter(None, myRecords)
    myRecords = [x for x in myRecords if len(x) == 18]

    # Use a dictionary to hold indices of fields
    schemaIndices = {}
    index = 0
    for i in myRecords[0]:
        schemaIndices[i] = index
        index += 1

    # This will get us the correct indices to look in for any particular tuple
    # Note that by doing this, we need our columns to have these titles, but the columns can be in any order    
    try:
        productInd = schemaIndices["Product"]
        dateIndex = schemaIndices["Date received"]
        companyIndex = schemaIndices["Company"]    
    except:
        print("Error: The input file does not have proper column headers. Exiting.")
        exit(1)

    # Key is tuple<Product, Year>, Value is a Dictionary of <Company Name, # of Complaints>
    companyComplaintsDict = {}

    for i in myRecords[1:len(myRecords)]:
        keyPair = ( i[productInd], getYear(i[dateIndex]) )
        if keyPair not in companyComplaintsDict:
            companyComplaintsDict [keyPair] = {}
        companyName = i[companyIndex].lower()
        if companyName not in companyComplaintsDict[keyPair]:
            companyComplaintsDict[keyPair][companyName] = 1
        else:
            companyComplaintsDict[keyPair][companyName] += 1

    myOutputList = getOutputList(companyComplaintsDict)

    f = open(outputFile, 'w')

    for i in myOutputList:
        f.write(i + '\n')    

    print("Completed successfully")

    exit(1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
