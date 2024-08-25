Attribute VB_Name = "Module3"
Function GETUNIQUE(rng As Range) As Variant
    Dim dict As Object
    Dim cell As Range
    Dim key As Variant
    Dim arr() As Variant
    Dim i As Long
    
    ' Create a dictionary to store unique values
    Set dict = CreateObject("Scripting.Dictionary")
    
    ' Loop through each cell in the range
    For Each cell In rng
        key = cell.Value
        ' Add unique values to the dictionary
        If Not dict.exists(key) And Not IsEmpty(key) Then
            dict.Add key, Nothing
        End If
    Next cell
    
    ' Resize the array to the number of unique items
    ReDim arr(1 To dict.Count, 1 To 1)
    
    ' Fill the array with unique values from the dictionary
    i = 1
    For Each key In dict.keys
        arr(i, 1) = key
        i = i + 1
    Next key
    
    ' Return the array
    GETUNIQUE = arr
End Function

