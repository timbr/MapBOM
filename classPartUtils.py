import pyodbc
import decimal
import os
import datetime
import glob
from classET import MindMap

class PartUtils:
    """Part utliities class"""
    
    def __init__(self, *args):
        self.namedata={}
        self.matdata={}
        self.drawingsdb = {}
        self.WILinksdb = {}
        
        self.ireland_assys=[]
        
        self.part_num = ''
        self.filename = 'temp.mm'
        
        self.uksytelineconnection = \
        pyodbc.connect('DRIVER={SQL Server};SERVER=GBSYTELINEDB1;DATABASE=UK_App')
        
        self.iesytelineconnection = \
        pyodbc.connect('DRIVER={SQL Server};SERVER=IESYTELINEDB1;DATABASE=IE_App')
        
        self.ukCurrentMaterialsdb = 'UK_App.dbo.rvxCurrentMaterials'
        self.ieCurrentMaterialsdb = 'IE_App.dbo.rvxCurrentMaterials'
        self.ukItemsdb = 'UK_App.dbo.rvxItems'
        self.ieItemsdb = 'IE_App.dbo.rvxItems'
        
                
        self.include_ireland_data = True
        self.include_drawings = False
        self.include_DWGdrawings = False
        self.include_part_costs = True
        self.include_WI_Links = False
        
        if len(args) > 0: # A partnumber can be given as an argument
            if self.valid_partnumber(args[0]):
                self.part_num = args[0]
            else:
                print 'Not a valid part number'
        
        
    def valid_partnumber(self, partnum):
            
        if len(self.findpartslike(partnum)) == 1:
            return True
        else:
            return False
            
            
    def findpartslike(self, partnum):
        result = self.runquery("%"+partnum+"%", searchtype = 'itemdesc', column = 'Item')
        #result += self.runquery("%"+partnum+"%", searchtype = 'itemdesc', column = 'Material')
        return result
        
        
    def query(self, db, in_list, searchtype='bom', column = 'Item'):
        if searchtype == 'bom':
            command="""select DISTINCT 
            %(database)s.Item, 
            %(database)s.Description, 
            %(database)s.Material, 
            %(database)s.Cost as matcost,
            %(database)s.\"Material Description\" as matdesc, 
            %(database)s.Quantity 
            FROM %(database)s 
            WHERE %(database)s.Item in (%(item_list)s) AND %(database)s.Material not like 'R-%%' 
            ORDER BY %(database)s.Material""" % {'database': db, 'item_list': in_list}

            return command
            
        elif searchtype == 'itemdesc':
            command="""select DISTINCT 
            %(database)s.Item, 
            %(database)s.Description
            FROM %(database)s 
            WHERE %(database)s.%(Column)s like '%(item_list)s'
            ORDER BY %(database)s.Item""" % {'database': db, 'Column': column, 'item_list': in_list}
            return command
            
        elif searchtype == 'matdesc':
            command="""select DISTINCT 
            %(database)s.Material,
            %(database)s.\"Material Description\" as matdesc
            FROM %(database)s 
            WHERE %(database)s.%(Column)s like '%(item_list)s'
            ORDER BY %(database)s.Material""" % {'database': db, 'Column': column, 'item_list': in_list}
            return command
        
        elif searchtype == 'partcost':
            command="""select 
            %(database)s.\"Unit Cost\" as itemcost
            FROM %(database)s 
            WHERE %(database)s.%(Column)s like '%(item_list)s'
            ORDER BY %(database)s.Item""" % {'database': db, 'Column': column, 'item_list': in_list}
            return command
        
        
    def CreateDrawingsDB(self):
        drawingfilepaths = glob.glob('\\\\Sheffield\\SPD_Data\\Temporary\\MapBom\\Drawings\\*.pdf')
        drawingfilepaths += glob.glob('C:\\Program Files\\MapBom\\Drawings\\*.pdf')
        
        for filepath in drawingfilepaths:
            filename = filepath.split('\\')[-1:][0]
            item = filename[1:15]
            #filename = filename.replace('[', '%5B').replace(']', '%5D').replace(' ', '%20').replace('&', '&amp;')
            self.drawingsdb[item] = filepath
            
            
    def CreateDWGDrawingsDB(self):
        DWGdrawings = glob.glob('\\\\Sheffield\\SPD_Data\\_SPD Drawings\\1.1.Issued (DIN)\\*\\*.dwg')
        
        for filepath in DWGdrawings:
            filename = filepath.split('\\')[-1:][0]
            item = filename[:14]
            #filename = filename.replace('[', '%5B').replace(']', '%5D').replace(' ', '%20').replace('&', '&amp;')
            self.drawingsdb[item] = filepath
            
    def CreateWILinksDB(self):
        WILinks = glob.glob('\\\\Sheffield\\SPD_Data\\Production\\Production_ Documents\\Work_Instructions\\WI Issued\\*')
        
        for filepath in WILinks:
            filename = filepath.split('\\')[-1:][0]
            item = filename[:11]
            #filename = filename.replace('[', '%5B').replace(']', '%5D').replace(' ', '%20').replace('&', '&amp;')
            self.WILinksdb[item] = filepath
            
            
    def runquery(self, parts, searchtype = 'bom', column = 'Item'):
         """Runs an SQL query on the Syteline database"""
         
         cursor = self.uksytelineconnection.cursor()
         cursor.execute(self.query(self.ukCurrentMaterialsdb, parts, searchtype, column))
         results = [row for row in cursor]
         
         if self.include_ireland_data == True:
             cursor = self.iesytelineconnection.cursor()
             cursor.execute(self.query(self.ieCurrentMaterialsdb, parts, searchtype, column))
             ireland_results = [row for row in cursor]
             for row in ireland_results:
                 self.ireland_assys.append(row[0])
             results += ireland_results
    
         return results
     
    def runpartscostquery(self, parts, searchtype = 'partscost', column = 'Item'):
         """Runs an SQL query on the Syteline database"""
         
         cursor = self.uksytelineconnection.cursor()
         cursor.execute(self.query(self.ukItemsdb, parts, searchtype, column))
         results = [row for row in cursor]
         
         if self.include_ireland_data == True:
             cursor = self.iesytelineconnection.cursor()
             cursor.execute(self.query(self.ieItemsdb, parts, searchtype, column))
             ireland_results = [row for row in cursor]
             for row in ireland_results:
                 self.ireland_assys.append(row[0])
             results += ireland_results
    
         return results
        
        
    def clean_number(self, number, decimal_places=2):
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
            
            
    def CreateDictionary(self, part):
        if part[-1] != "'" and part[:1] != "'":
            part = "'" + part + "'" # The part number needs to be in inverted commas for the SQL query

        result = self.runquery(part)
    
        if result != []:
            for row in result:
                if row.Item not in self.namedata:
                    self.namedata[row.Item] = row.Description
                if row.Material not in self.namedata:
                    self.namedata[row.Material] = row.matdesc
                
            for row in result:
                if row.Item not in self.matdata:
                    self.matdata[row.Item] = [[row.Material, row.Quantity, row.matcost]]
                else:
                    self.matdata[row.Item].append([row.Material, row.Quantity, row.matcost])

        
            children = [child.Material for child in result]
            child_list=''
            for child in children[:-1]: # all child parts apart from the final one
                child_list += "'" + str(child) + "', "
            
            child_list += "'" + children[-1] + "'" # the final child in the list has no comma after it
        
            self.CreateDictionary(child_list)
            
            
    def findchildren(self, part, mindmap):
        if part in self.matdata:
            result = self.matdata[part]
            mindmap.newgeneration()
            for row in result:
                material = str(row[0])
                materialdesc = str(self.namedata[material])
                quant = self.clean_number(row[1], 3)
                cost = self.clean_number(row[2], 0)
                if self.include_part_costs == True:
                    totalcost = str(cost * quant)
                    line = '%s  %s %s-off, Cost: %s' % (str(row[0]), materialdesc, str(quant), totalcost)
                else:
                    line = '%s  %s  %s-off' % (str(row[0]), materialdesc, str(quant))
                mindmap.addsibling(line)
                if self.drawingsdb.has_key(material):
                    link = '%s' % (self.drawingsdb[material])
                    mindmap.addlink(link)
                if self.WILinksdb.has_key(material):
                    link = '%s' % (self.WILinksdb[material])
                    mindmap.addlink(link)
                if str(row[0]) in self.ireland_assys:
                    mindmap.addicon('flag')
                next = self.findchildren(material, mindmap)
                if next != 'nochild':
                    mindmap.previousgeneration()
        else:
            return 'nochild'
           
           
    def generateBOMmap(self):
        if self.valid_partnumber(self.part_num) == False:
            print "No valid part number specified"
            return
            
        part_desc = self.runquery("%"+self.part_num+"%", searchtype = 'itemdesc')[0].Description
            
        self.CreateDictionary(self.part_num)
        
        if self.include_DWGdrawings == True:
            self.CreateDWGDrawingsDB()
        
        if self.include_drawings == True: # Any existing dwg files will be overwritten in the db if a pdf has the same assy number
            self.CreateDrawingsDB()
            
        if self.include_WI_Links == True:
            self.CreateWILinksDB()
    
        timeformat = format = "%d-%m-%Y    %H:%M:%S"
        timenow = datetime.datetime.today().strftime(timeformat)
        part_text = '%s  %s' % (self.part_num, str(part_desc))
        date_text = 'As of: %s' % (timenow)
        getcost = self.runpartscostquery("%"+self.part_num+"%", searchtype = 'partcost', column = 'Item')[0].itemcost
        print getcost
        cost = str(self.clean_number(getcost, 0))
        print cost
        if self.include_part_costs == True:
            topnodetext = '%s  Cost: %s\n%s' % (part_text, cost, date_text)
        else:
            topnodetext = '%s\n%s' % (part_text, date_text)
    
        mindmap = MindMap(self.filename)
        mindmap.addtitle(topnodetext)
        
        self.findchildren(self.part_num, mindmap)
        
        mindmap.fold()
        mindmap.write()
        
        
    def generateWhereUsedmap(self):
        part_desc = self.runquery("%"+self.part_num+"%", searchtype = 'matdesc', column = 'Material')[0].matdesc
        if len(part_desc) == 0:
            print "No valid part number specified"
            return
        #part_desc = self.runquery("%"+self.part_num+"%", searchtype = 'itemdesc')[0].Description
        
        if self.include_drawings == True:
            self.CreateDrawingsDB()
            
        timeformat = format = "%d-%m-%Y    %H:%M:%S"
        timenow = datetime.datetime.today().strftime(timeformat)
        part_text = 'WHERE USED: %s  %s' % (self.part_num, str(part_desc))
        date_text = 'As of: %s' % (timenow)
        topnodetext = '%s\n%s' % (part_text, date_text)
        
        mindmap = MindMap(self.filename)
        mindmap.addtitle(topnodetext)
        mindmap.newgeneration()
        
        result = self.runquery(self.part_num, searchtype = 'itemdesc', column = 'Material')
        if result != []:
            for row in result:
                material = str(row[0])
                materialdesc = str(row[1])
                line = '%s  %s' % (str(row[0]), materialdesc)
                mindmap.addsibling(line)
                if self.drawingsdb.has_key(material):
                    link = '//Sheffield/SPD_Data/Temporary/TimBrowning/Drawings/%s' % (self.drawingsdb[material])
                    mindmap.addlink(link)
        else:
            return 'No Parents Found'
            
        mindmap.fold()
        mindmap.write()
        