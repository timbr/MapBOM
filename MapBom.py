#-------------------------------------------------------------------------------
# Name:        MapBom.py
# Version:     0.2.4
# Purpose:     Creates a Freemind mindmap file which shows a BOM structure
#
# Author:      tb126975
#
# Created:     03/12/2009
#
# Changes:    0.2.4: If quantity is A/R then this is printed instead of error-off
#                     0.2.3: Checks to see if Yaml file can be found. If not then uses a local copy
#                     0.2.2: Added Yaml file containing Ireland BOMs
#                     0.2.1: Development branch to investigate using SELECT IN statements
#                     0.2: Modified SQL query to include INVIA part numbers [now irrelevant]
#-------------------------------------------------------------------------------

from tim_modules import pysyteline
import string
import os
import datetime
import getopt, sys
import yaml

__VERSION__ = '0.2.4'

namedata={}
matdata={}

#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  MapBom %s - Create a BOM map
  -------------------------------------------------------
  Tim Browning 21/10/2009


  USAGE: %s <Top Assembly Number> [outputfile]

  Requires Freemind.

""" % (__VERSION__, sys.argv[0], ))


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


def CreateDictionary(part):
    if part[-1] != "'" and part[:1] != "'":
        part = "'" + part + "'" # The part number needs to be in inverted commas for the SQL query

    result = pysyteline.runquery(query(part))
    
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
        child_list=''
        for child in children[:-1]: # all child parts apart from the final one
            child_list += "'" + str(child) + "', "
            
        child_list += "'" + children[-1] + "'" # the final child in the list has no comma after it
        
        CreateDictionary(child_list)

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
            materialdesc = str(namedata[material])
            html = materialdesc.replace('&' , '&amp;').replace('"' , '&quot;')
            quant = str(pysyteline.clean_number(row[1], 3))
            if quant == '999.999':
                quant = 'A/R'
            else:
                quant = quant + '-off'
            line = str(row[0]) + '  ' + html + '  ' + quant
            #print line
            f.write('<node POSITION="right" TEXT="' + line + '"')
            next = findchildren(material, tab)
            if next != 'nochild':
                f.write('</node>\n')
    else:
        f.write('/>\n')
        return 'nochild'


if __name__ == '__main__':
    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",)
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    if  len(args) == 1:
        outputfile = "BOMmindmap.mm"
        part = args[0]
    elif len(args) == 2:
        part = args[0]
        outputfile = args[1]
        if outputfile[-3:] != ".mm":
            outputfile+=".mm"
    else:
        print "MapBOM version %s" % __VERSION__
        print "\n"
        print "Enter all or part of the top level assembly number:"
        part = raw_input()
        outputfile = "BOMmindmap.mm"


    item_num = 0

    command="""select DISTINCT
    rvxCurrentMaterials.Item,
    rvxCurrentMaterials.Description
    FROM UK_App.dbo.rvxCurrentMaterials
    WHERE rvxCurrentMaterials.Item like ?
    ORDER BY rvxCurrentMaterials.Item
    """

    item = '%' + part + '%'

    toplevel = pysyteline.runquery(command, item)

    if toplevel == []:
        print "\nPart %s doesn't exist in Syteline Current Materials." % (part)
        print "\nPress return to end script.\n"
        z=raw_input()
        sys.exit()

    if len(toplevel) > 1:
        print "\nMore than one top level item found:\n"
        for i, row in enumerate(toplevel):
            print "%i:  %s    %s" % (i, row.Item, row.Description)
        print "\nType number of item or press return to end script.\n"
        z=raw_input()
        try:
            item_num = int(z)
        except:
            sys.exit()


    print "\nCreating BOM mind map for %s    %s" % (toplevel[item_num].Item, toplevel[item_num].Description)

    print "\nDownloading data from Syteline."

    CreateDictionary(toplevel[item_num].Item)
    AddIrelandParts()

    f=open(outputfile, 'w')
    f.write('<map version="0.8.1">\n')
    f.write('<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->\n')
    findchildren(toplevel[item_num].Item, -1)
    f.write('</node>\n')
    f.write('</map>\n')
    f.close()

    print "\nMind Map file saved as %s" % (outputfile)
    print "\nOpening Mind Map"

    os.popen(outputfile)
