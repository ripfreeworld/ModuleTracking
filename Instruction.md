# How to use this Module Tracking
>---------**JumpingJIVE**---------\
>Author: Chenyang Liu<br>
>Date: 2019.12.12
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

2.  Install PostgresSQL:
    <pre>$ brew update
    $ brew install postgresql</pre>
    Then check your PostgreSQL version by typing:
    <pre>$ postgres --version</pre>
    
3.  Manually start and stop Postgres:
    <pre>$ pg_ctl -D /usr/local/var/postgres start
    $ pg_ctl -D /usr/local/var/postgres stop</pre>
    Or let Postgres start every time your computer starts up
    <pre>$ brew services start postgresql</pre>
    
4.  Create or remove the user:
    <pre>$ createuser user_name
    $ dropuser user_name</pre>
    Log in as superuser:
    <pre>$ psql postgres</pre>
    Then you may see `postgres=#` at the beginning of each new line. <br>

5.  Create or remove the database `jumpingjive`:
    <pre>$ createdb jumpingjive
    $ dropdb jumpingjive</pre>
    Since the Camel Case is not always meaningful in database, I just use these names in small case at the
    very beginning, i.e. jumpingjive rather than JumpingJIVE to avoid unnecessary mistakes.

6.  Modify the database: <br>
    Log in `jumpingjive` by typing:
    <pre>$ psql jumpingjive</pre>
    Set a password:
    <pre>jumpingjive=# \password</pre>
    The password might not be asked because it is set to "trust" for local connections.
    
7.  View all users:
    <pre>postgres=# \du</pre>
    View the list of Database:
    <pre>postgres=# \list</pre>
    Connect the user with database `jumpingjive`:
    <pre>postgres=# GRANT ALL PRIVILEGES ON DATABASE jumpingjive to user_name</pre>
    

### Ubuntu
>More information in
>[Getting Started with PostgreSQL](https://www.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)
1.  Refresh the apt-get repository and install PostgreSQL:
    <pre>$ sudo apt-get update
    $ sudo apt-get install postgresql postgresql-contrib</pre>
    Then check your PostgreSQL information by typing:
    <pre>$ dpkg --status postgresql</pre>

2.  Manually start and stop Postgres:<br>
    The postgresql service is started automatically upon startup. But you
    could also do the following:
    <pre>
    $ sudo service postgresql stop     // Stop the service
    $ sudo service postgresql start    // Start the service
    $ sudo service postgresql restart  // Stop and restart the service
    $ sudo service postgresql reload   // Reload the configuration without stopping the service
    </pre>

3.  Login as SUPERUSER:<br>
    The PostgreSQL installation creates a "UNIX USER" called `postgres`, who is also the "Default PostgreSQL's SUPERUSER". <br>
    You could try as following:
    <pre>$ sudo -u postgres -i
        $ psql
        ...
        $ \q        //quit
    $ exit</pre>
    Or
    <pre>$ sudo -u postgres psql
    $ \q</pre>
    And set a password for the default `postgres`
    <pre>postgres=# \password
    ......

    postgres=# \q</pre>

4.  Change the `pg_hba.conf`:<br>
    Tailor the PostgreSQL configuration file `/etc/postgresql/10/main/pg_hba.conf`(`10` according to your PostgreSQL version) to allow non-default user to login to PostgreSQL Server, by adding the following entry:
    <pre>local   testdb      testuser                     md5</pre>
    If you still meet the error later with: `psql: FATAL: Peer authenitication failed for user ...`, the reason might be that you are only allowed to access the local database with default identity, namely `peer` instead of `md5`. You might find solutions from [stackoverflow - psql: FATAL: Peer authenitication failed](https://stackoverflow.com/questions/17443379/psql-fatal-peer-authentication-failed-for-user-dev)

4.  Create another user with a password for login:<br>
    
    <pre>$ sudo -u postgres createuser --login --pwprompt user_name</pre>
    Without the flag `-u postgres` would lead to the following ERROR:
    <pre>createuser: creation of new role failed: ERROR:  permission denied to create role</pre>
    Besides setting the password for new role, the password for `postgres` will also be asked.

5.  Create a new database called `jumpingjive`, owned by `user_name`.
    <pre>$ sudo -u postgres createdb --owner=user_name jumpingjive</pre>

6.  Restart PostgreSQL server and login:
    <pre>$ sudo service postgresql restart
    $ psql -U user_name jumpingjive</pre>



* Important is, the `database`, `user` and `password` must match with the script `connect.py`. And the `port` is default `5432`. <br>
At last, you could run the python script `connect.py` to see if it shows the result `Connected...`
## Installing packages
 
For capturing and filtering the data from desired websites, several packages for Python are needed. You could install either with the system packager `apt-get` or `pip`.

### psycopg2
> More information in [psycopg2](https://pypi.org/project/psycopg2/)
<pre>$ apt-get install python3-psycopg2</pre>

### Beautiful Soup
>More information in [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

<pre>$ apt-get install python3-bs4 </pre>

### Yattag
> More information in [Download and install yattag](https://www.yattag.org/download-install)

<pre>$ apt-get install python3-yattag</pre>

