import xml.etree.ElementTree as ET

# A potential problem with this script is that it locates the position in the tree based on the text.
# If there is duplication of the text in different leaves this could cause problems
# I need to investigate if it is possible to pass the current element id or even its instance.

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

        # The current position in the mind map is  logged here based on the text		
        self.text_at_current_position = ''
        self.text_at_parent = ''
        self.text_at_previous_parent = ''

        if len(args) > 0:
            self.filename = args[0]
        else:
            self.filename = ''

    def addtitle(self, title):
        self.title = title
        self.topnode = ET.SubElement(self.root, 'node')
        self.topnode.set('STYLE', 'fork')
        self.topnode.set('TEXT', self.title)

        self.edgestyle = ET.SubElement(self.topnode, 'edge')
        self.edgestyle.set('WIDTH', 'thin')

        self.text_at_current_position = title

    def addchild(self, text):
        self.addchildbyparentname(text, self.text_at_current_position)

    def addsibling(self, text):
        self.addchildbyparentname(text, self.text_at_parent)
		
    def newgeneration(self):
        if self.text_at_current_position != '':
            self.text_at_previous_parent = self.text_at_parent
            self.text_at_parent = self.text_at_current_position

    def previousgeneration(self):
        self.text_at_current_postion = self.text_at_parent
        self.text_at_parent = self.text_at_previous_parent

    def endbranch(self):
        self.text_at_parent = self.title
        self.text_at_current_position = ''

    def addchildbyparentname(self, data, parent = ''):
        if parent == '':
            parent = self.title
        self.findnode(parent, data, self.root)

    def textfound(self, text, element):
        if element.attrib.has_key('TEXT'):
            if element.attrib['TEXT'] == text:
                return True
		
    def findnode(self, text, data, element):
        if self.textfound(text, element) == True:
            child = ET.SubElement(subelement, 'node')
            child.set('POSITION', 'right')
            child.set('TEXT', data)
            return element
        for subelement in element:
            if self.textfound(text, subelement) == True:
                child = ET.SubElement(subelement, 'node')
                child.set('POSITION', 'right')
                child.set('TEXT', data)
                self.text_at_current_position = data
                self.text_at_parent = text
                return subelement
            self.findnode(text, data, subelement)


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