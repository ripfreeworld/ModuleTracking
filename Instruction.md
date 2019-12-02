# How to use this Module Tracking
>------------------**JumpingJIVE**------------------\
>Author: Chenyang Liu
##  Installation
### MacOS
>More informations in
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

1. 


## install package for python3
###
