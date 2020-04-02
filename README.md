# Consumer Complaints


## Summary
This is my solution for Insight's Data Engineering coding challenge, "Consumer Complaints". 

We are given a CSV input file, where each record represents a complaint filed against a company regarding some financial product. This data comes from the Consumer Financial Protection Bureau. Our goal is to output, for each financial product and year, the total number of complaints, the number of companies receiving a complaint, and the highest percentage of complaints directed at a single company. Our output format should be a csv listing these aggregate measures, and the output is sorted by financial product name and year.


## Running
This solution requires Python 3.7+.  

Please execute __run.sh__ from the command line. You can modify this script by changing the input and output directories in order to use different input files. There are sample test cases in the "insight_testsuite" folder- you can send output to the "output" folder in each test case's directory. 


Solution currently passes Insight's repo test.

## Known Issues
An example file provided by Insight contains more than 2.5 million lines of text. This is described as "modest-sized" by Insight, so I assume that the code should be able to handle files of this size regularly. While parsing the file seems to work as expected, it takes in excess of 20 minutes on one machine. In addition to the long run time, a sufficiently large input may cause us to run out of memory. 

Using some parallel processing framework to extend our task to multiple machines can scale this solution by providing more memory and compute power.


## Contact
Amery Chang at ac3241@nyu.edu
