# Collect application logs from the Event Viewer
$appLogs = Get-EventLog -LogName Application -EntryType Error -Newest 50

# Convert logs to a simple string for Python to analyze
$logText = $appLogs | Out-String

# Save the log text to a temporary file
$tempFile = [System.IO.Path]::GetTempFileName()
$logText | Out-File -FilePath $tempFile

# Call the Python script, passing the path of the temporary file
& python "AnalyzeLogs.py" $tempFile

# Clean up the temporary file
Remove-Item -Path $tempFile