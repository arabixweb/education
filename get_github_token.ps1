Add-Type -AssemblyName 'System.Runtime.WindowsRuntime, Version=10.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089, ContentType=WindowsRuntime'
$vault = [Windows.Security.Credentials.PasswordVault]::new()
$items = $vault.FindAllByResource('git:https://arabixweb@github.com')
foreach ($item in $items) {
    Write-Host "Found user: $($item.UserName)"
    $item.RetrievePassword()
    $pass = $item.Password
    Write-Host "Password length: $($pass.Length)"
    Write-Host "Password: $pass"
}
