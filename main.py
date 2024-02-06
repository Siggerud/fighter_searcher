from queryTool import queryTool

tool = queryTool()
tool.setTable("fighters")
tool.setColumn("name")
print(tool.query())