# SELECT from TABLE Capacity and show just the end result of each VSN
# indicator is to distinguish between current and history
import connect as conn

cursor = conn.cursor

newRecordList = []
historyList_pair = []
historyList_VSN_lastState = []
# to count identical antenna names for output format in .html
antennaCounter_dict = {}
vsnCounter_dict = {}



# DISTINCT ON is for PostSQL only

cursor.execute('''SELECT DISTINCT ON (whichAntenna, AorB)
                      whichAntenna, Schedule, AorB, VSN, mtime, remainingGB, remainingPer
                  FROM capacity
                  ORDER BY whichAntenna, AorB, created_at DESC ''')
lastRecords = cursor.fetchall()
for lr in lastRecords:
    newRecordList.append(lr)
    print(lr)

cursor.execute('''SELECT DISTINCT whichAntenna FROM capacity 
                  ORDER BY whichAntenna ASC''')
antenna_raw = cursor.fetchall()
# initialize antennaCounter_dict
for a in antenna_raw:
    antennaCounter_dict[a[0]] = 0
for aTuple in newRecordList:
    antennaCounter_dict[aTuple[0]] += 1

# if some VSN show more than once, (but VSN-Antenna-Schedule pairs are unique),
# it means these VSN are used more than once
# all unique VSN means also all newest VSN
cursor.execute('''SELECT DISTINCT ON (VSN)
                      VSN, whichAntenna, Schedule, AorB, mtime, remainingGB, remainingPer, created_at
                  FROM capacity
                  ORDER BY VSN, created_at DESC ''')
VSN_lastState = cursor.fetchall()
for vl in VSN_lastState:
    historyList_VSN_lastState.append(vl)

# all unique combinations of VSN-Antenna-Schedule
# because even the same VSN-Antenna combination could have not only one schedule
cursor.execute('''SELECT DISTINCT ON (VSN, whichAntenna, schedule)
                      VSN, whichAntenna, Schedule, AorB, mtime, remainingGB, remainingPer, created_at
                  FROM capacity
                  ORDER BY VSN, whichAntenna, schedule, created_at DESC 
                  ''')
VSN_Antenna_Schedule_history = cursor.fetchall()
for vah in VSN_Antenna_Schedule_history:
    historyList_pair.append(vah)

cursor.execute('''SELECT DISTINCT VSN FROM capacity''')
VSN_raw = cursor.fetchall()

# initialize vsnCounter_dict
for vsn in VSN_raw:
    vsnCounter_dict[vsn[0]] = 0
for aTuple in historyList_pair:
    vsnCounter_dict[aTuple[0]] += 1
for i in range(len(historyList_pair)):
    if historyList_pair[i] not in historyList_VSN_lastState:
        historyList_pair[i] += ("Out of date",)
    else:
        historyList_pair[i] += ("latest",)

# Alternative
    # cursor.execute('''SELECT m.VSN, m.mtime, m.remainingGB, m.remainingPer, t.create_t
    #                   FROM (
    #                         SELECT VSN, MAX(created_at) AS create_t
    #                         FROM capacity
    #                         GROUP BY VSN
    #                         ) t JOIN capacity m ON m.VSN = t.VSN AND t.create_t = m.created_at
    #                   WHERE whichAntenna = %s AND AorB = 'A'
    #                   ''', antennaName)
    # VSN_history = cursor.fetchall()
    # print(VSN_history)
    #
    # cursor.execute('''SELECT count(DISTINCT whichAntenna)
    #                   FROM capacity''')
    # # get the integer because of the following iteration
    # numAntenna = cursor.fetchall()[0][0]
    # print(numAntenna)

    # offset starts with 0
    # for i in range(numAntenna):
    #     # each iteration is for one Antenna
    #     cursor.execute('''SELECT DISTINCT whichAntenna
    #                       FROM capacity
    #                       ORDER BY whichAntenna
    #                       LIMIT 1 OFFSET %s''', str(i))
    #
    #     antennaName = cursor.fetchall()
    #     # print(antennaName)
    #
    #     # the latest record
    #     cursor.execute('''SELECT whichAntenna, Schedule, AorB, VSN, mtime, remainingGB, remainingPer
    #                       FROM capacity
    #                       WHERE whichAntenna = %s AND AorB = 'A'
    #                       ORDER BY created_at DESC
    #                       LIMIT 1''', antennaName)
    #     lastRecord = cursor.fetchall()
    #     # Although length exists throughout, it is always overwritten each time before usage
    #     length = len(lastRecord)
    #     antennaCounter_dict[antennaName[0][0]] = length
    #     for lr in lastRecord:
    #         newRecordList.append(lr)
    #         print(lr)
    #
    #     cursor.execute('''SELECT whichAntenna, Schedule, AorB, VSN, mtime, remainingGB, remainingPer
    #                       FROM capacity
    #                       WHERE whichAntenna = %s AND AorB = 'B'
    #                       ORDER BY created_at DESC
    #                       LIMIT 1''', antennaName)
    #     lastRecord = cursor.fetchall()
    #     # to break the square brackets, namely avoid nested list
    #     length = len(lastRecord)
    #     antennaCounter_dict[antennaName[0][0]] += length
    #     for lr in lastRecord:
    #         newRecordList.append(lr)
    #         print(lr)

