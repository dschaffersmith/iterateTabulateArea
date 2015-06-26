# iterateTabulateArea
Python script iterates dataset and runs tabulate area on each feature

This was developed because the Arc tool 'Tabulate Area' does not handle overlapping polygons. 

Instead, this tool iterates over the features via arcpy.da.SearchCursor, creates a FeatureLayer, and executes the Tabulate Area tool.

Output tables are merged in to one table to record all areas from feature class zones. 
