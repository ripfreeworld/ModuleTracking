from yattag import Doc
import report

newInfo = report.recordList
history = report.historyList_pair


def create_file(file_name):
    f = open(file_name, "w+")
    # w: write      +: create a file if it does not exist in library
    f.write(result)

    f.close()


result = None

doc, tag, text, line = Doc().ttl()
# doc = Doc()
# tag = doc.tag
# text = doc.text

#########################################################################
with tag('html'):
    with tag('body'):
        with tag ('table', width="100%", border="1", bgcolor="#FFFFFF", cellpadding="0", cellspacing="0", align="left"):
            with tag('tr'):     # row of title
                with tag('th', scope="col", bgcolor="#D6E3BC", colspan="8", style="font-size:14pt;"):
                    text('The latest information of each antenna')
            with tag('tr'):     # row of names
                title_name = ( 'Station', 'Schedule', 'A or B', 'VSN', 'TIME', 'REMAINING GB', 'REMAINING PERCENT(%)')
                for tn in title_name:
                    with tag('td', bgcolor="#FFFFFF",
                             style="font-size:11pt;""font-weight: bold;", align="center", width="160"):
                        # setting bold differently in style
                        with tag('font', color="#000000"):
                            text(tn)
            for row in newInfo:
                with tag('tr'):     # every row except the title_row
                    for element in row:
                        with tag('td', bgcolor="#FFFFFF", style="font-size:11pt;", align="center", width="160"):
                            # setting bold differently in style
                            with tag('font', color="#000000"):
                                text(str(element))      # convert every element in the mixed tuple to str

result = doc.getvalue()

create_file("latestAntenna.html")

doc, tag, text, line = Doc().ttl()
#######################################################################
with tag('html'):
    with tag('body'):
        with tag ('table', width="100%", border="1", bgcolor="#FFFFFF", cellpadding="0", cellspacing="0", align="left"):
            with tag('tr'):     # row of title
                with tag('th', scope="col", bgcolor="#D6E3BC", colspan="9", style="font-size:14pt;"):
                    text('The history of each VSN-Antenna Pair')
            with tag('tr'):     # row of names
                title_name = ( 'VSN', 'STATION', 'Schedule', 'A or B', 'TIME', 'REMAINING GB', 'REMAINING PERCENT(%)',
                               'GENERATED TIME', 'EXISTENCE')
                for tn in title_name:
                    with tag('td', bgcolor="#FFFFFF",
                             style="font-size:11pt;""font-weight: bold;", align="center", width="160"):
                        # setting bold differently in style
                        with tag('font', color="#000000"):
                            text(tn)
            for row in history:
                with tag('tr'):     # every row except the title_row
                    for element in row:
                        with tag('td', bgcolor="#FFFFFF", style="font-size:11pt;", align="center", width="160"):
                            # setting bold differently in style
                            with tag('font', color="#000000"):
                                text(str(element))      # convert every element in the mixed tuple to str

result = doc.getvalue()

create_file("historyAntenna.html")