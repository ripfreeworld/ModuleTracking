# This script is to record all antennas

import sys
import psycopg2
import requests
from bs4 import BeautifulSoup
import connect

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                  'Safari/537.36'}

url = 'https://vlbisysmon.evlbi.wettzell.de/monitoring_archive/fs_web_pages/ivsquickstatus.html'
# IVS e-QuickStatus

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

table = soup.find(lambda tag: tag.name == 'table')
# this is the way to locate antenna code lack of labels
rows = table.findAll(lambda tag: tag.name == 'tr')


conn = connect.conn
cursor = connect.cursor

cursor.execute('''create table IF NOT EXISTS stations (
                        station_name varchar(40) UNIQUE NOT NULL,
                        station_code varchar(10) PRIMARY KEY 
                                                  )''')

conn.commit()
if cursor.execute('''SELECT EXISTS (SELECT relname FROM pg_class WHERE relname = 'stations')''') == 't':
    print('TABLE stations created successfully...\n')

for row in rows:
    antenna_links = row.findAll('a')
    for antenna_link in antenna_links:
        parent = antenna_link.parent
        # the antennaCode is next to the antennaName
        antennaName = antenna_link.text.strip()
        antennaCode = parent.findNext('td').text.strip()
        ##########################################

        ##########################################

        try:  # ON CONFLICT (VSN, time, checkTime, remainingGB) DO NOTHING
            cursor.execute("insert into stations(station_name, station_code) "
                           "values (%s, %s)",
                           (antennaName, antennaCode))
            # without `[]` would lead to error
            print("The current Station has been now successfully added to database!\n")
        except:
            print(f"The Station {antennaName} already exists!\n")
        finally:
            conn.commit()
            # without `commit()`, psycopg2.errors.InFailedSqlTransaction occurs


if conn:
    cursor.execute('select * from stations')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # close the connection
    conn.close()
    print('Closed...')