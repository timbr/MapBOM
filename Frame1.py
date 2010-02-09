#Boa:Frame:Frame1

import wx
from classPartUtils import PartUtils#

mapbom = PartUtils()

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON_OK, wxID_FRAME1CHECKBOX_DWG_DRAWINGS, 
 wxID_FRAME1CHECKBOX_IRISH, wxID_FRAME1CHECKBOX_PDF_DRAWINGS, 
 wxID_FRAME1LISTCTRL1, wxID_FRAME1STATICBOXBOM, wxID_FRAME1STATICBOXMESSAGES, 
 wxID_FRAME1STATICBOXOPTIONS, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1TEXTCTRLMESSAGES, wxID_FRAME1TEXTCTRL_PART_NUM, 
] = [wx.NewId() for _init_ctrls in range(12)]

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
              pos=wx.Point(488, 256), size=wx.Size(456, 473),
              style=wx.DEFAULT_FRAME_STYLE, title='MapBOM GUI')
        self.SetClientSize(wx.Size(448, 446))
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        self.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.SetThemeEnabled(False)
        self.SetIcon(wx.Icon(u'C:/Python25/tim/mapbomclass/mapbom.ico',
              wx.BITMAP_TYPE_ICO))

        self.textCtrl_part_num = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL_PART_NUM,
              name='textCtrl_part_num', parent=self, pos=wx.Point(24, 40),
              size=wx.Size(120, 24), style=0, value='Enter Assy Number')
        self.textCtrl_part_num.Bind(wx.EVT_TEXT_ENTER,
              self.OnTextCtrl_part_numTextEnter,
              id=wxID_FRAME1TEXTCTRL_PART_NUM)
        self.textCtrl_part_num.Bind(wx.EVT_LEFT_DOWN,
              self.OnTextCtrl_part_numLeftDown)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1, label='',
              name='staticText1', parent=self, pos=wx.Point(192, 368),
              size=wx.Size(232, 16), style=0)

        self.staticBoxBOM = wx.StaticBox(id=wxID_FRAME1STATICBOXBOM,
              label='Bill Of Materials', name='staticBoxBOM', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(432, 232), style=0)

        self.button_OK = wx.Button(id=wxID_FRAME1BUTTON_OK, label='OK',
              name='button_OK', parent=self, pos=wx.Point(168, 40),
              size=wx.Size(32, 23), style=0)
        self.button_OK.Bind(wx.EVT_BUTTON, self.OnButton_OKButton,
              id=wxID_FRAME1BUTTON_OK)

        self.checkBox_Irish = wx.CheckBox(id=wxID_FRAME1CHECKBOX_IRISH,
              label='Search Ireland Syteline', name='checkBox_Irish',
              parent=self, pos=wx.Point(24, 272), size=wx.Size(128, 13),
              style=0)
        self.checkBox_Irish.SetValue(True)
        self.checkBox_Irish.SetToolTipString('checkBox_Irish')
        self.checkBox_Irish.Bind(wx.EVT_CHECKBOX, self.OnCheckBox_IrishCheckbox,
              id=wxID_FRAME1CHECKBOX_IRISH)

        self.staticBoxOptions = wx.StaticBox(id=wxID_FRAME1STATICBOXOPTIONS,
              label='Options', name='staticBoxOptions', parent=self,
              pos=wx.Point(16, 248), size=wx.Size(160, 100), style=0)

        self.listCtrl1 = wx.ListCtrl(id=wxID_FRAME1LISTCTRL1, name='listCtrl1',
              parent=self, pos=wx.Point(24, 80), size=wx.Size(368, 144),
              style=wx.LC_REPORT)
        self.listCtrl1.Show(True)
        self.listCtrl1.Enable(False)
        self._init_coll_listCtrl1_Columns(self.listCtrl1)
        self.listCtrl1.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
              self.OnListCtrl1ListItemActivated, id=wxID_FRAME1LISTCTRL1)

        self.checkBox_pdf_drawings = wx.CheckBox(id=wxID_FRAME1CHECKBOX_PDF_DRAWINGS,
              label='Add links to pdf drawings', name='checkBox_pdf_drawings',
              parent=self, pos=wx.Point(24, 296), size=wx.Size(144, 13),
              style=0)
        self.checkBox_pdf_drawings.SetValue(True)
        self.checkBox_pdf_drawings.SetToolTipString('checkBox_pdf_drawings')
        self.checkBox_pdf_drawings.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBox_pdf_drawingsCheckbox,
              id=wxID_FRAME1CHECKBOX_PDF_DRAWINGS)

        self.checkBox_dwg_drawings = wx.CheckBox(id=wxID_FRAME1CHECKBOX_DWG_DRAWINGS,
              label='Add links to dwg drawings', name='checkBox_dwg_drawings',
              parent=self, pos=wx.Point(24, 320), size=wx.Size(144, 13),
              style=0)
        self.checkBox_dwg_drawings.SetValue(False)
        self.checkBox_dwg_drawings.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBox_dwg_drawingsCheckbox,
              id=wxID_FRAME1CHECKBOX_DWG_DRAWINGS)

        self.staticBoxMessages = wx.StaticBox(id=wxID_FRAME1STATICBOXMESSAGES,
              label='Messages', name='staticBoxMessages', parent=self,
              pos=wx.Point(192, 248), size=wx.Size(248, 100), style=0)

        self.textCtrlMessages = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLMESSAGES,
              name='textCtrlMessages', parent=self, pos=wx.Point(200, 272),
              size=wx.Size(232, 64), style=0, value='')
        self.textCtrlMessages.SetEditable(False)
        self.textCtrlMessages.SetInsertionPoint(2)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnTextCtrl_part_numTextEnter(self, event):
        self.FindPart()

    def OnButton_OKButton(self, event):
##        self.staticText1.Label = self.textCtrl_part_num.Value
        self.textCtrlMessages.AppendText(self.textCtrl_part_num.Value)
##        self.button_OK.Shown = False

    def OnCheckBox_IrishCheckbox(self, event):
        mapbom.include_ireland_data = self.checkBox_Irish.Value

    def OnTextCtrl_part_numLeftDown(self, event):
        event.Skip()
        
    def generateBOMmindmap(self, partnum):
        mapbom.part_num = partnum
        outputfile = "C:\\Program Files\\MapBom\\BOMmindmap.mm"
        mapbom.filename = outputfile
        mapbom.generateBOMmap()
        self.textCtrlMessages.AppendText('Mindmap created for %s' % (partnum))
        

    def OnListCtrl1ListItemActivated(self, event):
        item = self.listCtrl1.GetItemText(self.listCtrl1.GetFocusedItem())
        self.textCtrlMessages.AppendText('Creating BOM Mindmap for %s' % (item))
        mapbom.part_num = item
        outputfile = "C:\\Program Files\\MapBom\\BOMmindmap.mm"
        mapbom.filename = outputfile
        mapbom.generateBOMmap()

    def OnCheckBox_pdf_drawingsCheckbox(self, event):
        mapbom.include_drawings = self.checkBox_dwg_drawings.Value

    def OnCheckBox_dwg_drawingsCheckbox(self, event):
        mapbom.include_DWGdrawings = self.checkBox_dwg_drawings.Value

    def FindPart(self):
        self.staticText1.Label = ''
        toplevel = mapbom.findpartslike(self.textCtrl_part_num.Value)
        if toplevel == []:
            self.listCtrl1.ClearAll()
            self.listCtrl1.Enable(False)
            self.textCtrlMessages.AppendText("Part number not found in Syteline")
            return
        if len(toplevel) == 1:
            self.listCtrl1.ClearAll()
            self.listCtrl1.Enable(False)
            self.textCtrlMessages.AppendText('Creating BOM Mindmap for %s' % (toplevel[0].Item))
            self.generateBOMmindmap(toplevel[0].Item)
            return
        self.listCtrl1.Enable(True)
        self.listCtrl1.ClearAll()
        self._init_coll_listCtrl1_Columns(self.listCtrl1)
        self.listCtrl1.SetFocus()
        for i, row in enumerate(toplevel):
            index = self.listCtrl1.InsertStringItem(i, '')
            self.listCtrl1.SetStringItem(i, 0, row.Item)
            self.listCtrl1.SetStringItem(i, 1, row.Description)
##            self.listBox1.Append("%s    %s" % (row.Item, row.Description))
        
