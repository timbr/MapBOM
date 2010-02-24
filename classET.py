import xml.etree.ElementTree as ET


class MindMap:
    """Build a FreeMind xml file
    Creates an xml tree that can be read by the FreeMind mind-mapping

    software."""

    def __init__(self, *args):
        if len(args) > 0: # If a filename for the mindmap is given then this is used
            self.filename = args[0]
        else:
            self.filename = ''
            
        if len(args) == 2:
            self.version = args[1]
        else:
            self.version = '0.8.1'
            
        self.root = ET.Element('map') # Boilerplate at start of Freemind xml file
        self.root.set('version', self.version)
        self.comment = 'To view this file, download free mind mapping '\
        + 'software FreeMind from http://freemind.sourceforge.net'
        self.root.append(ET.Comment(self.comment))
		
        # Keep track of current position in the xml tree
        self.current_element =[]
        self.current_element.append(self.root)
        self.new_generation = False

        
        self.builtin_icons = ["help", "messagebox_warning", "idea", "button_ok",\
            "bookmark", "penguin", "licq", "button_cancel", "full-1", "full-2", "full-3",\
            "full-4", "full-5", "full-6", "full-7", "back", "forward", "attach", "ksmiletris",\
            "clanbomber", "desktop_new", "flag", "gohome", "kaddressbook", "knotify", "korn",\
            "Mail", "password", "pencil", "stop", "wizard", "xmag", "bell"]
        
        if self.version == '0.9.0':
            self.builtin_icons.extend (['yes', 'stop-sign', 'closed', 'info', 'full-8', 'full-9', 'full-0', \
            'prepare', 'go', 'up', 'down', 'smiley-neutral', 'smiley-oh', 'smiley-angry', 'smily_bad', \
            'folder', 'kmail', 'list', 'edit', 'freemind_butterfly', 'broken-line',  'calendar', 'clock', \
            'hourglass', 'launch', 'flag-black', 'flag-blue',  'flag-green', 'flag-orange', 'flag-pink', \
            'family', 'female1', 'female2', 'male1', 'male2', 'fema', 'group'])

    def addtitle(self, title):
        """Adds the central node to the mindmap"""
        
        self.topnode = ET.SubElement(self.root, 'node')
        self.topnode.set('STYLE', 'fork')
        self.topnode.set('TEXT', title)
        self.edgestyle = ET.SubElement(self.topnode, 'edge')
        self.edgestyle.set('WIDTH', 'thin')
        
        self.current_element.append(self.topnode)


    def addnode(self, parentelement, text):
        """Adds a node to the mindmap given the parent element instance"""
        
        child = ET.SubElement(parentelement, 'node')
        child.set('POSITION', 'right')
        child.set('TEXT', text)
        
        parent = -2 # position of current element's parent in current_element list
        if parentelement != self.current_element[parent]:
            self.current_element.append(child)
        else:
            self.current_element.pop()
            self.current_element.append(child)

            
    def addchild(self, text):
        """Adds a child node to the current node using the given text"""
        
        last_in_list = -1 # position of current element in current_element list
        self.addnode(self.current_element[last_in_list], text) # add a child to current element
        
        
    def addsibling(self, text):
        """Adds a sibling node to the current node using the given text"""
        
        parent = -2 # position of current element's parent in current_element list
        if self.new_generation == True:
            self.new_generation = False
            self.addchild(text)
        else:
            self.addnode(self.current_element[parent], text) # add a sibling to current element


    def addlink(self, link):
        """Appends a URL link to the node"""
        
        last_in_list = -1 # position of current element in current_element list
        element = self.current_element[last_in_list].set('LINK', link)


    def addicon(self, iconname):
        """Attaches a built-in icon to a node"""
        
        last_in_list = -1 # position of current element in current_element list
        if iconname not in self.builtin_icons:
            iconname = "messagebox_warning"
        icon = ET.SubElement(self.current_element[last_in_list], 'icon')
        icon.set('BUILTIN', iconname)


    def newgeneration(self):
        """Moves down a generation so the current node becomes a parent node"""
        
        self.new_generation = True


    def previousgeneration(self):
        """Moves up a generation so the parent node becomes the current node"""
        
        self.current_element.pop()


    def endbranch(self):
        """Carriage return!! Returns postion of parent node back to the title node"""

        self.current_element = self.current_element[:2]


    def fold(self, *args):
        """Collapses the mind map"""
		
        if len(args) > 0:
            element = args[0]
        else:
            element = self.topnode

        for subelement in element:
            if len(subelement.getchildren()) > 1:
                subelement.set('FOLDED', 'true')
            elif len(subelement.getchildren()) == 1: # if there is only one child, check that it is a node rather than an icon
                if subelement.getchildren()[0].tag == 'node':
                    subelement.set('FOLDED', 'true')
            self.fold(subelement)


    def write(self, filename='temp.mm'):
        """Writes the xml to a file

        A filename can be given either when the MindMap is
        initiated or specified when the write method is called.
        A filename in the write method has priority."""

        if self.filename == '':
            self.filename = filename
        elif filename != 'temp.mm':
            self.filename = filename
        self.tree = ET.ElementTree(self.root)
        self.tree.write(self.filename, 'utf-8')
