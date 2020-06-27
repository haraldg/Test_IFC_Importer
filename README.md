This is a FreeCAD workbench intended for testing the IFC importer.
At the moment it is very bare bones and under heavy development.

This workbench allows you to:
 * create reference files
 * test the importer against reference files
 * compare two documents

A reference file is just a standard FreeCAD file that includes an object
holding metadata how it has been imported from IFC. Different versions
of the importer as well as different importer settings can be compared
against a reference file.

Self consistency checks working on a single file are planned for the
future.
