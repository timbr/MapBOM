import yaml
from tim_modules import pysyteline
import string
import os
import datetime
import getopt, sys

namedata={}
matdata={}

def AddIrelandParts():
    Ire_prefix = " **IRE**"
    yamlfile = "\\\\Sheffield\\SPD_Data\\Temporary\\TimBrowning\\IrelandBOMs\\IrelandBOM.yaml"
    try:
        yamldata = open(yamlfile, 'r').read()
    except:
        from IrelandBOM import yamldata
        print 'Using local copy of Ireland assembly data.'
    
    for assy in yaml.load_all(yamldata):
        namedata[assy['Assembly']] = assy['Description'] + Ire_prefix
        for part in assy['Items']:
            if part['Qty'] == 'A/R':
                qty = '999.999'
            else:
                qty = part['Qty']
            if part['Part Number'] not in namedata:
                namedata[part['Part Number']] = part['Description']
            if assy['Assembly'] not in matdata:
                matdata[assy['Assembly']] = [[part['Part Number'], qty]]
            else:
                matdata[assy['Assembly']].append([part['Part Number'], qty])

def findchildren(part,tab):
    if tab==-1:
        desc = namedata[part]
        timeformat = format = "%d-%m-%Y    %H:%M:%S"
        timenow = datetime.datetime.today().strftime(timeformat)
        part_text = part + '  ' + str(desc)
        date_text = 'As of: ' + timenow
        f.write('<node STYLE="fork" TEXT="' + part_text + '\n' + date_text + '">\n')
        f.write('<edge WIDTH="thin"/>\n')
    if part in matdata:
        result = matdata[part]
        if tab != -1:
            f.write(' FOLDED="true" >\n')
        tab+=1
        for row in result:
            material = str(row[0])
            materialdesc = namedata[material]
            html = string.replace(str(materialdesc), '&' , '&amp;')
            html2 = string.replace(html, '"' , '&quot;')
            quant = str(pysyteline.clean_number(row[1], 3))
            if quant == '999.999':
                quant = 'A/R'
            else:
                quant = quant + '-off'
            line = str(row[0]) + '  ' + html2 + '  ' + quant
            #print line
            f.write('<node POSITION="right" TEXT="' + line + '"')
            next = findchildren(material, tab)
            if next != 'nochild':
                f.write('</node>\n')
    else:
        f.write('/>\n')
        return 'nochild'

AddIrelandParts()

namedata['A-0000-0000-00'] = 'Ireland Parts'

yamlfile = "\\\\Sheffield\\SPD_Data\\Temporary\\TimBrowning\\IrelandBOMs\\IrelandBOM.yaml"
try:
    yamldata = open(yamlfile, 'r').read()
except:
    from IrelandBOM import yamldata
    print 'Using local copy of Ireland assembly data.'

matdata['A-0000-0000-00'] = []
for assy in yaml.load_all(yamldata):
    matdata['A-0000-0000-00'].append([assy['Assembly'], '0'])

outputfile = "BOMmindmap.mm"
f=open(outputfile, 'w')
f.write('<map version="0.8.1">\n')
f.write('<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->\n')
findchildren('A-0000-0000-00', -1)
f.write('</node>\n')
f.write('</map>\n')
f.close()

print "\nMind Map file saved as %s" % (outputfile)
print "\nOpening Mind Map"

os.popen(outputfile)
