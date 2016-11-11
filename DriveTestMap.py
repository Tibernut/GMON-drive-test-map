__author__ = 'cjones84'
import tkinter
import csv
import random
import translate
from tkinter import filedialog



mytrans = translate.transcell()
tc=0


def fmtcols(mylist, cols):
    #Modified and taken from 'masat' at http://stackoverflow.com/questions/171662/formatting-a-list-of-text-into-columns
    maxwidth = max(map(lambda x: len(x), mylist))
    #For whatever reason if my fill character is just a ' ' the columns don't line up.  I have to use a character
    #that fills the entire character space or '_' in this case
    justifyList = list(map(lambda x: x.ljust(maxwidth,'_'), mylist))
    lines = ("\t".join(justifyList[i:i+cols]) for i in range(0,len(justifyList),cols))
    return(str('\n'.join(lines)))

#Creates a Google Earth KML from a GMON csv with CELL IDs distinguished by color
def CellID():
    if b2 == 'null' or b2 == '':
        infobox.set("************************\n"
                    "Please load a file FIRST\n"
                    "************************\n"
                    "   (Click File>Open)")
    else:
        filename = b2
        var = b2.split("/")
        var2 = var[-1]
        var3 = b2.rsplit("/", 1)
        #Create a list of contrasting colors to use for each unique Cell ID
        color = ['ffffff', '8b8378', '7fffd4', '458b74', '838b8b', 'eed5b7', '000000', '0000ff', 'a52a2a', '76ee00', 'ff7f24', '9a32cd', '2f4f4f', '7a7a7a', 'ffb6c1', 'ffff00', '00f5ff', 'ff7f00', '8b7355']
        #Get csvfile
        data = open(filename,)
        #read in the csv file using ; as the delimiter
        read = csv.reader(data, delimiter = ';')
        #create the kml file using the name from csv file
        kml = open(var3[0] + '/' + var2[:-4] + '_Cell' + '.kml', 'w')
        #print(kml)
        #print(var)
        #print(var2[:-4])
        #print(var3[0])
        #This is just stuff that must go into every KML
        kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        kml.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
        kml.write("<Document>\n")
        #This is what the kml file will show up named as in Google Earth
        kml.write("\t<name>" + str(var2[:-4]) + '_Cell' + "</name>\n")
        #create an empty list to use in for loop
        myl = list()
        #make sure we are reading from the top of the csv file and then advance 1 row because GMON creates headers that we must ignore
        data.seek(0)
        next(read)
        #This loop creates a list of unique CellIds contained in the CSV file
        for row in read:
            if row[11] == 'LTE':
                if row[0] not in myl:
                    myl.append(row[0])
            elif row[1] not in myl:
                myl.append(row[1])
        #this loop creates a unique style block for each unique cell id
        #print(myl)
        for s in myl:
            if not color:
                    #print(s)
                    print('ran out of colors')
                    rcolor = "%06x" % random.randint(0, 0xFFFFFF)
                    #print(rcolor)
                    #Sets the style id to the Cell ID so I can easily match it later
                    kml.write("\t<Style id='" + str(s) + "'>\n")
                    kml.write("\t\t<LabelStyle>\n")
                    kml.write("\t\t\t<color>00000000</color>\n")
                    kml.write("\t\t</LabelStyle>\n")
                    kml.write("\t\t<IconStyle>\n")
                    #"..ff" sets the opacity to 100% then we add the string clr
                    kml.write("\t\t\t<color>ff" + rcolor + "</color>\n")
                    kml.write("\t\t\t<scale>0.5</scale>\n")
                    kml.write("\t\t\t<Icon>\n")
                    kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
                    kml.write("\t\t\t</Icon>\n")
                    kml.write("\t\t</IconStyle>\n")
                    kml.write("\t</Style>\n")
            else:
                #print(s)
                #print('still have colors')
                #selects a random color from list color then removes that color from the list
                clr = random.choice(color)
                color.remove(clr)
                #sets the selected color to string so I can use it below
                str(clr)
                #Sets the style id to the Cell ID so I can easily match it later
                kml.write("\t<Style id='" + str(s) + "'>\n")
                kml.write("\t\t<LabelStyle>\n")
                kml.write("\t\t\t<color>00000000</color>\n")
                kml.write("\t\t</LabelStyle>\n")
                kml.write("\t\t<IconStyle>\n")
                #"..ff" sets the opacity to 100% then we add the string clr
                kml.write("\t\t\t<color>ff" + clr + "</color>\n")
                kml.write("\t\t\t<scale>0.5</scale>\n")
                kml.write("\t\t\t<Icon>\n")
                kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
                kml.write("\t\t\t</Icon>\n")
                kml.write("\t\t</IconStyle>\n")
                kml.write("\t</Style>\n")
        kml.write("\t<Folder>\n")
        kml.write("\t\t<name>" + var2[:-4] + "_Cell</name>\n")
        kml.write("\t\t<visibility>0</visibility>\n")
        #go back to start of csv and advance past the header
        data.seek(0)
        next(read)
        #this loop creates a placemark block for every row in the csv
        for row in read:
            #row 1 contains cell id - I flipped it to an integer and back because I needed to get rid of the leading spaces that GMON puts in (probably not the best way to do this)
            if row[0] in mytrans:
              temptrans = mytrans[str(row[0])]
              #print('row0')
            elif row[1] in mytrans:
                temptrans = mytrans[str(row[1])]
                #print('row1')
            else:
                print(row[0])
                temptrans = "Not in dictionary"
                print('couldntfind')
            #print(temptrans)
            lvar = row[0]
            dvar = row[1]
            dint = int(dvar)
            dvarr = str(dint)
            kml.write("\t\t<Placemark>\n")
            kml.write("\t\t\t<name>" + str(row[1]) + "</name>\n")
            #print(row[6])
            if row[11] == 'LTE':
                kml.write("\t\t\t<description>Cell ID: " + str(row[1]) +
                          '\n Sector Name: ' + temptrans +
                          '\nTechnology: ' + str(row[11]) +
                          '\nRSSI: ' + str(row[6]) +
                          '\nRSRP: ' + str(row[8]) +
                          '\nRSRQ: ' + str(row[9]) +
                          '\nSNR: ' + str(row[16]) +
                          '\nDate: ' + str(row[17]) +
                          '\nTime: ' + str(row[18]) +
                          "</description>\n")
            else:
                kml.write("\t\t\t<description>Cell ID: " + str(row[1]) +
                          '\n Sector Name: ' + temptrans +
                          '\nTechnology: ' + str(row[11]) +
                          '\nRSL: ' + str(row[6]) +
                          '\nDate: ' + str(row[17]) +
                          '\nTime: ' + str(row[18]) +
                          "</description>\n")
            if row[11] == 'LTE':
                kml.write("\t\t\t<styleUrl>#" + lvar + "</styleUrl>\n")
            else:
                kml.write("\t\t\t<styleUrl>#" + dvarr + "</styleUrl>\n")
            kml.write("\t\t\t<Point>\n")
            kml.write("\t\t\t\t<coordinates>" + str(row[13]) + "," + str(row[12]) + "</coordinates>\n")
            kml.write("\t\t\t</Point>\n")
            kml.write("\t\t</Placemark>\n")
        kml.write("\t</Folder>\n")
        #this needs to be at the end of every KML file
        kml.write("</Document>\n")
        kml.write("</kml>\n")
        #close the file
        kml.close()
        infobox.set(var2[:-4] + '_Cell.kml\n \nsaved in:\n\n' + str(var3[0]) + "\n\n")
        #print("RSL Finished")

#Creates a Google Earth KML from a GMON csv with RSLs distinguished by color
def RSLMap():
    if b2 == 'null' or b2 == '':
        infobox.set("************************\n"
                    "Please load a file FIRST\n"
                    "************************\n"
                    "   (Click File>Open)")
    else:
        filename = b2
        var = b2.split("/")
        var2 = var[-1]
        var3 = b2.rsplit("/", 1)
        data = open(filename)
        read = csv.reader(data, delimiter = ';')
        kml = open(var3[0] + '/' + var2[:-4] + '_RSL' + '.kml', 'w')
        kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        kml.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
        kml.write("<Document>\n")
        kml.write("\t<name>" + var2[:-4] + '_RSL' + "</name>\n")
        #Create 4 styles for varying levels of signal quality. Should really be a loop!
        kml.write("\t<Style id='0'>\n")
        kml.write("\t\t<LabelStyle>\n")
        kml.write("\t\t\t<color>00000000</color>\n")
        kml.write("\t\t</LabelStyle>\n")
        kml.write("\t\t<IconStyle>\n")
        kml.write("\t\t\t<color>bf000000</color>\n")#black
        kml.write("\t\t\t<scale>0.5</scale>\n")
        kml.write("\t\t\t<Icon>\n")
        kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
        kml.write("\t\t\t</Icon>\n")
        kml.write("\t\t</IconStyle>\n")
        kml.write("\t</Style>\n")
        kml.write("\t\t<Style id='1'>\n")
        kml.write("\t\t<LabelStyle>\n")
        kml.write("\t\t\t<color>00000000</color>\n")
        kml.write("\t\t</LabelStyle>\n")
        kml.write("\t\t<IconStyle>\n")
        kml.write("\t\t\t<color>bfFF0000</color>\n")#blue
        kml.write(" \t\t\t<scale>0.5</scale>\n")
        kml.write("\t\t\t<Icon>\n")
        kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
        kml.write("\t\t\t</Icon>\n")
        kml.write("\t\t</IconStyle>\n")
        kml.write("\t</Style>\n")
        kml.write("\t<Style id='2'>\n")
        kml.write("\t\t<LabelStyle>\n")
        kml.write("\t\t\t<color>00000000</color>\n")
        kml.write("\t\t</LabelStyle>\n")
        kml.write("\t\t<IconStyle>\n")
        kml.write("\t\t\t<color>bf008C14</color>\n")#green
        kml.write("\t\t\t<scale>0.5</scale>\n")
        kml.write("\t\t\t<Icon>\n")
        kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
        kml.write("\t\t\t</Icon>\n")
        kml.write("\t\t</IconStyle>\n")
        kml.write("\t</Style>\n")
        kml.write("\t<Style id='3'>\n")
        kml.write("\t\t<LabelStyle>\n")
        kml.write("\t\t\t<color>00000000</color>\n")
        kml.write("\t\t</LabelStyle>\n")
        kml.write("\t\t<IconStyle>\n")
        kml.write("\t\t\t<color>bf00FFFF</color>\n")#yellow
        kml.write("\t\t\t<scale>0.5</scale>\n")
        kml.write("\t\t\t<Icon>\n")
        kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
        kml.write("\t\t\t</Icon>\n")
        kml.write("\t\t</IconStyle>\n")
        kml.write("\t</Style>\n")
        kml.write("\t<Style id='4'>\n")
        kml.write("\t\t<LabelStyle>\n")
        kml.write("\t\t\t<color>00000000</color>\n")
        kml.write("\t\t</LabelStyle>\n")
        kml.write("\t\t<IconStyle>\n")
        kml.write("\t\t\t<color>bf0000FF</color>\n")#red
        kml.write("\t\t\t<scale>0.5</scale>\n")
        kml.write("\t\t\t<Icon>\n")
        kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
        kml.write("\t\t\t</Icon>\n")
        kml.write("\t\t</IconStyle>\n")
        kml.write("\t</Style>\n")
        kml.write("\t<Style id='5'>\n")
        kml.write("\t\t<LabelStyle>\n")
        kml.write("\t\t\t<color>00000000</color>\n")
        kml.write("\t\t</LabelStyle>\n")
        kml.write("\t\t<IconStyle>\n")
        kml.write("\t\t\t<color>bf7800F0</color>\n")#purple
        kml.write("\t\t\t<scale>0.5</scale>\n")
        kml.write("\t\t\t<Icon>\n")
        kml.write("\t\t\t\t<href>https://sites.google.com/site/pynetmony/home/iconrxl.png</href>\n")
        kml.write("\t\t\t</Icon>\n")
        kml.write("\t\t</IconStyle>\n")
        kml.write("\t</Style>\n")
        kml.write("\t<Folder>\n")
        kml.write("\t\t<name>" + var2[:-4] + "_RSL</name>\n")
        kml.write("\t\t<visibility>0</visibility>\n")
        next(read)
        #create the placemarks and assign each of them to one of the above styles based on signal quality
        for row in read:
            if row[0] in mytrans:
                temptrans = mytrans[str(row[0])]
            elif row[1] in mytrans:
                temptrans = mytrans[str(row[1])]
            else:
                temptrans = "Not in dictionary"
            kml.write("\t\t<Placemark>\n")
            kml.write("\t\t\t<name>" + str(row[1]) + "</name>\n")
            if row[11] == 'LTE':
                kml.write("\t\t\t<description>Cell ID: " + str(row[1]) +
                          '\n Sector Name: ' + temptrans +
                          '\nTechnology: ' + str(row[11]) +
                          '\nRSSI: ' + str(row[6]) +
                          '\nRSRP: ' + str(row[8]) +
                          '\nRSRQ: ' + str(row[9]) +
                          '\nSNR: ' + str(row[16]) +
                          '\nDate: ' + str(row[17]) +
                          '\nTime: ' + str(row[18]) +
                          "</description>\n")
                if float(row[16]) >= 20:
                    kml.write("\t\t\t<styleUrl>#5</styleUrl>\n")#507800F0
                elif float(row[16]) >= 16:
                    kml.write("\t\t\t<styleUrl>#4</styleUrl>\n")
                elif float(row[16]) >= 12:
                    kml.write("\t\t\t<styleUrl>#3</styleUrl>\n")
                elif float(row[16]) >= 9:
                    kml.write("\t\t\t<styleUrl>#2</styleUrl>\n")
                elif float(row[16]) >= 5:
                    kml.write("\t\t\t<styleUrl>#1</styleUrl>\n")
                else:
                    kml.write("\t\t\t<styleUrl>#0</styleUrl>\n")
                kml.write("\t\t\t<Point>\n")
                kml.write("\t\t\t\t<coordinates>" + str(row[13]) + "," + str(row[12]) + "</coordinates>\n")
                kml.write("\t\t\t</Point>\n")
                kml.write("\t\t</Placemark>\n")
            else:
                kml.write("\t\t\t<description>Cell ID: " + str(row[1]) +
                          '\n Sector Name: ' + temptrans +
                          ##mytrans[str(row[1])] +
                          '\nTechnology: ' + str(row[11]) +
                          '\nRSL: ' + str(row[6]) +
                          '\nDate: ' + str(row[17]) +
                          "</description>\n")
                if int(row[6]) >= -60:
                    kml.write("\t\t\t<styleUrl>#5</styleUrl>\n")
                elif int(row[6]) >= -69:
                    kml.write("\t\t\t<styleUrl>#4</styleUrl>\n")
                elif int(row[6]) >= -78:
                    kml.write("\t\t\t<styleUrl>#3</styleUrl>\n")
                elif int(row[6]) >= -86:
                    kml.write("\t\t\t<styleUrl>#2</styleUrl>\n")
                elif int(row[6]) >= -95:
                    kml.write("\t\t\t<styleUrl>#1</styleUrl>\n")
                else:
                    kml.write("\t\t\t<styleUrl>#0</styleUrl>\n")
                kml.write("\t\t\t<Point>\n")
                kml.write("\t\t\t\t<coordinates>" + str(row[13]) + "," + str(row[12]) + "</coordinates>\n")
                kml.write("\t\t\t</Point>\n")
                kml.write("\t\t</Placemark>\n")
        kml.write("\t</Folder>\n")
        kml.write("</Document>\n")
        kml.write("</kml>\n")
        kml.close()
        infobox.set(var2[:-4] + '_RSL.kml\n \nsaved in:\n\n' + str(var3[0]) + "\n\n")

def getfile():
    global b2
    b2 = filedialog.askopenfilename( filetypes = (("Text Files", "*.txt"), ("All Files", "*.*")))
    if b2 == '':
        infobox.set("************************\n"
                    "Please load a file FIRST\n"
                    "************************\n"
                    "   (Click File>Open)")
    else:
        var = b2.split('/')
        infobox.set(var[-1] + ' loaded')

def analyze():
    #create/empty list of cells
    myl2 = []
    if b2 == 'null' or b2 == '':
        infobox.set("************************\n"
                    "Please load a file FIRST\n"
                    "************************\n"
                    "   (Click File>Open)")
    else:
        var = b2.split("/")
        var2 = var[-1]
        data = open(b2)
        read = csv.reader(data, delimiter = ';')
        bad = 0
        good = 0
        medium = 0
        terrible = 0
        HSPA = 0
        HSPAP = 0
        HSDPA = 0
        UMTS = 0
        LTE = 0
        NA = 0
        EDGE = 0
        GPRS = 0
        UNKNOWN = 0
        messagetext2 =""
        opstring = ''
        next(read)
        for row in read:
            if row[1] in mytrans:
                temptrans = mytrans[str(row[1])]
            else:
                temptrans = "Not in dictionary"
            if row[11] == "HSPA+":
                HSPAP = HSPAP + 1
            elif row[11] == "HSPA":
                HSPA = HSPA + 1
            elif row[11] == "HSDPA":
                HSDPA = HSDPA + 1
            elif row[11] == "n/a":
                NA = NA + 1
            elif row[11] == "EDGE":
                EDGE = EDGE + 1
            elif row[11] == "GPRS":
                GPRS = GPRS +1
            elif row[11] == "UMTS":
                UMTS = UMTS +1
            elif row[11] == "LTE":
                LTE = LTE +1
            else:
                UNKNOWN = UNKNOWN + 1
                print("noooo")
                print(row[11])
            if int(row[6]) >= -70:
                good = good + 1
            elif int(row[6]) >= -80:
                medium = medium + 1
            elif int(row[6]) >= -95:
                bad = bad + 1
            else:
                terrible = terrible +1
        data.seek(0)
        next(read)
        techtot = HSPA + HSPAP + HSDPA + NA + EDGE + GPRS + UMTS + LTE + UNKNOWN
        if HSPAP > 0:
            HSPAP = HSPAP/techtot*100
            messagetext2 = messagetext2 + "%.2f" %HSPAP + "% of data points were HSPA+\n"
        if HSPA > 0:
            HSPA = HSPA/techtot*100
            messagetext2 = messagetext2 + "%.2f" %HSPA + "% of data points were HSPA\n"
        if HSDPA > 0:
            HSDPA = HSDPA/techtot*100
            messagetext2 = messagetext2 + "%.2f" %HSDPA + "% of data points were HSDPA\n"
        if UMTS > 0:
            UMTS = UMTS/techtot*100
            messagetext2 = messagetext2 + "%.2f" %UMTS + "% of data points were UMTS\n"
        if EDGE > 0:
            EDGE = EDGE/techtot*100
            messagetext2 = messagetext2 + "%.2f" %EDGE + "% of data points were EDGE\n"
        if GPRS > 0:
            GPRS = GPRS/techtot*100
            messagetext2 = messagetext2 + "%.2f" %GPRS + "% of data points were GPRS\n"
        if LTE > 0:
            LTE = LTE/techtot*100
            messagetext2 = messagetext2 + "%.2f" %LTE + "% of data points were LTE\n"
        if UNKNOWN > 0:
            UNKNOWN = UNKNOWN/techtot*100
            messagetext2 = messagetext2 + "%.2f" %UNKNOWN + "% of datapints were UNKNOWN\n"
        if NA > 0:
            NA = NA/techtot*100
            messagetext2 = messagetext2 + "%.2f" %NA + "% of datapints were out of coverage\n"
        total = good + medium + bad + terrible
        if good > 0:
            good = good/total*100
        if bad > 0:
            bad = bad/total*100
        if medium > 0:
            medium = medium/total*100
        if terrible > 0:
            terrible = terrible/total*100
        messagetext = "%.2f" %good + "% of data points were greater than -70 dB\n"\
                      + "%.2f" %medium + "% of data points were between -80 dB and -70 dB\n" \
                      + "%.2f" %bad + "% of data points were between -80 dB and -95 dB\n" \
                      + "%.2f" %terrible + "% of datapints were worse than -95 dB \n"
        #This loop creates a list of unique CellIds contained in the CSV file
        myl = list()
        for row in read:
            if row[11] == 'LTE':
                if row[0] not in myl:
                    myl.append(row[0])
            else:
                if row[11] != 'LTE':
                    if row[1] not in myl:
                        #print(myl)
                        #print(row[11])
                        #print(row[18])
                        #print(row[1])
                        myl.append(row[1])
        #this loop creates a unique style block for each unique cell id
        listlength = len(myl)
        mylint = list(map(int, myl))
        #print(list(map(int, myl)))
        mylint = (sorted(mylint, key=int))
        #print(myl)
        for i in myl:
            try:
                ii = mytrans[str(i)]
                myl2.append(ii)
            except:
                myl2.append(i)

        #print(myl2)
        infobox.set(var2 + ' loaded'
                           '\n\nDrive Test RSLs:'
                           '\n----------------------------------------------------------------------\n'
                    + messagetext + "\n Technology Types seen:"
                                    "\n----------------------------------------------------------------------\n"
                    + messagetext2 +'\nUnique cells seen (' + str(listlength)
                    + '):\n----------------------------------------------------------------------\n'
                     + fmtcols(myl2,2))

window = tkinter.Tk()
window.resizable(0,1)
infobox = tkinter.StringVar()
b2 = 'null'
window.title("Drive Test Map")
menubar = tkinter.Menu(window)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=getfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)


lbl = tkinter.Label(window, relief='sunken', anchor='n', height = 30, border=2, width=58, wrap=350, background='white', justify='left', textvariable=infobox, takefocus='True', state='active')
infobox.set('Please open a file to be processed')
CID = tkinter.Button(window, text="Cell ID Map", command=CellID)
RSL = tkinter.Button(window, text="RSL Map", command=RSLMap)
ANL = tkinter.Button(window, text="Analyze", command=analyze)



window.config(menu=menubar)
lbl.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='s')
CID.grid(row=2, column=1, sticky='s')
RSL.grid(row=2, column=2, sticky='s')
ANL.grid(row=2, column=0, sticky='s')

window.mainloop()
