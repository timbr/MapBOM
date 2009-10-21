import pyodbc
import string
import datetime
from tim_modules import pysyteline

namedata={}
matdata={}

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GBSYTELINEDB1;DATABASE=UK_App;Trusted_Connection=Yes')

cursor = cnxn.cursor()

def query(in_list):
    command="""select DISTINCT 
    rvxCurrentMaterials.Item, 
    rvxCurrentMaterials.Description, 
    rvxCurrentMaterials.Material, 
    rvxCurrentMaterials.\"Material Description\" as matdesc, 
    rvxCurrentMaterials.Quantity 
    FROM UK_App.dbo.rvxCurrentMaterials 
    WHERE rvxCurrentMaterials.Item in (%s) AND rvxCurrentMaterials.Material like '_-%%' 
    ORDER BY rvxCurrentMaterials.Material""" % in_list
    
    return command
    

f=open('outputodbc.mm', 'w')

def CreateDictionary(part):
    if part[-1] != "'" and part[:1] != "'":
        part = "'" + part + "'"
    print "Parent: " + part

    cursor.execute(query(part))
    result = cursor.fetchall()
    
    if result != []:
        for row in result:
            if row.Item not in namedata:
                namedata[row.Item] = row.Description
            if row.Material not in namedata:
                namedata[row.Material] = row.matdesc
                
        for row in result:
            if row.Item not in matdata:
                matdata[row.Item] = [[row.Material, row.Quantity]]
            else:
                matdata[row.Item].append([row.Material, row.Quantity])

        
        children = [child.Material for child in result]
        p_list=''
        for t in children[:-1]:
            p_list += "'" + str(t) + "', "
            
        p_list += "'" + children[-1] + "'"
        print p_list
        
        CreateDictionary(p_list)

        
def findchildren(part,tab):
    if tab==-1:
        desc = namedata[part]
        timeformat = format = "%d-%m-%Y    %H:%M:%S"
        timenow = datetime.datetime.today().strftime(timeformat)
        f.write('<node STYLE="fork" TEXT="' + part + '  ' + str(desc) + \
                '\n        As of: ' + timenow + '">\n')
        f.write('<edge WIDTH="thin"/>\n')
    if part in matdata:
        result = matdata[part]
        if tab != -1:
            f.write(' FOLDED="true" >\n')
        tab+=1
        for row in result:
            materialdesc = namedata[str(row[0])]
            html = string.replace(str(materialdesc), '&' , '&amp;')
            html2 = string.replace(html, '"' , '&quot;')
            quant = str(pysyteline.clean_number(row[1], 3))
            line = str(row[0]) + '  ' + html2 + '  ' + quant + '-off'
            #print line
            f.write('<node POSITION="right" TEXT="' + line + '"')
            next = findchildren(str(row[0]),tab)
            if next != 'nochild':
                f.write('</node>\n')
    else:
        f.write('/>\n')
        return 'nochild'


part ="A-9836-3294-01"
f.write('<map version="0.8.1">\n')
f.write('<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->\n')
CreateDictionary(part)
findchildren(part, -1)
f.write('</node>\n')
f.write('</map>\n')
f.close()
