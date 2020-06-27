# This program is free software; it is licensed to you
# under every possible license.

class TestIFCImporter(Workbench):


    def __init__(self):

        self.__class__.MenuText = "Test IFC Importer"
        self.__class__.ToolTip = "Test the importer on any IFC files"
        self.__class__.Icon = """
/* XPM */
static char * IFC_xpm[] = {
"16 16 9 1",
" 	c None",
".	c #D80742",
"+	c #C20B5E",
"@	c #B11A71",
"#	c #0E4A94",
"$	c #A12288",
"%	c #61398E",
"&	c #983563",
"*	c #1E8BA6",
"                ",
"     #   ..     ",
"    ### ....    ",
"   ## ##+  ..   ",
"  ##  .##   ..  ",
" ##  +. ##   .. ",
" ## $$$+##**..  ",
"  #%$$$%#**&.   ",
"  $$% ##*+..&*  ",
" $$$###*@..  ** ",
" $$  #**$@@  ** ",
"  $$  **%$  **  ",
"   $$  **  **   ",
"    $$$$****    ",
"     $$  **     ",
"                "};
"""

    def Initialize(self):

        import Arch
        import TestIFCReference, TestIFCCompare

        self.commands = ["TestIFC_Create_Default", "TestIFC_Create_Local", "TestIFC_Compare", "TestIFC_RunTestRef"]
        self.appendMenu("Test IFC", self.commands)

        # load Arch & Draft preference pages
        if hasattr(FreeCADGui,"draftToolBar"):
            if not hasattr(FreeCADGui.draftToolBar,"loadedArchPreferences"):
                import Arch_rc
                FreeCADGui.addPreferencePage(":/ui/preferences-arch.ui","Arch")
                FreeCADGui.addPreferencePage(":/ui/preferences-archdefaults.ui","Arch")
                FreeCADGui.draftToolBar.loadedArchPreferences = True
            if not hasattr(FreeCADGui.draftToolBar,"loadedPreferences"):
                import Draft_rc
                FreeCADGui.addPreferencePage(":/ui/preferences-draft.ui","Draft")
                FreeCADGui.addPreferencePage(":/ui/preferences-draftsnap.ui","Draft")
                FreeCADGui.addPreferencePage(":/ui/preferences-draftvisual.ui","Draft")
                FreeCADGui.addPreferencePage(":/ui/preferences-drafttexts.ui","Draft")
                FreeCADGui.draftToolBar.loadedPreferences = True

        Log ('Loading Test IFC module... done\n')
        FreeCADGui.updateLocale()

    def Activated(self):
        Log("Test IFC Importer workbench activated\n")

    def Deactivated(self):
        Log("Test IFC Importer workbench deactivated\n")

    def GetClassName(self):
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(TestIFCImporter)




