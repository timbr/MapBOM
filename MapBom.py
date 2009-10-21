#-------------------------------------------------------------------------------
# Name:        MapBom.py
# Version:     0.2.1
# Purpose:     Creates a Freemind mindmap file which shows a BOM structure
#
# Author:      tb126975
#
# Created:     21/10/2009
#
# Changes:     0.2.1: Development branch to investigate using SELECT IN statements
#                     0.2: Modified SQL query to include INVIA part numbers
#-------------------------------------------------------------------------------

from tim_modules import pysyteline
import string
import os
import datetime
import getopt, sys



namedata={}
matdata={}

#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  BomMap 0.2.1 - Create a BOM map
  -------------------------------------------------------
  Tim Browning 21/10/2009


  USAGE: %s <Top Assembly Number> [outputfile]

  Requires Freemind.

""" % (sys.argv[0], ))



def createdictionary():
    command="""select DISTINCT
    rvxCurrentMaterials.Item,
    rvxCurrentMaterials.Description,
    rvxCurrentMaterials.Material,
    rvxCurrentMaterials.\"Material Description\" as matdesc,
    rvxCurrentMaterials.Quantity
    FROM UK_App.dbo.rvxCurrentMaterials
    WHERE (rvxCurrentMaterials.Item like '_-%' OR rvxCurrentMaterials.Item like 'INVIA%')
    AND rvxCurrentMaterials.Material like '_-%'
    ORDER BY rvxCurrentMaterials.Material
    """

    sqlresult = pysyteline.runquery(command)
    print 'Creating names dictionary...'
    for row in sqlresult:
        if row.Item not in namedata:
            namedata[row.Item] = row.Description
        if row.Material not in namedata:
            namedata[row.Material] = row.matdesc

    print 'Creating material dictionary...'
    for row in sqlresult:
        if row.Item not in matdata:
            matdata[row.Item] = [[row.Material, row.Quantity]]
        else:
            matdata[row.Item].append([row.Material, row.Quantity])



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

    createdictionary()

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
