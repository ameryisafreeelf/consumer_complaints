# Running

Please run this script using <run.sh>. You can modify this by changing the input and output directories in order to pass in different CSV files.

# Approach

We essentially need to do 2 things:

(Please note that we are instructed not to use libraries outside of standard Python.)

1. Parse the CSV file properly

Parsing the file is pretty straightforward. The major issue we must deal with is that some fields in the CSV contain commas within quotation marks. For example, given one field containing the value "Hi, Insight, my name is Amery", this must be parsed as one value. Therefore, naively cutting the string at commas does not work.

We solve this by using an ad-hoc style of parsing. We generally denote fields in the CSV by commas, but whenever we run into a quotation mark, we do not consider any commas within the quotations to be a column delimiter, but instead keep parsing until we find another quotation mark. This ensures that fields containing quotation marks are parsed correctly.

The result of parsing is a list of lists, where each list denotes one parsed record. 

2. Move the data into appropriate data structures so that we can pull the aggregate measures we need

For each list, we create a dictionary where the key is a tuple of (Product, Year) and the value is a dictionary of {CompanyName : Number of Complaints}. This is quite intuitive; the keys of dictionaries have to be unique, and we want to return unique aggregate measures for each product and year (basically a GroupBy statement). By keeping counts of how many complaints are filed against each company for that product and year, it's trivial to track the total complaints and maximum complaints against one company by iterating through the dictionary.

Finally, we iterate through that dictionary we created to product correctly formatted output.