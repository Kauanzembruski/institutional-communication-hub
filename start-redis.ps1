$ErrorActionPreference = 'Stop'
$redisDir = Join-Path $PSScriptRoot 'tools\redis\Redis-8.10.2-Windows-x64-cygwin'
$cli = Join-Path $redisDir 'redis-cli.exe'
$server = Join-Path $redisDir 'redis-server.exe'
if (-not (Test-Path -LiteralPath $server)) { throw 'Executavel Redis local ausente.' }
$previousPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$ping = & $cli -h 127.0.0.1 -p 6380 ping 2>$null
$ErrorActionPreference = $previousPreference
if ($ping -eq 'PONG') { Write-Host 'Redis ativo em 127.0.0.1:6380'; return }
Start-Process -FilePath $server -ArgumentList @('redis-local.conf') -WorkingDirectory $redisDir -WindowStyle Hidden
for ($attempt = 0; $attempt -lt 20; $attempt++) {
    Start-Sleep -Milliseconds 250
    $ErrorActionPreference = 'Continue'
    $ping = & $cli -h 127.0.0.1 -p 6380 ping 2>$null
    $ErrorActionPreference = $previousPreference
    if ($ping -eq 'PONG') { Write-Host 'Redis iniciado em 127.0.0.1:6380'; return }
}
throw 'Redis nao iniciou. Verifique redis-local.log na pasta do Redis.'
