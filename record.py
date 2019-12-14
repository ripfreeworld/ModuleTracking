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
                        schedule varchar(20) NOT NULL,
                        CONSTRAINT no_duplicate UNIQUE (VSN, mtime, checkTime, remainingGB)
                                                  )''')
                        # the constraint name `no_duplicate` can exist only once in the entire database

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
        stationName = stationName[0].lower()
        # .lower() is to convert uppercase to lowercase e.g. WETTZELL -> wettzell
        url = f"https://vlbisysmon.evlbi.wettzell.de/monitoring_archive/fs_web_pages/{stationName}" \
            f"/Mark5RemainingCapacity.html"
        url2readSchedule = f"https://vlbisysmon.evlbi.wettzell.de/monitoring_archive/fs_web_pages/{stationName}" \
            f"/eQuickStatusReport.txt"

        page = requests.get(url, headers=headers)
        page2readSchedule = requests.get(url2readSchedule, headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')
        # in order to find the corresponding schedule and add to tuple
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

        content = soup2readSchedule.text
        list_content = content.split()
        schedule = None

        try:
            vsn = list_content[list_content.index("Mark5VSN") + 2]
            if vsn == VSN : # to make sure that the VSN has not changed at the reading moment
                schedule_index = list_content.index("Schedule ")
                # avoid the situation that schedule is empty. It wouldn't have an empty sting " ", but just nothing
                if list_content[schedule_index + 3] is not "=":
                    schedule = list_content[schedule_index + 2]
                    # if schedule is empty, it would keep being None
        except:
            print(f"cannot get information from {stationName} at the moment")

        data = [(stationName, moduleAB, VSN, mtime, remainingGB, remainingPer, checkTime, schedule)]
        print("current information", data)
        # don't save the information with empty schedule, otherwise it generates redundant data with empty schedule
        # as a new schedule label
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
