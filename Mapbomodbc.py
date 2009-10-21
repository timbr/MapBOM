import pyodbc
import string

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GBSYTELINEDB1;DATABASE=UK_App;Trusted_Connection=Yes')

cursor = cnxn.cursor()

command="""select DISTINCT
rvxCurrentMaterials.Item,
rvxCurrentMaterials.Description,
rvxCurrentMaterials.Material,
rvxCurrentMaterials.\"Material Description\" as matdesc,
rvxCurrentMaterials.Quantity 
FROM UK_App.dbo.rvxCurrentMaterials
WHERE rvxCurrentMaterials.Item=? AND rvxCurrentMaterials.Material like '_-%'
ORDER BY rvxCurrentMaterials.Material
"""

f=open('outputodbc.mm', 'w')

def findchildren(part,tab):
    print part
    if tab==-1:
        cursor.execute("select distinct rvxCurrentMaterials.Description from UK_App.dbo.rvxCurrentMaterials where rvxCurrentMaterials.Item=?", part)
        desc = cursor.fetchone()
        f.write('<node STYLE="fork" TEXT="' + part + '  ' + desc.Description + '">\n')
        f.write('<edge WIDTH="thin"/>\n')
    cursor.execute(command, part)
    result = cursor.fetchall()
    if result != []:
        if tab != -1:
            f.write('>\n')
        tab+=1
        for row in result:
            html = string.replace(row.matdesc, '&' , '&amp;')
            html2 = string.replace(html, '"' , '&quot;')
            quant=int(row.Quantity)
            line = row.Material + '  ' + html2 + '  ' + str(quant) + '-off'
            #if tab < 0:
            #    f.write('<node POSITION="right" TEXT="' + line + '"')
            #else:
            #    f.write('<node POSITION="right" FOLDED="true" TEXT="' + line + '"')
            f.write('<node POSITION="right" TEXT="' + line + '"')
            next = findchildren(row.Material,tab)
            if next != 'nochild':
                f.write('</node>\n')
    else:
        f.write('/>\n')
        return 'nochild'


part ='A-9836-3294-01'
f.write('<map version="0.8.1">\n')
f.write('<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->\n')
findchildren(part,-1)
f.write('</node>\n')
f.write('</map>\n')
f.close()
