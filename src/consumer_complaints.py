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
            while i != len(line) - 1 and line[i] != '"':
                buff += line[i]
                i += 1
            i += 1
        else:
        # If not, the value we extract either goes until the next comma, or the end of the line
            while i != len(line) - 1 and line[i] != ',':
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
        for i in v.values():
            totalComplaints += i
            if i > maxComplaints:
                maxComplaints = i
        # Calculate the ratio of maxComplaints to totalComplaints 
        # This denotes the highest number of complaints against one company
        ratio = maxComplaints/totalComplaints
        ratio *= 100
        if not ratio.is_integer():
            ratio += 1
        ratio = int(ratio)
        complaintsAgainstMax = ratio
        line += str(totalComplaints) + "," + str(maxComplaints) + "," + str(complaintsAgainstMax)
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

    print(outputFile)

    try:
        f = open(inputFile,'r', encoding="latin-1")
    except:
        print("Error opening inputFile, exiting...")
        # exit(1)
    contents = f.read()
    
    # List of tuples for holding contents, split at new line
    tupes = []
    for i in contents.split('\n'):
        tupes.append(i)
    
    # List for holding parsed tupes
    myRecords = []
    for i in tupes:
        parseLine(i, myRecords)

    # Use a dictionary to hold indices of fields
    schemaIndices = {}
    index = 0
    for i in myRecords[0]:
        schemaIndices[i] = index
        index += 1

    # This will get us the correct indices to look in for any particular tuple
    # Note that by doing this, we need our columns to have these titles, but the columns can be in any order    
    productInd = schemaIndices["Product"]
    dateIndex = schemaIndices["Date received"]
    companyIndex = schemaIndices["Company"]    

    # Key is tuple<Product, Year>, Value is a Dictionary of <Company Name, # of Complaints>
    companyComplaintsDict = {}

    for i in myRecords[1:len(myRecords)]:
        keyPair = ( i[productInd], getYear(i[dateIndex]) )
        if keyPair not in companyComplaintsDict:
            companyComplaintsDict [keyPair] = {}
        companyName = i[companyIndex]
        if companyName not in companyComplaintsDict [keyPair]:
            companyComplaintsDict [keyPair][companyName] = 1
        else:
            companyComplaintsDict [keyPair][companyName] += 1

    myOutputList = getOutputList(companyComplaintsDict)

    f = open(outputFile, 'a+')

    for i in myOutputList:
        f.write(i + '\n')    

    # exit(1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])