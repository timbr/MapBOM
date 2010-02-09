#!/usr/bin/env python
#Boa:App:BoaApp
#-------------------------------------------------------------------------------
# Name:        MapBom.py
# Version:     0.3
# Purpose:     Creates a Freemind mindmap file which shows a BOM structure
#
# Author:      tb126975
#
# Created:     09/02/2010
#
#Changes      0.3: GUI version!!
#             0.2.7: PartUtils class written and used to generate BOM map (includes Ireland Syteline data)
#             0.2.6: Now uses MindMap class to write FreeMind xml file
#             0.2.5: Added links to drawings on Sheffield
#             0.2.4: If quantity is A/R then this is printed instead of error-off
#             0.2.3: Checks to see if Yaml file can be found. If not then uses a local copy
#             0.2.2: Added Yaml file containing Ireland BOMs
#             0.2.1: Development branch to investigate using SELECT IN statements
#             0.2: Modified SQL query to include INVIA part numbers [now irrelevant]
#-------------------------------------------------------------------------------

import wx
import MapBomFrame

__VERSION__ = '0.3'


modules ={u'MapBomFrame': [1, 'Main frame of Application', u'MapBomFrame.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = MapBomFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()


if __name__ == '__main__':
    main()