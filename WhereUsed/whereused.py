#-------------------------------------------------------------------------------
# Name:        WhereUsed.py
# Version:     0.1
# Purpose:     Creates a Freemind mindmap file which shows where the part is used
#
# Author:      tb126975
#
# Created:     21/10/2009
#
# Changes:   
#-------------------------------------------------------------------------------

from tim_modules import pysyteline
import string
import os
import datetime
import getopt, sys

__VERSION__ = '0.1'


#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  WhereUsed %s - Create a Where-Used map
  -------------------------------------------------------
  Tim Browning 22/10/2009


  USAGE: %s <Part Number> [outputfile]

  Requires Freemind.

""" % (__VERSION__, sys.argv[0], ))



def WhereUsed(part):
    desc = pysyteline.getitems(part)[0][1]
    timeformat = format = "%d-%m-%Y    %H:%M:%S"
    timenow = datetime.datetime.today().strftime(timeformat)
    part_text = part + '  ' + str(desc)
    date_text = 'As of: ' + timenow
    f.write('<node STYLE="fork" TEXT="WHERE USED:\n' + part_text + '\n' + date_text + '">\n')
    f.write('<edge WIDTH="thin"/>\n')
    result = pysyteline.whereused(part)
    if result != []:
        for row in result:
            material = str(row[0])
            materialdesc = str(row[1])
            html = string.replace(str(materialdesc), '&' , '&amp;')
            html2 = string.replace(html, '"' , '&quot;')
            line = str(row[0]) + '  ' + html2
            #print line
            f.write('<node POSITION="right" TEXT="' + line + '"')
            f.write('/>\n')
            #f.write('</node>\n')
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
        outputfile = "WUmindmap.mm"
        part = args[0]
    elif len(args) == 2:
        part = args[0]
        outputfile = args[1]
        if outputfile[-3:] != ".mm":
            outputfile+=".mm"
    else:
        print "WhereUsed version %s" % __VERSION__
        print "\n"
        print "Enter all or part of the part-number or assembly:"
        part = raw_input()
        outputfile = "WUmindmap.mm"


    item_num = 0

    item = '%' + part + '%'

    toplevel = pysyteline.getitems(item)

    if toplevel == []:
        print "\nPart %s doesn't exist in Syteline Current Materials." % (part)
        print "\nPress return to end script.\n"
        z=raw_input()
        sys.exit()

    if len(toplevel) > 1:
        print "\nMore than one item found:\n"
        for i, row in enumerate(toplevel):
            print "%i:  %s    %s" % (i, row.Item, row.Name)
        print "\nType number of item or press return to end script.\n"
        z=raw_input()
        try:
            item_num = int(z)
        except:
            sys.exit()


    print "\nCreating Where-Used mind map for %s    %s" % (toplevel[item_num].Item, toplevel[item_num].Name)

    print "\nDownloading data from Syteline."


    f=open(outputfile, 'w')
    f.write('<map version="0.8.1">\n')
    f.write('<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->\n')
    WhereUsed(toplevel[item_num].Item)
    f.write('</node>\n')
    f.write('</map>\n')
    f.close()

    print "\nMind Map file saved as %s" % (outputfile)
    print "\nOpening Mind Map"

    os.popen(outputfile)
