# This program is free software; it is licensed to you
# under every possible license.

import FreeCAD,importIFC,importIFCHelper,os

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtGui,QtCore

def translate(ctxt,txt):
    return txt

defaultSettings = {
    'DEBUG': True,
    'PREFIX_NUMBERS': False,
    'SKIP': [],
    'SEPARATE_OPENINGS': False,
    'ROOT_ELEMENT': "IfcProduct",
    'GET_EXTRUSIONS': False,
    'MERGE_MATERIALS': False,
    'MERGE_MODE_ARCH': 0,
    'MERGE_MODE_STRUCT': 1,
    'CREATE_CLONES': False,
    'IMPORT_PROPERTIES': False,
    'SPLIT_LAYERS': False,
    'FITVIEW_ONIMPORT': False,
    'ALLOW_INVALID': False,
    'REPLACE_PROJECT': False
}


def addProperties(doc, filename, settings):
    if "IFCTestData" in doc.PropertiesList:
        return
    td = doc.addObject("App::FeaturePython","IFCTestData")
    td.addProperty("App::PropertyFile", "IFCFile", "Test IFC", "The IFC file to test")
    td.IFCFile = filename
    td.Proxy = settings # TODO: Show this in the GUI

def makeReferenceFile(filename, settings):
    docname = os.path.splitext(os.path.basename(filename))[0]
    name = importIFCHelper.decode(docname,utf=True) + "_ref"
    doc = FreeCAD.newDocument(name)
    importIFC.insert(filename,doc.Name,preferences=settings)
    sname,sext = os.path.splitext(doc.FileName)
    if sname:
        doc.FileName = sname + "_ref" + sext
    else:
        doc.FileName = os.path.splitext(filename)[0] + "_ref.FCStd"
    addProperties(doc, os.path.basename(filename), settings)
    doc.recompute()
    doc.save()

class _CommandCreate:
    def Activated(self):
        from PySide import QtCore,QtGui

        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TestIFC")
        lastfolder = p.GetString("lastImportFolder","")
        filename = QtGui.QFileDialog.getOpenFileName(None,translate("EnVis","Select an IFC file"),lastfolder,translate("TestIFC","IFC files (*.ifc)"))
        if filename:
            filename = filename[0]
            p.SetString("lastImportFolder",os.path.dirname(filename))
        makeReferenceFile(filename, self.getsettings())

class _CommandCreateDefault(_CommandCreate):
    def GetResources(self):
        return {
            'MenuText': QtCore.QT_TRANSLATE_NOOP("TestIFC_CreateDefault","Create Reference (default)"),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP("TestIFC_CreateDefault","Create reference file with default settings")}

    def getsettings(self):
        return defaultSettings

class _CommandCreateLocal(_CommandCreate):
    def GetResources(self):
        return {
            'MenuText': QtCore.QT_TRANSLATE_NOOP("TestIFC_CreateLocal","Create Reference (local)"),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP("TestIFC_CreateLocal","Create reference file with local settings")}

    def getsettings(self):
        return importIFC.getPreferences()

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('TestIFC_Create_Default', _CommandCreateDefault())
    FreeCADGui.addCommand('TestIFC_Create_Local', _CommandCreateLocal())
