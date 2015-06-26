import arcpy
import arcpy.sa

workspace = arcpy.GetParameterAsText(0)
inRas = arcpy.GetParameterAsText(1)
inBuffers = arcpy.GetParameterAsText(2)
unID = arcpy.GetParameterAsText(3)
cellSize = arcpy.GetParameter(4)

if len(str(cellSize)) <= 1:
    cellSize = "#"
else:
    cellSize = cellSize

arcpy.env.workspace = workspace

with arcpy.da.SearchCursor(inBuffers, unID) as cursor:
    for row in cursor:
        expression = unID + "=" + "{0}".format(row[0])
        outFL = "{0}FL".format(row[0])
        outTable = "table{0}".format(row[0])
        arcpy.MakeFeatureLayer_management(inBuffers, outFL, expression)
        arcpy.sa.TabulateArea(outFL, unID, inRas, "Value", outTable, cellSize)
        arcpy.Delete_management(outFL)
tables = arcpy.ListTables("Table*")
totalTable = arcpy.Merge_management(tables, "TotalsTable")
for table in tables:
    arcpy.Delete_management(table)

wkspc = arcpy.Describe(workspace)
if wkspc.workspaceType == "FileSystem":
    totalTable = str(totalTable) + ".dbf"
else:
    totalTable = totalTable
    
fields = arcpy.ListFields(totalTable, "VALUE*")
    
for field in fields:
    expression = "zeroNull(!{0}!)".format(field.name)
    codeblock = """def zeroNull(field):
        if field is None:
            return 0
        else:
            return field"""
    arcpy.CalculateField_management(totalTable, field.name , expression, "PYTHON_9.3", codeblock)



