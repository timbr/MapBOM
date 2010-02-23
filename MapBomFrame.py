#Boa:Frame:Frame1

import wx
import wx.lib.buttons
import wx.lib.hyperlink
from classPartUtils import PartUtils
import os

mapbom = PartUtils()

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON_CREATEBOM, wxID_FRAME1BUTTON_OK, 
 wxID_FRAME1CHECKBOX_DWG_DRAWINGS, wxID_FRAME1CHECKBOX_IRISH, 
 wxID_FRAME1CHECKBOX_PART_COSTS, wxID_FRAME1CHECKBOX_PDF_DRAWINGS, 
 wxID_FRAME1HYPERLINKCTRL_DWG, wxID_FRAME1HYPERLINKCTRL_IRISH, 
 wxID_FRAME1HYPERLINKCTRL_PART_COST, wxID_FRAME1HYPERLINKCTRL_PDF, 
 wxID_FRAME1LISTCTRL1, wxID_FRAME1STATICBOXBOM, wxID_FRAME1STATICBOXMESSAGES, 
 wxID_FRAME1STATICBOXOPTIONS, wxID_FRAME1TEXTCTRLMESSAGES, 
 wxID_FRAME1TEXTCTRL_PART_NUM, 
] = [wx.NewId() for _init_ctrls in range(17)]

class Frame1(wx.Frame):
    def _init_coll_listCtrl1_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Part Number', width=100)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Name',
              width=248)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(462, 265), size=wx.Size(422, 465),
              style=wx.SIMPLE_BORDER | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU,
              title='MapBOM GUI')
        self.SetClientSize(wx.Size(414, 438))
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        self.SetBackgroundColour(wx.Colour(212, 208, 200))
        self.SetThemeEnabled(False)

        self.textCtrl_part_num = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL_PART_NUM,
              name='textCtrl_part_num', parent=self, pos=wx.Point(24, 40),
              size=wx.Size(120, 24), style=0, value='Enter Assy Number')
        self.textCtrl_part_num.Bind(wx.EVT_TEXT_ENTER,
              self.OnTextCtrl_part_numTextEnter,
              id=wxID_FRAME1TEXTCTRL_PART_NUM)

        self.button_OK = wx.Button(id=wxID_FRAME1BUTTON_OK, label='OK',
              name='button_OK', parent=self, pos=wx.Point(168, 40),
              size=wx.Size(32, 23), style=0)
        self.button_OK.Bind(wx.EVT_BUTTON, self.OnButton_OKButton,
              id=wxID_FRAME1BUTTON_OK)

        self.button_CreateBOM = wx.Button(id=wxID_FRAME1BUTTON_CREATEBOM,
              label='Create BOM Mindmap', name='button_CreateBOM', parent=self,
              pos=wx.Point(272, 248), size=wx.Size(112, 23), style=0)
        self.button_CreateBOM.Show(False)
        self.button_CreateBOM.Bind(wx.EVT_BUTTON, self.OnButton_CreateBOMButton,
              id=wxID_FRAME1BUTTON_CREATEBOM)

        self.listCtrl1 = wx.ListCtrl(id=wxID_FRAME1LISTCTRL1, name='listCtrl1',
              parent=self, pos=wx.Point(24, 80), size=wx.Size(368, 144),
              style=wx.LC_REPORT)
        self.listCtrl1.Show(True)
        self.listCtrl1.Enable(False)
        self._init_coll_listCtrl1_Columns(self.listCtrl1)
        self.listCtrl1.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
              self.OnListCtrl1ListItemActivated, id=wxID_FRAME1LISTCTRL1)

        self.checkBox_Irish = wx.CheckBox(id=wxID_FRAME1CHECKBOX_IRISH,
              label='Search Ireland Syteline', name='checkBox_Irish',
              parent=self, pos=wx.Point(16, 328), size=wx.Size(128, 13),
              style=0)
        self.checkBox_Irish.SetValue(True)
        self.checkBox_Irish.SetToolTipString('Search Ireland Syteline')
        self.checkBox_Irish.Bind(wx.EVT_CHECKBOX, self.OnCheckBox_IrishCheckbox,
              id=wxID_FRAME1CHECKBOX_IRISH)

        self.checkBox_pdf_drawings = wx.CheckBox(id=wxID_FRAME1CHECKBOX_PDF_DRAWINGS,
              label='Add links to pdf drawings', name='checkBox_pdf_drawings',
              parent=self, pos=wx.Point(16, 352), size=wx.Size(144, 13),
              style=0)
        self.checkBox_pdf_drawings.SetValue(False)
        self.checkBox_pdf_drawings.SetToolTipString('Add links to pdf drawings')
        self.checkBox_pdf_drawings.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBox_pdf_drawingsCheckbox,
              id=wxID_FRAME1CHECKBOX_PDF_DRAWINGS)

        self.checkBox_dwg_drawings = wx.CheckBox(id=wxID_FRAME1CHECKBOX_DWG_DRAWINGS,
              label='Add links to dwg drawings', name='checkBox_dwg_drawings',
              parent=self, pos=wx.Point(16, 376), size=wx.Size(144, 13),
              style=0)
        self.checkBox_dwg_drawings.SetValue(False)
        self.checkBox_dwg_drawings.SetToolTipString('Add links to dwg drawings')
        self.checkBox_dwg_drawings.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBox_dwg_drawingsCheckbox,
              id=wxID_FRAME1CHECKBOX_DWG_DRAWINGS)

        self.staticBoxBOM = wx.StaticBox(id=wxID_FRAME1STATICBOXBOM,
              label='Part Search', name='staticBoxBOM', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(400, 232), style=0)

        self.staticBoxOptions = wx.StaticBox(id=wxID_FRAME1STATICBOXOPTIONS,
              label='Options', name='staticBoxOptions', parent=self,
              pos=wx.Point(8, 304), size=wx.Size(168, 128), style=0)

        self.staticBoxMessages = wx.StaticBox(id=wxID_FRAME1STATICBOXMESSAGES,
              label='Messages', name='staticBoxMessages', parent=self,
              pos=wx.Point(192, 304), size=wx.Size(216, 100), style=0)

        self.textCtrlMessages = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLMESSAGES,
              name='textCtrlMessages', parent=self, pos=wx.Point(200, 328),
              size=wx.Size(200, 64), style=wx.TE_MULTILINE, value='')
        self.textCtrlMessages.SetEditable(True)
        self.textCtrlMessages.SetInsertionPoint(2)

        self.hyperLinkCtrl_Irish = wx.lib.hyperlink.HyperLinkCtrl(id=wxID_FRAME1HYPERLINKCTRL_IRISH,
              label='?', name='hyperLinkCtrl_Irish', parent=self,
              pos=wx.Point(165, 327), size=wx.Size(5, 13), style=0)

        self.hyperLinkCtrl_pdf = wx.lib.hyperlink.HyperLinkCtrl(id=wxID_FRAME1HYPERLINKCTRL_PDF,
              label='?', name='hyperLinkCtrl_pdf', parent=self,
              pos=wx.Point(165, 352), size=wx.Size(5, 13), style=0)

        self.hyperLinkCtrl_dwg = wx.lib.hyperlink.HyperLinkCtrl(id=wxID_FRAME1HYPERLINKCTRL_DWG,
              label='?', name='hyperLinkCtrl_dwg', parent=self,
              pos=wx.Point(165, 376), size=wx.Size(5, 13), style=0)

        self.checkBox_part_costs = wx.CheckBox(id=wxID_FRAME1CHECKBOX_PART_COSTS,
              label='Display Part Costs', name='checkBox_part_costs',
              parent=self, pos=wx.Point(16, 400), size=wx.Size(112, 16),
              style=0)
        self.checkBox_part_costs.SetValue(True)
        self.checkBox_part_costs.SetToolTipString('Display parts costs')
        self.checkBox_part_costs.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBox_part_costsCheckbox,
              id=wxID_FRAME1CHECKBOX_PART_COSTS)

        self.hyperLinkCtrl_part_cost = wx.lib.hyperlink.HyperLinkCtrl(id=wxID_FRAME1HYPERLINKCTRL_PART_COST,
              label='?', name='hyperLinkCtrl_part_cost', parent=self,
              pos=wx.Point(165, 400), size=wx.Size(5, 13), style=0)

    def __init__(self, parent):
        from MapBom import __VERSION__
        self._init_ctrls(parent)
        self.SetTitle('MapBom GUI v%s' % (__VERSION__))
        
        ib = wx.IconBundle()
        ib.AddIconFromFile("mapbom.ico", wx.BITMAP_TYPE_ANY)
        self.SetIcons(ib)
        
        self.InitialiseHyperlinks()

    def OnTextCtrl_part_numTextEnter(self, event):
        self.FindPart()

    def OnButton_OKButton(self, event):
        self.FindPart()

    def OnCheckBox_IrishCheckbox(self, event):
        mapbom.include_ireland_data = self.checkBox_Irish.Value

        
    def generateBOMmindmap(self, partnum):
        self.textCtrlMessages.AppendText('\nCreating BOM Mindmap for %s\n\n' % (partnum))
        mapbom.part_num = partnum
        outputfile = "C:\\Program Files\\MapBom\\BOMmindmap.mm"
        mapbom.filename = outputfile
        mapbom.generateBOMmap()
        self.textCtrlMessages.AppendText('\nMindmap created for %s\n\n' % (partnum))
        os.popen('FreemindPortable.bat ' + outputfile)
        

    def OnListCtrl1ListItemActivated(self, event):
        item = self.listCtrl1.GetItemText(self.listCtrl1.GetFocusedItem())
        self.generateBOMmindmap(item)

    def OnCheckBox_pdf_drawingsCheckbox(self, event):
        mapbom.include_drawings = self.checkBox_pdf_drawings.Value

    def OnCheckBox_dwg_drawingsCheckbox(self, event):
        mapbom.include_DWGdrawings = self.checkBox_dwg_drawings.Value

    def FindPart(self):
        toplevel = mapbom.findpartslike(self.textCtrl_part_num.Value)
        if toplevel == []:
            self.listCtrl1.ClearAll()
            self.listCtrl1.Enable(False)
            self.textCtrlMessages.AppendText("\nPart number not found in Syteline\n\n\n")
            return
        self.listCtrl1.Enable(True)
        self.listCtrl1.ClearAll()
        self._init_coll_listCtrl1_Columns(self.listCtrl1)
        self.listCtrl1.SetFocus()
        for i, row in enumerate(toplevel):
            index = self.listCtrl1.InsertStringItem(i, '')
            self.listCtrl1.SetStringItem(i, 0, row.Item)
            self.listCtrl1.SetStringItem(i, 1, row.Description)
        self.button_CreateBOM.Show(True)

    def InitialiseHyperlinks(self):
        self.hyperLinkCtrl_Irish.SetToolTipString("What's this?")
        self.hyperLinkCtrl_Irish.AutoBrowse(False)
        self.hyperLinkCtrl_Irish.DoPopup(False)
        self.hyperLinkCtrl_Irish.Bind(wx.lib.hyperlink.EVT_HYPERLINK_LEFT, self.OnIrishHyperlink, id=wxID_FRAME1HYPERLINKCTRL_IRISH)
        self.hyperLinkCtrl_pdf.SetToolTipString("What's this?")
        self.hyperLinkCtrl_pdf.AutoBrowse(False)
        self.hyperLinkCtrl_pdf.DoPopup(False)
        self.hyperLinkCtrl_pdf.Bind(wx.lib.hyperlink.EVT_HYPERLINK_LEFT, self.OnPdfHyperlink, id=wxID_FRAME1HYPERLINKCTRL_PDF)
        self.hyperLinkCtrl_dwg.SetToolTipString("What's this?")
        self.hyperLinkCtrl_dwg.AutoBrowse(False)
        self.hyperLinkCtrl_dwg.DoPopup(False)
        self.hyperLinkCtrl_dwg.Bind(wx.lib.hyperlink.EVT_HYPERLINK_LEFT, self.OnDwgHyperlink, id=wxID_FRAME1HYPERLINKCTRL_DWG)
        self.hyperLinkCtrl_part_cost.SetToolTipString("What's this?")
        self.hyperLinkCtrl_part_cost.AutoBrowse(False)
        self.hyperLinkCtrl_part_cost.DoPopup(False)
        self.hyperLinkCtrl_part_cost.Bind(wx.lib.hyperlink.EVT_HYPERLINK_LEFT, self.OnPartCostHyperlink, id=wxID_FRAME1HYPERLINKCTRL_PART_COST)
        
        
    def OnIrishHyperlink(self, event):
        self.textCtrlMessages.AppendText('\nInclude Ireland Syteline in the parts search. This is useful for parts which are only stocked in Ireland, but it can be slow.')

    def OnPdfHyperlink(self, event):
        self.textCtrlMessages.AppendText('\nInclude links to pdf drawings.\nPdf files are stored on Sheffield/Temporary/MapBom/Drawings/')

    def OnDwgHyperlink(self, event):
        self.textCtrlMessages.AppendText('\nInclude links to dwg files on Sheffield. Mechanical Desktop is required to view these files.\n')

    def OnPartCostHyperlink(self, event):
        self.textCtrlMessages.AppendText('\nInclude part costs. The cost is mulitplied up by the number of parts used.\n')


    def OnButton_CreateBOMButton(self, event):
        print self.listCtrl1.GetFocusedItem()
        if self.listCtrl1.GetFocusedItem() == -1:
            self.textCtrlMessages.AppendText('\nNo part has been selected\n\n\n')
            return
        item = self.listCtrl1.GetItemText(self.listCtrl1.GetFocusedItem())
        self.generateBOMmindmap(item)

    def OnCheckBox_part_costsCheckbox(self, event):
        mapbom.include_part_costs = self.checkBox_part_costs.Value
