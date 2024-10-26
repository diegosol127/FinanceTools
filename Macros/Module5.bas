Attribute VB_Name = "Module5"
Sub SaveCSV()
    Dim ws As Worksheet
    Dim tbl As ListObject
    Dim csvFilePath As String
    Dim year_month As String
    Dim fileNumber As Integer
    Dim row As ListRow
    Dim cell As Range
    Dim outputFolderDir As String

    ' Define the sheet and table
    Set ws = ThisWorkbook.Sheets("Income and Expenses")
    Set tbl = ws.ListObjects("Transactions")
    
    ' Get the year_month variable (replace with actual year_month value if needed)
    year_month = Evaluate("year_month")
    
    ' Set the path to the Outputs folder
    outputFolderDir = ThisWorkbook.Path & "\Outputs"
    If Dir(outputFolderDir, vbDirectory) = "" Then
        MkDir outputFolderDir ' Create the Outputs folder if it doesn't exist
    End If
    
    ' Construct the full CSV file path
    csvFilePath = outputFolderDir & "\Sorted_Transactions_" & year_month & "_mod.csv"
    
    ' Open the CSV file for writing
    fileNumber = FreeFile
    Open csvFilePath For Output As #fileNumber
    
    ' Write the custom header row
    Print #fileNumber, "DATE,AMOUNT,DESCRIPTION,INSTITUTION,CATEGORY"
    
    ' Write each row in the table to the CSV in the required format
    For Each row In tbl.ListRows
        Print #fileNumber, _
            Format(row.Range(1, 1).Value, "yyyy-mm-dd") & "," & _
            row.Range(1, 2).Value & "," & _
            row.Range(1, 3).Text & "," & _
            row.Range(1, 4).Text & "," & _
            row.Range(1, 5).Text
    Next row
    
    ' Close the CSV file
    Close #fileNumber
    
    MsgBox "CSV file saved as " & csvFilePath, vbInformation
End Sub

