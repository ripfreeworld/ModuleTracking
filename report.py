# SELECT from TABLE Capacity and show just the end result of each VSN
# indicator is to distinguish between current and history
import connect as conn

cursor = conn.cursor
cursor.execute('''SELECT count(DISTINCT whichAntenna) 
                  FROM capacity''')
# get the integer because of the following iteration
numAntenna = cursor.fetchall()[0][0]
#print(numAntenna)

recordList = []
historyList_pair = []
historyList_VSN = []

# offset starts with 0
for i in range(numAntenna):
    # each iteration is for one Antenna
    cursor.execute('''SELECT DISTINCT whichAntenna
                      FROM capacity
                      ORDER BY whichAntenna
                      LIMIT 1 OFFSET %s''', str(i))

    antennaName = cursor.fetchall()
    #print(antennaName)

    # the latest record
    cursor.execute('''SELECT whichAntenna, Schedule, AorB, VSN, mtime, remainingGB, remainingPer
                      FROM capacity
                      WHERE whichAntenna = %s AND AorB = 'A'
                      ORDER BY created_at DESC
                      LIMIT 1''', antennaName)
    lastRecord = cursor.fetchall()
    for lr in lastRecord:
        recordList.append(lr)

    cursor.execute('''SELECT whichAntenna, Schedule, AorB, VSN, mtime, remainingGB, remainingPer
                      FROM capacity
                      WHERE whichAntenna = %s AND AorB = 'B'
                      ORDER BY created_at DESC
                      LIMIT 1''', antennaName)
    lastRecord = cursor.fetchall()
    # to break the square brackets, namely avoid nested list
    for lr in lastRecord:
        recordList.append(lr)

    # DISTINCT ON is for PostSQL only
    # all unique combinations of VSN-Antenna-Schedule
    cursor.execute('''SELECT DISTINCT ON (VSN, whichAntenna, schedule)
                          VSN, whichAntenna, Schedule, AorB, mtime, remainingGB, remainingPer, created_at
                      FROM capacity
                      WHERE whichAntenna = %s
                      ORDER BY VSN, whichAntenna, schedule, created_at DESC 
                      ''', antennaName)
    VSN_Antenna_Schedule_history = cursor.fetchall()
    for vah in VSN_Antenna_Schedule_history:
        historyList_pair.append(vah)

    # if some VSN show more than once, (but VSN-Antenna-Schedule pairs are unique),
    # it means these VSN are used more than once
    cursor.execute('''SELECT DISTINCT ON (VSN)
                          VSN, whichAntenna, Schedule, AorB, mtime, remainingGB, remainingPer, created_at
                      FROM capacity
                      WHERE whichAntenna = %s
                      ORDER BY VSN, created_at DESC 
                      ''', antennaName)
    VSN_history = cursor.fetchall()
    for vh in VSN_history:
        historyList_VSN.append(vh)

for i in range(len(historyList_pair)):
    if historyList_pair[i] not in historyList_VSN:
        historyList_pair[i] += ("Out of date",)
    else:
        historyList_pair[i] += ("Overwritten",)

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
