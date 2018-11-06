import time
import sys

starttime = time.time()

#############################
## Make table ###############
#############################
def maketable(fname):
    # Reads file and make a table
    with open(fname, 'r') as f: #, encoding = "Latin-1") as f:
        content = f.readlines()

    HeaderRow = content[0]
    Header = list()
    s = ''
    for c in HeaderRow:
        if (c != ';'):
            s = s + c
        if (c == ';'):
            Header.append(s)
            s = ''

    # make 2D array of strings as table
    table = [['' for j in range(len(Header))] for i in range(len(content))]
    table[0] = Header
    i = 0
    for Row in content[1 : len(content)]:
        i = i + 1
        s = ''
        r = list()
        for c in Row:
            if (c != ';'):
                s = s + c
            if (c == ';'):
                r.append(s)
                s = ''
        table[i] = r

    return table

######################################################################
######### Sorts the table based on column index and visa status ######
######################################################################
def SortTop(table, SortIndex, VisaIndex, VisaStatus):
    TableIndex = [i for i, s in enumerate(table[0]) if SortIndex in s]
    VisaStatusIndex = [i for i, s in enumerate(table[0]) if VisaIndex in s]
                 
    Index = [[row[VisaStatusIndex[0]], row[TableIndex[0] ]] for row in table[1:len(table)]]
    
    IndexSet = set([row[1] for row in Index])
    IndexCount = [[0, 0] for i in range(len(IndexSet))]
    IndexCountDict = dict(zip(IndexSet, IndexCount))

    for j in Index:
        if j[0] == VisaStatus:
            IndexCountDict[j[1]][0] = IndexCountDict[j[1]][0] + 1

    StatusIndexSorted = sorted(IndexCountDict.items(), \
                               key=lambda value: (value[1][0], value[0]), reverse = True)

    
    v = [x[1] for x in StatusIndexSorted]
    Sum = sum([float(x[0]) for x in v])
    Percentage = [float(x[0])/Sum for x in v]
    for i in range(len(StatusIndexSorted)):
        StatusIndexSorted[i][1][1] = round(Percentage[i] * 100, 1)
        
    return StatusIndexSorted

#############################
### Writes output to file ###
#############################
def Write2File(fname, data, header, number, separator):
    with open(fname, 'w+') as f:
        s = header[0] + ';' + header[1] + ';' + header[2] + '\n'
        f.write(s)
        for x in data[0 : number]:
            s = str(x[0]) + ';' + str(x[1][0]) + ';' + str(x[1][1]) + '%' + '\n'
            f.write(s)
            
    return 0
    
#fname = 'H1b_Data/H1B_FY_2014.csv'
fname = sys.argv[1]
joboutfile = sys.argv[2]
statesoutfile = sys.argv[3]
if len(sys.argv) < 4:
    fname = './input/h1b_input.csv'
    joboutfile = './output/top_10_occupations.txt'
    statesoutfile = '.output/top_10_states.txt'
    
table = maketable(fname)

#topcertifiedjobs = SortTop(table, 'LCA_CASE_JOB_TITLE', 'STATUS', 'CERTIFIED') 
topcertifiedjobs = SortTop(table, 'JOB_TITLE', 'CASE_STATUS', 'CERTIFIED') 
#topcertifiedstates = SortTop(table, 'LCA_CASE_WORKLOC1_STATE', 'STATUS', 'CERTIFIED')
topcertifiedstates = SortTop(table, 'EMPLOYER_STATE', 'CASE_STATUS', 'CERTIFIED')

outheader = ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']
Write2File(joboutfile, topcertifiedjobs, outheader, 10, ';')
outheader = ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']
Write2File(statesoutfile, topcertifiedstates, outheader, 10, ';')


#print("Header = ", table[0])
#print("Last Row = ", table[len(table) - 1])
#print('Elapsed time = ', time.time() - starttime)
