# This script is to combine Antenna Schedule and VSN together
import requests
import time
from bs4 import BeautifulSoup
from bs4 import Comment
import connect

conn = connect.conn
cursor = connect.cursor

cursor.execute('''SELECT EXISTS (SELECT relname FROM pg_class WHERE relname = 'capacity')''')
if cursor.fetchall()[0][0] is False:
    print('TABLE capacity is to be created...\n')
cursor.execute('''create table IF NOT EXISTS capacity (
                        id SERIAL PRIMARY KEY,
                        whichAntenna varchar(40),
                        hdd_slot varchar(10) NOT NULL,
                        VSN varchar(20) NOT NULL,
                        mtime varchar(40) NOT NULL,
                        remainingGB decimal(10,3) NOT NULL,
                        remainingPer decimal(3,1) NOT NULL,
                        checkTime time(0) NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT Now(),
                        schedule varchar(20),
                        CONSTRAINT no_duplicate UNIQUE (VSN, mtime, checkTime, remainingGB)
                                                  )''')

conn.commit()


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.90 Safari/537.36'}


while True:
    cursor.execute('''SELECT station_name FROM stations''')
    stationNames = cursor.fetchall()

    # Each station has its own url, which only differs in one segment, i.e. /.../
    for stationName in stationNames:
        # tuple
        stationName = stationName[0]
        # .lower() is to convert uppercase to lowercase e.g. WETTZELL -> wettzell
        url = f"https://vlbisysmon.evlbi.wettzell.de/monitoring_archive/fs_web_pages/{stationName.lower()}" \
            f"/Mark5RemainingCapacity.html"
        url2readSchedule = f"https://vlbisysmon.evlbi.wettzell.de/monitoring_archive/fs_web_pages/ivsquickstatus.html"

        page = requests.get(url, headers=headers)
        page2readSchedule = requests.get(url2readSchedule, headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')
        soup2readSchedule = BeautifulSoup(page2readSchedule.text, 'html.parser')

        moduleAB = None
        VSN = None
        selected = None
        mtime = None
        remainingGB = None
        remainingPer = None
        checkTime = None

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if comment in ['ERC::SELECTED_MODULEA']:
                if comment.next_element.strip() == '>':
                    moduleAB = 'A'
                    for commentA in comments:
                        if commentA in ['ERC::VSN_MODULEA']:
                            VSN = commentA.next_element.strip()
                        if commentA in ['ERC::TIME_MODULEA']:
                            mtime = commentA.next_element.strip()
                        if commentA in ['ERC::REMAININGGB_MODULEA']:
                            remainingGB = commentA.next_element.strip()
                        if commentA in ['ERC::REMAININGPERCENT_MODULEA']:
                            remainingPer = commentA.next_element.strip()
                        if commentA in ['ERC::CHECKTIME_MODULEA']:
                            checkTime = commentA.next_element.strip()
            if comment in ['ERC::SELECTED_MODULEB']:
                if comment.next_element.strip() == '>':
                    moduleAB = 'B'
                    for commentB in comments:
                        if commentB in ['ERC::VSN_MODULEB']:
                            VSN = commentB.next_element.strip()
                        if commentB in ['ERC::TIME_MODULEB']:
                            mtime = commentB.next_element.strip()
                        if commentB in ['ERC::REMAININGGB_MODULEB']:
                            remainingGB = commentB.next_element.strip()
                        if commentB in ['ERC::REMAININGPERCENT_MODULEB']:
                            remainingPer = commentB.next_element.strip()
                        if commentB in ['ERC::CHECKTIME_MODULEB']:
                            checkTime = commentB.next_element.strip()

        if moduleAB is None:
            print("Neither Module A nor Module B is selected")

        table = soup2readSchedule.find(lambda tag: tag.name == 'table')
        # this is the way to locate antenna code lack of labels
        rows = table.findAll(lambda tag: tag.name == 'tr')
        schedule = None
        for row in rows:
            antenna_links = row.findAll('a')
            for antenna_link in antenna_links:
                parent = antenna_link.parent
                antennaName = antenna_link.text.strip()
                vsn = parent.find_next_siblings()[7].text.strip()
                if antennaName == stationName and vsn == VSN:
                    schedule = parent.find_next_siblings()[4].text.strip()
                if schedule == '':
                    schedule = None
        data = [(stationName, moduleAB, VSN, mtime, remainingGB, remainingPer, checkTime, schedule)]
        print("current information", data)
        # insert into the table capacity
        try:  # ON CONFLICT (stationName, moduleAB, VSN, mtime, checkTime, remainingGB) DO NOTHING
            cursor.execute("insert into capacity(id, whichAntenna, hdd_slot, VSN, mtime, remainingGB, remainingPer, "
                           "checkTime, schedule) "
                           "values (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (stationName, moduleAB, VSN, mtime, remainingGB, remainingPer, checkTime, schedule))
            print("The current DATA has been successfully added to database!\n")
        except:
            print("Nothing to update.\n")
        finally:
            # without commit(), psycopg2.errors.InFailedSqlTransaction occurs
            conn.commit()

    time.sleep(5)
    # gap between each tracking
