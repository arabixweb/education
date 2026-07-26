Add-Type -AssemblyName System.Runtime.WindowsRuntime
$vault = New-Object Windows.Security.Credentials.PasswordVault
$items = $vault.FindAllByResource("git:https://arabixweb@github.com")
foreach ($item in $items) {
    Write-Host "User: $($item.UserName)"
    $item.RetrievePassword()
    Write-Host "Password retrieved, length: $($item.Password.Length)"
}
