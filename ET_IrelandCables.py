import yaml
from tim_modules.pysyteline import clean_number
import os
import datetime
import getopt, sys
from classET import MindMap

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

def findchildren(part, mindmap):
    if part in matdata:
        result = matdata[part]
        mindmap.newgeneration()
        for row in result:
            material = str(row[0])
            materialdesc = namedata[material]
            quant = str(clean_number(row[1], 3))
            if quant == '999.999':
                quant = 'A/R'
            else:
                quant = '%s-off' % (quant)
            line = '%s  %s  %s' % (str(row[0]), materialdesc, quant)
            mindmap.addsibling(line)
            next = findchildren(material, mindmap)
            if next != 'nochild':
                mindmap.previousgeneration()
    else:
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

	
part = 'A-0000-0000-00'

desc = namedata[part]
timeformat = format = "%d-%m-%Y    %H:%M:%S"
timenow = datetime.datetime.today().strftime(timeformat)
part_text = '%s  %s' % (part, str(desc))
date_text = 'As of: %s' % (timenow)
topnodetext = '%s\n%s' % (part_text, date_text)

outputfile = "BOMmindmap.mm"

map = MindMap(outputfile)
map.addtitle(topnodetext)

findchildren(part, map)

map.fold()
map.write()

print "\nMind Map file saved as %s" % (outputfile)
print "\nOpening Mind Map"

os.popen(outputfile)
