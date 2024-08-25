Attribute VB_Name = "Module4"
Sub ImportCategoriesFromCSVAndCreateNamedRange()
    Dim ws As Worksheet
    Dim csvFilePath As String
    Dim lastRow As Long
    Dim expensesRange As Range
    Dim incomeRange As Range
    Dim importSheet As Worksheet

    ' Path to the CSV file
    csvFilePath = ThisWorkbook.Path & "\Outputs\Categories.csv"
    
    ' Check if the import sheet exists, if not, create it
    On Error Resume Next
    Set importSheet = ThisWorkbook.Sheets("Transaction Categories")
    On Error GoTo 0
    
    If importSheet Is Nothing Then
        Set importSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
        importSheet.name = "Transaction Categories"
    End If

    ' Clear the import sheet
    importSheet.Cells.Clear

    ' Import CSV data into the import sheet
    With importSheet.QueryTables.Add(Connection:="TEXT;" & csvFilePath, Destination:=importSheet.Range("A1"))
        .TextFileParseType = xlDelimited
        .TextFileConsecutiveDelimiter = False
        .TextFileTabDelimiter = False
        .TextFileSemicolonDelimiter = False
        .TextFileCommaDelimiter = True
        .TextFileColumnDataTypes = Array(1, 1)
        .Refresh BackgroundQuery:=False
    End With

    ' Find the last row with data in column A
    lastRow = importSheet.Cells(importSheet.Rows.Count, "A").End(xlUp).Row
    
    ' Set the ranges for the categories
    Set expensesRange = importSheet.Range("A2:A" & lastRow)
    Set incomeRange = importSheet.Range("B2:B" & lastRow)

    ' Create named ranges in the current workbook
    ThisWorkbook.Names.Add name:="Expenses", RefersTo:=expensesRange
    ThisWorkbook.Names.Add name:="Income", RefersTo:=incomeRange
    
    ' Optionally, you may want to hide the import sheet
    ' importSheet.Visible = xlSheetVeryHidden

    MsgBox "Categories imported from CSV and named ranges 'Expenses' and 'Income' created."
End Sub
