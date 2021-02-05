# web-search-engine
Search engine that maintains an inverted index of webpages and allows users to query ranked results.

To run the program: 
~~~
python main.py
~~~

Change variables *path* and *pathToWebpages* as necessary.

**MySQLdb Instructions**
1. Download and install MySQL Server (and MySQL Shell which might already come with the server, not sure). Run the MySQL Shell application.
2. Change to SQL mode:
~~~
\sql
~~~
3. Set up a password
~~~
\connect root@localhost
~~~
4. Create a database
~~~
CREATE DATABASE inverted_index;
~~~
5. Confirm the database has been created
~~~
show databases;
~~~
6. 
~~~
use inverted_index;
~~~
