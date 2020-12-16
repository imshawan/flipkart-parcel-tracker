import requests
import pandas as pd
import trackfile
from bs4 import BeautifulSoup


def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]

def track(trackingID):
    rows1 = []
    rows = []
    try:
        r = requests.get(f'https://ekartlogistics.com/track/{trackingID}/').text
    except:
        print("Sorry, No Internet Connection!")
        input("")
        return

    soup = BeautifulSoup(r, 'html.parser')
    table1 = soup.find( "table", { 'class' : 'col-md-12 table-bordered table-striped table-condensed cf width-100' } )
    table = soup.findAll( "table", { 'class' : 'col-md-12 table-bordered table-striped table-condensed cf width-100' } )
    try:
        trsf = table1.find_all('tr')
    except AttributeError:
        print("Invalid Tracking ID")
        return
    headerow1 = rowgetDataText(trsf[0], 'th')
    if headerow1: # if there is a header row include first
        rows1.append(headerow1)
        trsf = trsf[1:]
    for tr in trsf: # for every table row
        rows1.append(rowgetDataText(tr, 'td') ) # data row       
    headerow1 = rowgetDataText(trsf[0], 'th')
    dftable1 = pd.DataFrame(rows1[1:], columns=rows1[0])
    print(dftable1)



    print("\n                             Detailed Tracking Details:")
    for tables in table:
        trs1 = tables.findAll('tr')
    trs = trs1
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row       
    headerow = rowgetDataText(trs[0], 'th')

    dftable = pd.DataFrame(rows[1:], columns=rows[0])

    print("    " + dftable)
    print("\n    *********************************************************************************************")

    
i=0
tracking = trackfile.trackingIDS
info = trackfile.item_info['iteminfo']
for trackinginfo in tracking.values():
    for ids in trackinginfo:
        print("\nCurrently Tracking Item: %s \n" %info[i])
        i +=1
        track(ids)

input("")
