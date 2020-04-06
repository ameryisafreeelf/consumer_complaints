Here are some test cases we can run. Just run the script from command line with the correct input/output directories, or modify run.sh. 

1. Simple 1 line test

Just the header and one CSV record. Should produce one line- very straightforward. 

2. No header test

This should just print an error message and exit gracefully. No output expected.

3.  Added spaces test

Threw in a bunch of spaces between the header and one record. Ensure that this is handled in the code. Should produce the same result as the first test.

4. Company names capitalized test

Ensure that different capitalizations of the same company name are treated the same. The output should indicate that only one company received complaints. 

5. Test 1

Insight's provided input. Make sure (1) the complain names are lowercase, (2) any strings that contain quotations show the quotations in the output, (3) the outputs are sorted by complaint type and year. 
 
