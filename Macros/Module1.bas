Attribute VB_Name = "Module1"
Sub ImportCSV()
    Dim ws As Worksheet
    Dim outputFolderDir As String
    Dim csvFilePath As String
    Dim csvFullPath As String
    Dim csvData As Variant
    Dim lastRow As Long
    Dim i As Long, j As Long
    
    ' Set your worksheet where you want to populate the data
    Set ws = ThisWorkbook.Sheets("Income and Expenses")
    
    ' Clear any existing table
    On Error Resume Next
    Set tbl = ws.ListObjects("Transactions")
    If Not tbl Is Nothing Then
        ' Define the range of cells to clear
        Dim maxRow As Long
        Dim clearRange As Range
        maxRow = ws.Rows.Count
        Set clearRange = ws.Range("B3:F" & maxRow)
        ' Delete the table
        tbl.Delete
        ' Fill the area where the table used to be with color white
        clearRange.ClearContents
        clearRange.Interior.Color = RGB(255, 255, 255)
    End If
    On Error GoTo 0
    
    ' Get CSV file
    outputFolderDir = ThisWorkbook.Path & "\Outputs"
    csvFullPath = GetFilePath(outputFolderDir, Evaluate("year_month"))
    ' Read the CSV file
    csvData = ReadCSVFile(csvFullPath)
    
    ' Check if the data is read correctly
    If Not IsArray(csvData) Then
        MsgBox "Failed to import budget data. Make sure a CSV file exists for the selected MONTH and YEAR. " & _
            "If the file exists, inpect the format.", vbExclamation
        Exit Sub
    End If
    
    ' Set the first row in the worksheet to start populating the data
    startRow = 4
    
    ' Populate the data into the worksheet
    For i = LBound(csvData) To UBound(csvData)
        For j = 0 To 4
            ws.Cells(startRow + i - LBound(csvData), j + 2).Value = csvData(i, j)
        Next j
    Next i
    
    ' Create a table from the CSV data
    CreateTransactionTable
End Sub



Sub CreateCategoriesTable()
    Dim ws As Worksheet
End Sub



Sub CreateTransactionTable()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim tblRange As Range
    Dim tbl As ListObject
    
    ' Set reference to the worksheet
    Set ws = ThisWorkbook.Sheets("Income and Expenses")
    
    ' Find the last populated row in column B
    lastRow = ws.Cells(ws.Rows.Count, "B").End(xlUp).Row
    
    ' Define the range for the table including headers
    Set tblRange = ws.Range("B4:F" & lastRow) ' Assuming columns B to E starting on row 4
    
    ' Clear the background color of the table range to preserve table style and colors
    tblRange.Interior.ColorIndex = xlNone
    
    ' Create the table
    Set tbl = ws.ListObjects.Add(xlSrcRange, tblRange, , xlYes)
    ' Apply a theme color to the table (e.g., "TableStyleLight9")
    tbl.TableStyle = "TableStyleTransaction"
    tbl.name = "Transactions"
    ' Format the "Amount" column as currency
    tbl.ListColumns("Amount").DataBodyRange.NumberFormat = "$#,##0.00"
    ' Set different formats for positive and negative numbers
    tbl.ListColumns("Amount").DataBodyRange.FormatConditions.Add Type:=xlCellValue, Operator:=xlGreaterEqual, Formula1:="0"
    tbl.ListColumns("Amount").DataBodyRange.FormatConditions(tbl.ListColumns("Amount").DataBodyRange.FormatConditions.Count).Font.Color = RGB(0, 128, 0)
    tbl.ListColumns("Amount").DataBodyRange.FormatConditions.Add Type:=xlCellValue, Operator:=xlLess, Formula1:="0"
    tbl.ListColumns("Amount").DataBodyRange.FormatConditions(tbl.ListColumns("Amount").DataBodyRange.FormatConditions.Count).Font.Color = RGB(255, 0, 0)
    ' Remove the filter buttons
    tbl.ShowAutoFilter = False
    ' Make header row bold and centered
    tbl.HeaderRowRange.Font.Bold = True
    tbl.HeaderRowRange.HorizontalAlignment = xlCenter
    
End Sub



Function ReadCSVFile(filePath As String) As Variant
    Dim fso As Object
    Dim ts As Object
    Dim line As String
    Dim data As Variant
    Dim rowData As Variant
    Dim i As Long
    Dim numRows As Long
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' Check if the file exists
    If Not fso.FileExists(filePath) Then
        ReadCSVFile = CVErr(xlErrNA)
        Exit Function
    End If
    
    ' Open the CSV file
    Set ts = fso.OpenTextFile(filePath, 1)
    
    ' Determine the number of rows in the CSV file
    numRows = 0
    Do While Not ts.AtEndOfStream
        ts.ReadLine
        numRows = numRows + 1
    Loop
    
    ' Close and reopen the CSV file to reset the file cursor
    ts.Close
    Set ts = fso.OpenTextFile(filePath, 1)
    
    ' Read the first line to determine the number of columns
    line = ts.ReadLine
    rowData = Split(line, ",")
    
    ' Initialize data array based on the number of rows and columns
    ReDim data(0 To numRows - 1, 0 To UBound(rowData))
    For i = 0 To 4
        data(0, i) = rowData(i)
    Next i
    
    ' Read the rest of the lines
    i = 1
    Do While Not ts.AtEndOfStream
        line = ts.ReadLine
        rowData = Split(line, ",")
        
        ' Populate data array with row data
        For j = 0 To 4
            data(i, j) = rowData(j)
        Next j
        i = i + 1
    Loop
    
    ' Close the file
    ts.Close
    
    ' Return CSV data
    ReadCSVFile = data
End Function

Function GetFilePath(parentDir As String, searchStr As String) As String
    Dim fileName As String
    Dim fileFound As String
    
    ' Initialize file found with empty string
    fileFound = ""
    
    ' Get the first file in the directory
    fileName = Dir(parentDir & "\*.*")
    ' Loop through all files in the directory
    Do While fileName <> ""
        ' Check if the file file contains the search string
        If InStr(1, fileName, searchStr, vbTextCompare) > 0 Then
            fileFound = parentDir & "\" & fileName
            Exit Do
        End If
        ' Get the next file in the directory
        fileName = Dir
    Loop
    
    GetFilePath = fileFound
End Function

