# Web-Crawler
In this project, the problem has two main parts :

1. Traversing through Bogazici University OBIKAS System and extracting the data related to all departmental courses within input.

2. Processing the data and store it in a way that enables us to create a table in the
desired format.

#### General Explanation of Algorithm:

We take the input and after encoding years and semesters we call the method construct_table. We follow this strategy:
For each departments do this separately:

1. For each semester given in the range of input do this:

    1.1. Go to the website and extract the html of it.
  
    1.2. Process the html by using find_headers and merge_white_grey methods and get the list of all lessons. 
  
    1.3. Process the list of all lessons and store the necessary information to create the table.
  
2. After storing all semesters’ data, process the data stored to print the table.
