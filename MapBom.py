#-------------------------------------------------------------------------------
# Name:        MapBom.py
# Version:     0.2.7
# Purpose:     Creates a Freemind mindmap file which shows a BOM structure
#
# Author:      tb126975
#
# Created:     26/01/2010
#
# Changes:    0.2.7: PartUtils class written and used to generate BOM map (includes Ireland Syteline data)
#                     0.2.6: Now uses MindMap class to write FreeMind xml file
#                     0.2.5: Added links to drawings on Sheffield
#                     0.2.4: If quantity is A/R then this is printed instead of error-off
#                     0.2.3: Checks to see if Yaml file can be found. If not then uses a local copy
#                     0.2.2: Added Yaml file containing Ireland BOMs
#                     0.2.1: Development branch to investigate using SELECT IN statements
#                     0.2: Modified SQL query to include INVIA part numbers [now irrelevant]
#-------------------------------------------------------------------------------

import getopt, sys, os
from classPartUtils import PartUtils

__VERSION__ = '0.2.7'


#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  MapBom %s - Create a BOM map
  -------------------------------------------------------
  Tim Browning 26/01/2010


  USAGE: %s <Top Assembly Number> [outputfile]

  Requires Freemind.

""" % (__VERSION__, sys.argv[0], ))


if __name__ == '__main__':
    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",)
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    if  len(args) == 1:
        outputfile = "C:\\Program Files\\MapBom\\BOMmindmap.mm"
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
        outputfile = "C:\\Program Files\\MapBom\\BOMmindmap.mm"
        
        include_ireland = False
        print "Would you like to include Ireland Syteline in the search?\n(This sometimes results in a large delay)\nY/N?"
        response = raw_input()
        if response.upper() == "Y" or response.upper() == 'YES':
            print "\n=====> Including Ireland Syteline data"
            include_ireland = True

    item = '%' + part + '%'

    mapbom = PartUtils()
    mapbom.include_ireland_data = include_ireland
    
    toplevel = mapbom.findpartslike(item)
    #toplevel = runquery_uk(ukcommand, item) + runquery_ie(iecommand, item)

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
    else:
        item_num = 0 # There is only one part that matches

    part_num = toplevel[item_num].Item
    part_desc = toplevel[item_num].Description

    print "\nCreating BOM mind map for %s    %s" % (part_num, part_desc)

    print "\nDownloading data from Syteline."

    mapbom.part_num = part_num
    mapbom.filename = outputfile
    mapbom.generateBOMmap()

    print "\nMind Map file saved as %s" % (outputfile)
    print "\nOpening Mind Map"

    os.popen('FreemindPortable.bat ' + outputfile)
