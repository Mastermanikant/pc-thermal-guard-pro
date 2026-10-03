$proc = Get-Process -Name PC_Thermal_Guard_Pro -ErrorAction SilentlyContinue
if ($proc) {
    Write-Host "Found process $($proc.Id)"
    $proc.CloseMainWindow()
}