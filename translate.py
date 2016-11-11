import csv
from collections import defaultdict
def transcell():
    with open('celldict.csv', mode='r') as infile:
        reader = csv.reader(infile)
        #mydict = defaultdict(str, '')
        mydict = {rows[0]:rows[1] for rows in reader}
        #mydict.setdefault(str, 'None')
        #print(mydict)

    return mydict
transcell()
#put the following in your program to use:
#celltrans = translate()
#print(celltrans['your value here'])
