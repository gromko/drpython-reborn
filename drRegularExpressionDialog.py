#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2010 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#    DrPython is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#Regular Expression Dialog

import os
import re
import wx
import drScrolledMessageDialog
import drFileDialog

wildcard = "Text File (*.txt)|*.txt|All files (*)|*"

class drRETextCtrl(wx.TextCtrl):
    def __init__(self, parent, id, value, pos, size):
        wx.TextCtrl.__init__(self, parent, id, value, pos, size)

        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.GetParent().OnbtnCancel(event)
        elif event.GetKeyCode() == wx.WXK_RETURN:
            self.GetParent().OnbtnOk(event)
        else:
            event.Skip()


class drRegularExpressionDialog(wx.Frame):
    def __init__(self, parent, id, title, prompthasfocus = 0, infiles = 0):

        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.insert = (title == "Insert Regular Expression")

        self.theSizer = wx.FlexGridSizer(0, 1, 5, 10)

        okcancelSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.parent = parent
        self.prompthasfocus = prompthasfocus

        #that part of code is ugly
        if self.insert:
            self.drpyframe = self.parent
        elif not infiles:
            self.drpyframe = self.parent.GetParent()
        else:
            self.drpyframe = self.parent.GetGrandParent()

        self.defaultdirectory = self.drpyframe.prefs.defaultdirectory
        self.enablefeedback = self.drpyframe.prefs.enablefeedback
        self.filedialogparent = self.drpyframe
        self.regdatdirectory = os.path.join(self.drpyframe.datdirectory, "regex")
        if not os.path.exists(self.regdatdirectory):
            os.mkdir(self.regdatdirectory)

        #end of uglpy part of code

        FileMenu = wx.Menu()
        FileMenu.Append(wx.ID_OPEN)
        FileMenu.Append(wx.ID_SAVE)

        TextMenu = wx.Menu()
        mnuNormalText = TextMenu.Append(wx.ID_ANY, "Normal Text")
        mnuAnyChar = TextMenu.Append(wx.ID_ANY, 'Any Character  "."')
        mnuAnyDigit = TextMenu.Append(wx.ID_ANY, 'Any Decimal Digit  "\\d"')
        mnuAnyNonDigit = TextMenu.Append(wx.ID_ANY, 'Any Non Digit  "\\D"')
        mnuAnyWS = TextMenu.Append(wx.ID_ANY, 'Any Whitespace Character  "\\s"')
        mnuAnyNonWS = TextMenu.Append(wx.ID_ANY, 'Any Non Whitespace Character  "\\S"')
        mnuAnyAlphaNum = TextMenu.Append(wx.ID_ANY, 'Any AlphaNumeric Character  "\\w"')
        mnuAnyNonAlphaNum = TextMenu.Append(wx.ID_ANY, 'Any Non AlphaNumeric Character  "\\W"')
        mnuCharSet = TextMenu.Append(wx.ID_ANY, 'A Set of Characters  "[]"')

        RepetitionsMenu = wx.Menu()
        mnuZeroOrMore = RepetitionsMenu.Append(wx.ID_ANY, "0 Or More  \"*\"")
        mnuOneOrMore = RepetitionsMenu.Append(wx.ID_ANY, "1 Or More  \"+\"")
        mnuZeroOrOne = RepetitionsMenu.Append(wx.ID_ANY, "0 Or 1  \"?\"")
        mnuRepeat = RepetitionsMenu.Append(wx.ID_ANY, "n  \"{n}\"")

        LimitMenu = wx.Menu()
        mnuStartOfLine = LimitMenu.Append(wx.ID_ANY, 'The Start Of Each Line  "^"')
        mnuEndOfLine = LimitMenu.Append(wx.ID_ANY, 'The End Of Each Line  "$"')
        mnuStartOfDoc = LimitMenu.Append(wx.ID_ANY, 'The Start of the Document  "\\A"')
        mnuEndOfDoc = LimitMenu.Append(wx.ID_ANY, 'The End of the Document  "\\Z"')
        mnuWordBoundary = LimitMenu.Append(wx.ID_ANY, 'The Start or End of a Word  "\\b"')
        mnuNonWordBoundary = LimitMenu.Append(wx.ID_ANY, 'Text That is Not at Either End of a Word  "\\B"')

        lookMenu = wx.Menu()
        mnuPositiveLookahead = lookMenu.Append(wx.ID_ANY, "Lookahead: Positive  \"(?=)\"")
        mnuNegativeLookahead = lookMenu.Append(wx.ID_ANY, "Lookahead: Negative  \"(?!)\"")
        mnuPositiveLookbehind = lookMenu.Append(wx.ID_ANY, "Lookbehind: Positive  \"(?<=)\"")
        mnuNegativeLookbehind = lookMenu.Append(wx.ID_ANY, "Lookbehind: Negative  \"(?<!)\"")

        InsertMenu = wx.Menu()
        InsertMenu.AppendMenu(wx.ID_ANY, "&Text", TextMenu)
        InsertMenu.AppendMenu(wx.ID_ANY, "&Repetitions", RepetitionsMenu)
        InsertMenu.AppendMenu(wx.ID_ANY, "&Match", LimitMenu)
        InsertMenu.AppendMenu(wx.ID_ANY, "&Assertions", lookMenu)
        mnuOr = InsertMenu.Append(wx.ID_ANY, "&Or  \"|\"")
        mnuGroup = InsertMenu.Append(wx.ID_ANY, "&Group  \"( )\"")

        menuBar = wx.MenuBar()
        menuBar.Append(FileMenu, "&File")
        menuBar.Append(InsertMenu, "&Insert")

        self.SetMenuBar(menuBar)

        self.txtRE = drRETextCtrl(self, -1, "", wx.DefaultPosition, (500, -1))

        self.btnOk = wx.Button(self, wx.ID_OK)
        self.btnCancel = wx.Button(self, wx.ID_CANCEL)

        okcancelSizer.Add(self.btnOk, 1, wx.SHAPED)
        okcancelSizer.Add(self.btnCancel, 1, wx.SHAPED)

        self.theSizer.Add(self.txtRE, 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(okcancelSizer, 1, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.btnOk.SetDefault()
        self.txtRE.SetFocus()

        self.Bind(wx.EVT_BUTTON, self.OnbtnCancel, self.btnCancel)
        self.Bind(wx.EVT_BUTTON, self.OnbtnOk, self.btnOk)

        self.Bind(wx.EVT_MENU, self.OnLoad, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacter, mnuAnyChar)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacterD, mnuAnyDigit)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacterND, mnuAnyNonDigit)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacterW, mnuAnyWS)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacterNW, mnuAnyNonWS)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacterA, mnuAnyAlphaNum)
        self.Bind(wx.EVT_MENU, self.OnbtnAnyCharacterNA, mnuAnyNonAlphaNum)
        self.Bind(wx.EVT_MENU, self.OnbtnSetOfCharacters, mnuCharSet)
        self.Bind(wx.EVT_MENU, self.OnbtnStart, mnuStartOfLine)
        self.Bind(wx.EVT_MENU, self.OnbtnEnd, mnuEndOfLine)
        self.Bind(wx.EVT_MENU, self.OnbtnStartD, mnuStartOfDoc)
        self.Bind(wx.EVT_MENU, self.OnbtnEndD, mnuEndOfDoc)
        self.Bind(wx.EVT_MENU, self.OnbtnEdgeW, mnuWordBoundary)
        self.Bind(wx.EVT_MENU, self.OnbtnEdgeNW, mnuNonWordBoundary)
        self.Bind(wx.EVT_MENU, self.OnbtnRepsZeroPlus, mnuZeroOrMore)
        self.Bind(wx.EVT_MENU, self.OnbtnRepsOnePlus, mnuOneOrMore)
        self.Bind(wx.EVT_MENU, self.OnbtnRepsZeroOrOne, mnuZeroOrOne)
        self.Bind(wx.EVT_MENU, self.OnbtnRepsN, mnuRepeat)
        self.Bind(wx.EVT_MENU, self.OnbtnOr, mnuOr)
        self.Bind(wx.EVT_MENU, self.OnbtnGroup, mnuGroup)
        self.Bind(wx.EVT_MENU, self.OnbtnLookPositiveA, mnuPositiveLookahead)
        self.Bind(wx.EVT_MENU, self.OnbtnLookNegativeA, mnuNegativeLookahead)
        self.Bind(wx.EVT_MENU, self.OnbtnLookPositiveB, mnuPositiveLookbehind)
        self.Bind(wx.EVT_MENU, self.OnbtnLookNegativeB, mnuNegativeLookbehind)

        self.Bind(wx.EVT_MENU, self.OnbtnInsertNormalText, mnuNormalText)

        if self.drpyframe.PLATFORM_IS_WIN:
            size = (500, 160)
        else:
            size = (500, 110)
        self.SetSize(size)

    def insertText(self, text):
        pos = self.txtRE.GetInsertionPoint()
        textRE = self.txtRE.GetValue()
        self.txtRE.SetValue(textRE[0:pos] + text + textRE[pos:])
        self.txtRE.SetInsertionPoint(pos + len(text))

    def OnbtnAnyCharacter(self, event):
        self.insertText('.')

    def OnbtnAnyCharacterA(self, event):
        self.insertText('\\w')

    def OnbtnAnyCharacterD(self, event):
        self.insertText('\\d')

    def OnbtnAnyCharacterNA(self, event):
        self.insertText('\\W')

    def OnbtnAnyCharacterND(self, event):
        self.insertText('\\D')

    def OnbtnAnyCharacterNW(self, event):
        self.insertText('\\S')

    def OnbtnAnyCharacterW(self, event):
        self.insertText('\\s')

    def OnbtnCancel(self, event):
        self.txtRE.SetValue("")
        self.Close(1)

    def OnbtnEdgeNW(self, event):
        self.insertText('\\B')

    def OnbtnEdgeW(self, event):
        self.insertText('\\b')

    def OnbtnEnd(self, event):
        self.insertText('$')

    def OnbtnEndD(self, event):
        self.insertText('\\Z')

    def OnbtnGroup(self, event):
        self.insertText('()')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnInsertNormalText(self, event):
        d = wx.TextEntryDialog(self, "Enter Normal Text", "Insert Normal Text", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            self.insertText(re.escape(v))

    def OnbtnLookNegativeA(self, event):
        self.insertText('(?!)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnLookPositiveA(self, event):
        self.insertText('(?=)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnLookNegativeB(self, event):
        self.insertText('(?<!)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnLookPositiveB(self, event):
        self.insertText('(?<=)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnOk(self, event):
        self.Show(0)

        result = self.txtRE.GetValue()
        l = len(result)
        if l > 0:
            if self.insert:
                if self.prompthasfocus:
                    pos = self.parent.txtPrompt.GetCurrentPos()
                    self.parent.txtPrompt.InsertText(pos, result)
                    self.parent.txtPrompt.GotoPos(pos + l)
                else:
                    pos = self.parent.txtDocument.GetCurrentPos()
                    self.parent.txtDocument.InsertText(pos, result)
                    self.parent.txtDocument.GotoPos(pos + l)
            else:
                self.parent.txtSearchFor.SetValue(result)

        self.Close(1)

    def OnbtnOr(self, event):
        self.insertText('|')

    def OnbtnRepsN(self, event):
        d = wx.TextEntryDialog(self, "Enter The Desired Number of Repetitions:", "Insert N Repetitions", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            self.insertText('{' + v + '}')

    def OnbtnRepsOnePlus(self, event):
        self.insertText('+')

    def OnbtnRepsZeroOrOne(self, event):
        self.insertText('?')

    def OnbtnRepsZeroPlus(self, event):
        self.insertText('*')

    def OnbtnSetOfCharacters(self, event):
        self.insertText('[]')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnStart(self, event):
        self.insertText('^')

    def OnbtnStartD(self, event):
        self.insertText('\\A')

    def OnLoad(self, event):
        dlg = drFileDialog.FileDialog(self.filedialogparent, "Load Regular Expression From", wildcard)
        if self.regdatdirectory:
            try:
                dlg.SetDirectory(self.regdatdirectory)
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Setting Default Directory To: " + self.regdatdirectory), "DrPython Error")
        if dlg.ShowModal() == wx.ID_OK:
            refile = dlg.GetPath().replace('\\', '/')
            try:
                f = open(refile, 'r')
                text = f.read()
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Reading From: " +  refile), "DrPython Error")
                text = ""
            if (text.find('\n') > -1) or (text.find('\r') > -1):
                drScrolledMessageDialog.ShowMessage(self, ("Error Reading From: " +  refile), "DrPython Error")
                text = ""
            self.txtRE.SetValue(text)

        dlg.Destroy()
        self.Raise()

    def OnSave(self, event):
        dlg = drFileDialog.FileDialog(self.filedialogparent, "Save Regular Expression As", wildcard, IsASaveDialog=True)
        if self.regdatdirectory:
            try:
                dlg.SetDirectory(self.regdatdirectory)
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Setting Default Directory To: " + self.regdatdirectory), "DrPython Error")
        if dlg.ShowModal() == wx.ID_OK:
            refile = dlg.GetPath().replace('\\', '/')
            if refile.lower()[-4:] != ".txt":
                refile += ".txt"
            try:
                f = open(refile, 'w')
                f.write(self.txtRE.GetValue())
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Writing To: " +  refile), "DrPython Error")
                return
            if self.enablefeedback:
                drScrolledMessageDialog.ShowMessage(self, ("Successfully Saved: " + refile), "Save Success")
            dlg.Destroy()
        self.Raise()
