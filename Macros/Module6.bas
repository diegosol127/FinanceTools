Attribute VB_Name = "Module6"
Sub ExportAllVBAComponents()
    Dim vbComponent As Object
    Dim exportPath As String
    Dim fileName As String

    ' Set the export path to the workbook's path
    If ThisWorkbook.Path <> "" Then
        exportPath = ThisWorkbook.Path & "\Macros\" ' Ensure there's a trailing backslash
    Else
        ' If the workbook has not been saved yet, prompt the user
        MsgBox "The workbook must be saved first. Please save the workbook before exporting VBA components.", vbExclamation
        Exit Sub
    End If

    ' Ensure the export path exists (optional)
    If Dir(exportPath, vbDirectory) = "" Then
        MkDir exportPath
    End If

    ' Loop through all components in the VBA project
    For Each vbComponent In ThisWorkbook.VBProject.VBComponents
        fileName = vbComponent.name
        Debug.Print "Exporting: " & fileName

        Select Case vbComponent.Type
            Case 1 ' vbext_ct_StdModule
                vbComponent.Export exportPath & fileName & ".bas"
                Debug.Print "Exported: " & exportPath & fileName & ".bas"
            Case 2 ' vbext_ct_ClassModule
                vbComponent.Export exportPath & fileName & ".cls"
                Debug.Print "Exported: " & exportPath & fileName & ".cls"
            Case 3 ' vbext_ct_MSForm
                vbComponent.Export exportPath & fileName & ".frm"
                Debug.Print "Exported: " & exportPath & fileName & ".frm"
            Case 100 ' vbext_ct_Document
                vbComponent.Export exportPath & fileName & ".cls"
                Debug.Print "Exported: " & exportPath & fileName & ".cls"
        End Select
    Next vbComponent

    MsgBox "VBA components exported successfully to " & exportPath & "."
End Sub

