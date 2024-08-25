Attribute VB_Name = "Module2"
Function UniqueNames(inputRange As Range) As Variant
    Dim myUniqueNames() As String
    Dim cell As Range
    Dim name As String
    Dim i As Integer
    Dim isUnique As Boolean
    
    ' Initialize variables
    ReDim myUniqueNames(0)
    i = 0
    
    ' Loop through each cell in the input range
    For Each cell In inputRange
        ' Check if the value is not empty
        If cell.Value <> "" Then
            name = cell.Value
            isUnique = True
            
            ' Check if the name is already in the array
            For j = LBound(myUniqueNames) To UBound(myUniqueNames)
                If name = myUniqueNames(j) Then
                    isUnique = False
                    Exit For
                End If
            Next j
            
            ' If the name is unique, add it to the array
            If isUnique Then
                ReDim Preserve myUniqueNames(i)
                myUniqueNames(i) = name
                i = i + 1
            End If
        End If
    Next cell
    
    ' Return the array of unique names
    If i > 0 Then
        UniqueNames = Application.Transpose(myUniqueNames)
    Else
        UniqueNames = ""
    End If
End Function

