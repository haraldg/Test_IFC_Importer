# This program is free software; it is licensed to you
# under every possible license. (I.e. no rights reserved)

import FreeCAD,importIFC,os


if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtGui,QtCore

last_result = []

def compare(a, b, attrs, f):
    """Returns True if all attributes compare under f"""
    for attr in attrs:
        if not f(getattr(a, attr), getattr(b, attr)):
            return False
    return True

def stdcompare(a, b):
    return a == b

def epsiloncompare(a, b):
    return abs(a - b) < 0.001

def lencompare(a, b):
    return len(a) == len(b)


class Check:
    """Base class for checks. On it's own a pretty useless template."""
    def __init__(self):
        self.count_ok = 0
        self.failed = []
        self.name = "Useless identity check"

    def __call__(self, ro, co):
        try:
            if self.compare(ro, co):
                self.count_ok += 1
                return True
        except:
            print("Exception while running check. Treating as failure.")
        self.failed.append((ro, co))
        return False

    def compare(self, ro, co):
        return True

class CheckBoundingBox(Check):
    def __init__(self):
        Check.__init__(self)
        self.name = "BoundingBox"

    def compare(self, ro, co):
        return compare(ro.Shape.BoundBox, co.Shape.BoundBox, ["XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax"], epsiloncompare)

class CheckGeometryType(Check):
    def __init__(self):
        Check.__init__(self)
        self.name = "Number of Subshapes"

    def compare(self, ro, co):
        return compare(ro.Shape, co.Shape, ["CompSolids", "Compounds", "Edges", "Faces", "Shells", "Solids", "Vertexes"], lencompare)

class CheckGeometryValues(Check):
    def __init__(self):
        Check.__init__(self)
        self.name = "shape values"

    def compare(self, ro, co):
        if ro.Shape.isNull():
            return True
        return compare(ro.Shape, co.Shape, ["Area", "Length", "Volume"], epsiloncompare)


def compareByGuid(ref, candidate, checks):
    """compare(ref, candidate, checks): compare the two documents and report differences. Objects are matched by IfcGuid
    checks: list of callable objects check(ref_obj, candidate_obj) returning False if the check fails"""

    cobjs = {}
    missing = []
    for o in candidate.Objects:
        if hasattr(o, "GlobalId"):
            cobjs[o.GlobalId] = o

    for ro in ref.Objects:
        if not hasattr(ro, "GlobalId"):
            continue
        try:
            co = cobjs.pop(ro.GlobalId)
        except KeyError:
            missing.append(ro)
            continue
        for check in checks:
            if not check(ro, co):
                print("Error comparing '", ro.Label, "' with '", co.Label, "'")

    if cobjs:
        print("Document contains", len(cobjs), "extra objecs:", cobjs.keys())
    if missing:
        print("Error: Document misses", len(missing), "objects:", [m.Label for m in missing])

    return missing


def print_report(checks):
    global last_result
    last_result = checks

    for c in checks:
        total = c.count_ok + len(c.failed)
        if c.failed:
            print("check", c.name, "failed for the following", len(c.failed), "/", total, "objects (GUID):")
            for (ro,co) in c.failed:
                print("    ", ro.GlobalId)
        else:
            print("check", c.name, "successfull for all", c.count_ok, "objects")


class _CommandCompare:
    def GetResources(self):
        return {
            'MenuText': QtCore.QT_TRANSLATE_NOOP("TestIFC_Compare","Compare documents"),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP("TestIFC_Compare","Compare two documents")}

    def IsActive(self):
        return len(FreeCAD.listDocuments()) == 2

    def Activated(self):
        checks = [CheckBoundingBox(), CheckGeometryType(), CheckGeometryValues()]
        docs = [d for d in FreeCAD.listDocuments().values()]
        if hasattr(docs[1], "IFCTestData"):
            docs.reverse()

        compareByGuid(docs[0], docs[1], checks)
        print_report(checks)

class _CommandRunTestRef:
    def GetResources(self):
        return {
            'MenuText': QtCore.QT_TRANSLATE_NOOP("TestIFC_RunTestRef","Run Reference Test"),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP("TestIFC_RunTestRef","Import IFC file with settings from reference and compare the result")}

    def IsActive(self):
        return hasattr(FreeCAD.ActiveDocument, "IFCTestData")

    def Activated(self):
        refdoc = FreeCAD.ActiveDocument
        filename = os.path.join(os.path.dirname(refdoc.FileName), refdoc.IFCTestData.IFCFile)
        newdoc = importIFC.insert(filename, refdoc.IFCTestData.IFCFile, preferences=refdoc.IFCTestData.Proxy)

        checks = [CheckBoundingBox(), CheckGeometryType(), CheckGeometryValues()]
        compareByGuid(refdoc, newdoc, checks)
        print_report(checks)

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('TestIFC_Compare', _CommandCompare())
    FreeCADGui.addCommand('TestIFC_RunTestRef', _CommandRunTestRef())
