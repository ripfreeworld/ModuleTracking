# How to use this Module Tracking
>---------**JumpingJIVE**---------\
>Author: Chenyang Liu

## A Brief Introduction
 
 Aiming for collecting information of certain websites by [IVS](https://ivscc.gsfc.nasa.gov/program/index.html),
 which show the current usage and information respectively for
 HDD and antennas, there are 5 scripts in total. <br>
 
 **connect.py** is used to connect the PostgreSQL database. <br>
 This script is automatically called by antenna.py, record.py and report.py before accessing the database.
 
 **antenna.py** is for reading different antennas/stations into the TABLE `stations`.<br>
 This script is used to update the new antennas in use. 
 
 **record.py** is to read the current usage for each antenna and store new records into the TABLE `capacity`.<br>
 This script keeps running with a given gap between each loop, adding every new record into the database. 
 
 **report.py** filters the information and generates two html files, which shows the latest status of antenna 
 and the history of VSN, respectively. <br>
 
 **htmlGenerator.py** finally generate the reader-friendly result from report.py into html format.
 
 ### How to use
 The usage is simple. First enumerate all antennas into database by running **antenna.py**. With the given names of
 antenna, then you are able to keep **record.py** running. After having some data by recording, you could run the 
 **htmlGenerator.py** to have a view at selected information from two new generated `.html` files. The **connect.py**
 and **report.py** are called automatically, if the path during importing is clear.

##  Installation
Through installation you would have the all necessary packages installed in your system and the database with matching
roll and database. Afterwards you could run all scripts without problem.
### MacOS
>More information in
>[Getting Started with PostgreSQL on Mac OSX](
https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)
, [How to setup PostgreSQL on MacOS](https://www.robinwieruch.de/postgres-sql-macos-setup) and
[Getting Started with PostgreSQL](https://www.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)
1.  Get `Homebrew` installed:<br>
    Paste that in a macOS Terminal prompt:
    <pre>/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"</pre>
    For specific you could read from [Homebrew](https://brew.sh)

2.  Install Postgres:
    <pre>brew update
    brew install postgresql</pre>
    Then check your PostgreSQL version by typing:
    <pre>postgres --version</pre>
    
3.  Manually start and stop Postgres:
    <pre>pg_ctl -D /usr/local/var/postgres start
    pg_ctl -D /usr/local/var/postgres stop</pre>
    Or let Postgres start every time your computer starts up
    <pre>brew services start postgresql</pre>
    
4.  Create or remove the user:
    <pre>createuser user_name
    dropuser user_name</pre>
    Log in as superuser:
    <pre>psql postgres</pre>
    Then you may see `postgres=#` at the beginning of each new line. <br>

5.  Create or remove the database `jumpingjive`:
    <pre>createdb jumpingjive
    dropdb jumpingjive</pre>
    Since the Camel Case is not always meaningful in database, I just use these names in small case at the
    very beginning, i.e. jumpingjive rather than JumpingJIVE to avoid unnecessary mistakes.

6.  Modify the database: <br>
    Log in `jumpingjive` by typing:
    <pre>psql jumpingjive</pre>
    Set a password:
    <pre>jumpingjive=# \password</pre>
    The password might not be asked because it is set to "trust" for local connections.
    
7.  View all users:
    <pre>postgres=# \du</pre>
    View the list of Database:
    <pre>postgres=# \list</pre>
    Connect the user with database `jumpingjive`:
    <pre>postgres=# GRANT ALL PRIVILEGES ON DATABASE jumpingjive to user_name</pre>
    
8.  At last, you could try to run the python script `connect.py` to see if it shows the result `Connected...`
### Ubuntu
>More information in
>[Getting Started with PostgreSQL](https://www.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)
1. 


## Installing packages
 
For capturing and filtering the data from desired websites, several packages for Python are needed. 

### Beautiful Soup
>More information in [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

On Debian or Ubuntu Linux, you can install Beautiful Soup with the system package manager:

<pre>apt-get install python-bs4 </pre> or for python3:
<pre>apt-get install python3-bs4 </pre> 

Beautiful Soup 4 is published through PyPi, so if you can’t install it with the system packager, 
you can install it with `easy_install` **or** `pip`. <br>
The package name is beautifulsoup4, and the same package works on Python 2 and Python 3. 
(pip3 and easy_install3 respectively for Python 3).

<pre>easy_install beautifulsoup4
pip install beautifulsoup4 </pre> 

### Yattag
> More information in [Download and install yattag](https://www.yattag.org/download-install)

Use pip to install yattag:

<pre>pip install yattag</pre>

Or `pip-python3` instead of `pip` for Python 3 environment.
