import xml.etree.ElementTree as ET


class MindMap:
    """Build a FreeMind xml file
    Creates an xml tree that can be read by the FreeMind mind-mapping

    software."""

    def __init__(self, *args):
        self.root = ET.Element('map') # Boilerplate at start of Freemind xml file
        self.root.set('version', '0.8.1')
        self.comment = 'To view this file, download free mind mapping '\
        + 'software FreeMind from http://freemind.sourceforge.net'
        self.root.append(ET.Comment(self.comment))
		
        # Keep track of current position in the xml tree
        self.current_element = self.root
        self.parent_element = self.root
        self.grandfather_element = self.root

        if len(args) > 0: # If a filename for the mindmap is given then this is used
            self.filename = args[0]
        else:
            self.filename = ''


    builtin_icons = ["help", "messagebox_warning", "idea", "button_ok",\
        "bookmark", "penguin", "licq", "button_cancel", "full-1", "full-2", "full-3",\
        "full-4", "full-5", "full-6", "full-7", "back", "forward", "attach", "ksmiletris",\
        "clanbomber", "desktop_new", "flag", "gohome", "kaddressbook", "knotify", "korn",\
        "Mail", "password", "pencil", "stop", "wizard", "xmag", "bell"]


    def addtitle(self, title):
        """Adds the central node to the mindmap"""
        
        self.topnode = ET.SubElement(self.root, 'node')
        self.topnode.set('STYLE', 'fork')
        self.topnode.set('TEXT', title)
        self.edgestyle = ET.SubElement(self.topnode, 'edge')
        self.edgestyle.set('WIDTH', 'thin')
        
        self.updateposition(self.topnode, self.topnode)


    def addnode(self, parentelement, text):
        """Adds a node to the mindmap given the parent element instance"""
        
        child = ET.SubElement(parentelement, 'node')
        child.set('POSITION', 'right')
        child.set('TEXT', text)
        self.updateposition(child, parentelement)

        
    def updateposition(self, currentelement, parentelement):
        """Refreshes the stored position in the xml tree
    
        This is so that a new node can be added in the correct place"""
        
        if parentelement != self.parent_element:
            self.grandfather_element = self.parent_element
        self.current_element = currentelement
        self.parent_element = parentelement

        
    def addchild(self, text):
        """Adds a child node to the current node using the given text"""
        
        self.addnode(self.current_element, text) # add a child to current element

        
    def addsibling(self, text):
        """Adds a sibling node to the current node using the given text"""
        
        self.addnode(self.parent_element, text) # add a sibling to current element


    def addlink(self, link):
        """Appends a URL link to the node"""

        self.current_element.set('LINK', link)


    def addicon(self, iconname):
        """Attaches a built-in icon to a node"""

        if iconname not in self.builtin_icons:
            iconname = "messagebox_warning"
        icon = ET.SubElement(self.current_element, 'icon')
        icon.set('BUILTIN', iconname)


    def newgeneration(self):
        """Moves down a generation so the current node becomes a parent node"""
        
        self.updateposition(self.current_element, self.current_element)


    def previousgeneration(self):
        """Moves up a generation so the parent node becomes the current node"""
        
        self.updateposition(self.parent_element, self.grandfather_element)


    def endbranch(self):
        """Carriage return!! Returns postion of parent node back to the title node"""

        self.updateposition(self.topnode, self.topnode)


    def fold(self, *args):
        """Collapses the mind map"""
		
        if len(args) > 0:
            element = args[0]
        else:
            element = self.topnode

        for subelement in element:
            if len(subelement.getchildren()) > 0:
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
        self.tree.write(self.filename)
