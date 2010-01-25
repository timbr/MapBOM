#-------------------------------------------------------------------------------
# Name:        ET_withIreland_MapBom.py
# Version:     0.2.6
# Purpose:     Creates a Freemind mindmap file which shows a BOM structure
#
# Author:      tb126975
#
# Created:     06/01/2010
#
# Changes:     0.2.6: Now uses MindMap class to write FreeMind xml file
#                     0.2.5: Added links to drawings on Sheffield
#                     0.2.4: If quantity is A/R then this is printed instead of error-off
#                     0.2.3: Checks to see if Yaml file can be found. If not then uses a local copy
#                     0.2.2: Added Yaml file containing Ireland BOMs
#                     0.2.1: Development branch to investigate using SELECT IN statements
#                     0.2: Modified SQL query to include INVIA part numbers [now irrelevant]
#-------------------------------------------------------------------------------

import pyodbc
import decimal
import os
import datetime
import getopt, sys
#import yaml
import glob
from classET import MindMap

__VERSION__ = '0.2.6'

namedata={}
matdata={}
drawingsdb = {}

drawingfilepaths = glob.glob('\\\\Sheffield\\SPD_Data\\Temporary\\TimBrowning\\Drawings\\*.pdf')

#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  MapBom %s - Create a BOM map
  -------------------------------------------------------
  Tim Browning 06/01/2009


  USAGE: %s <Top Assembly Number> [outputfile]

  Requires Freemind.

""" % (__VERSION__, sys.argv[0], ))


def ukquery(in_list):
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
    
def iequery(in_list):
    command="""select DISTINCT 
    rvxCurrentMaterials.Item, 
    rvxCurrentMaterials.Description, 
    rvxCurrentMaterials.Material, 
    rvxCurrentMaterials.\"Material Description\" as matdesc, 
    rvxCurrentMaterials.Quantity 
    FROM IE_App.dbo.rvxCurrentMaterials 
    WHERE rvxCurrentMaterials.Item in (%s) AND rvxCurrentMaterials.Material like '_-%%' 
    ORDER BY rvxCurrentMaterials.Material""" % in_list
    
    return command



def CreateDictionary(part):
    if part[-1] != "'" and part[:1] != "'":
        part = "'" + part + "'" # The part number needs to be in inverted commas for the SQL query

    result = runquery_uk(ukquery(part)) + runquery_ie(iequery(part))
    
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


def CreateDrawingsDB():
    for filepath in drawingfilepaths:
        filename = filepath.split('\\')[-1:][0]
        item = filename[1:15]
        filename = filename.replace('[', '%5B').replace(']', '%5D').replace(' ', '%20').replace('&', '&amp;')
        drawingsdb[item] = filename

def findchildren(part, mindmap):
    if part in matdata:
        result = matdata[part]
        mindmap.newgeneration()
        for row in result:
            material = str(row[0])
            materialdesc = str(namedata[material])
            quant = str(clean_number(row[1], 3))
            if quant == '999.999':
                quant = 'A/R'
            else:
                quant = '%s-off' % (quant)
            line = '%s  %s  %s' % (str(row[0]), materialdesc, quant)
            mindmap.addsibling(line)
            if drawingsdb.has_key(material):
                link = '//Sheffield/SPD_Data/Temporary/TimBrowning/Drawings/%s' % (drawingsdb[material])
                mindmap.addlink(link)
            next = findchildren(material, mindmap)
            if next != 'nochild':
                mindmap.previousgeneration()
    else:
        return 'nochild'

        
def runquery_uk(*args):
    """Runs an SQL query on the Syteline database

    First argument is the query string.
    Optional arguments are search string substitutions."""

    uksytelineconnection = \
    pyodbc.connect('DRIVER={SQL Server};SERVER=GBSYTELINEDB1;DATABASE=UK_App')
    
    cursor = uksytelineconnection.cursor()
    cursor.execute(*args)
    ukresults = [row for row in cursor]
    
    return ukresults
    
def runquery_ie(*args):
    """Runs an SQL query on the Syteline database

    First argument is the query string.
    Optional arguments are search string substitutions."""
    
    iesytelineconnection = \
    pyodbc.connect('DRIVER={SQL Server};SERVER=IESYTELINEDB1;DATABASE=IE_App')
    
    cursor = iesytelineconnection.cursor()
    cursor.execute(*args)
    ieresults = [row for row in cursor]
    
    return ieresults

        
def clean_number(number, decimal_places=2):
    """Quantizes decimal number

    If the number is an integer then the number is returned with no decimal
    places. If the number is a non-integer it is returned to decimal_places
    (default is 2 decimal places).

    If the 'number' sent is unicode text it is converted to Decimal then cleaned
    """

    decplaces = decimal.Decimal('10') ** -decimal_places

    if type(number) != decimal.Decimal:
        try:
            number = decimal.Decimal(number)
        except:
            return 'error' # can only deal with decimal types
    if number._isinteger() == True:
        return number.to_integral()
    elif number.is_zero() == True:
        return number.to_integral()
    else:
        return number.quantize(decplaces)


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

    ukcommand="""select DISTINCT
    rvxCurrentMaterials.Item,
    rvxCurrentMaterials.Description
    FROM UK_App.dbo.rvxCurrentMaterials
    WHERE rvxCurrentMaterials.Item like ?
    ORDER BY rvxCurrentMaterials.Item
    """
    
    iecommand="""select DISTINCT
    rvxCurrentMaterials.Item,
    rvxCurrentMaterials.Description
    FROM IE_App.dbo.rvxCurrentMaterials
    WHERE rvxCurrentMaterials.Item like ?
    ORDER BY rvxCurrentMaterials.Item
    """

    item = '%' + part + '%'

    toplevel = runquery_uk(ukcommand, item) + runquery_ie(iecommand, item)

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

    part_num = toplevel[item_num].Item
    part_desc = toplevel[item_num].Description
    print "\nCreating BOM mind map for %s    %s" % (part_num, part_desc)

    print "\nDownloading data from Syteline."

    CreateDictionary(part_num)
    #AddIrelandParts()
    CreateDrawingsDB()

    #desc = namedata[part_num]
    timeformat = format = "%d-%m-%Y    %H:%M:%S"
    timenow = datetime.datetime.today().strftime(timeformat)
    part_text = '%s  %s' % (part_num, str(part_desc))
    date_text = 'As of: %s' % (timenow)
    topnodetext = '%s\n%s' % (part_text, date_text)
    
    map = MindMap(outputfile)
    map.addtitle(topnodetext)
    
    findchildren(part_num, map)

    map.fold()
    map.write()

    print "\nMind Map file saved as %s" % (outputfile)
    print "\nOpening Mind Map"

    os.popen('FreemindPortable.bat ' + outputfile)
