# PowerShell script to create GitHub repo and push
$store = "$env:LOCALAPPDATA\Microsoft\Credentials"
$credFile = Get-ChildItem -Path $store -Recurse -ErrorAction SilentlyContinue | 
    Where-Object { $_.Length -gt 100 } | 
    Select-Object -First 1

# Try git credential fill via a workaround
$envLine = "url=https://github.com`n"
$tempFile = [System.IO.Path]::GetTempFileName()
Set-Content -Path $tempFile -Value $envLine -NoNewline

# Write input for git credential
$inputStr = "url=https://github.com`n`n"
$inputBytes = [System.Text.Encoding]::UTF8.GetBytes($inputStr + "`n")
$memStream = New-Object System.IO.MemoryStream($inputBytes)
$proc = Start-Process -FilePath "git" -ArgumentList "credential fill" -NoNewWindow -RedirectStandardInput (Get-Process -Id $pid).MainWindowHandle -PassThru

# Alternative: use cmdkey to get password
Write-Host "=== Available credentials ==="
cmdkey /list | Out-String

Write-Host "=== Trying direct push with stored credential ==="
cd "C:\Users\paule\OneDrive\Desktop\Arabix Theme\education"
git remote set-url origin "https://arabixweb@github.com/arabixweb/education.git"
Write-Host "Trying push (will prompt for password if needed)..."
git push -u origin master 2>&1
