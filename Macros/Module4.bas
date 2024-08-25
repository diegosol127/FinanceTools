Attribute VB_Name = "Module4"
Sub RunPythonScriptWithArgs()
    Dim pythonPath As String
    Dim scriptPath As String
    Dim cmd As String
    Dim month As String
    Dim year As String
    Dim verbose As Boolean

    ' Retrieve the month and year from named ranges
    month = Evaluate("current_month").Value
    year = Evaluate("current_year").Value
    
    ' Set verbose mode
    verbose = False ' Change this to False if you don't want verbose mode
    
    ' Modify pythonPath if Python is not in the system PATH
    pythonPath = "python"
    
    ' Set the path to your Python script
    scriptPath = ThisWorkbook.Path & "\SortTransactions.py"
    
    ' Construct the command to run
    cmd = pythonPath & " " & scriptPath & " --month " & month & " --year " & year
    If verbose Then
        cmd = cmd & " --verbose"
    End If
    
    ' Run the command using Shell
    Call Shell(cmd, vbNormalFocus)
End Sub
