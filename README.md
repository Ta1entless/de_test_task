# ABOUT TASK 2 AND 3

In tasks 2 and 3, we engaged with the REST Countries API to obtain comprehensive information about various countries. After thorough research, we selected an API method that utilizes the
```
all?fields
```
 filter. This choice enabled us to validate all necessary fields at the stage of retrieving JSON data, thereby optimizing memory usage by only fetching relevant data.

### TASK 2

We parsed the JSON data and exported it to a CSV file. By opening the file in "write" mode, we processed and wrote each record line by line, ensuring the data was structured for easy analysis.

### TASK 3

Using a Docker Compose setup, we connected to a PostgreSQL database and performed next steps:

1. Table Setup: Defined a schema matching the API data structure.
2. Data Insertion: Inserted records into the database, using arrays for languages and ensuring updates via the ON CONFLICT clause.
3. SQL Queries: Executed queries to validate data insertion and analyze results, such as population sums and language distributions.