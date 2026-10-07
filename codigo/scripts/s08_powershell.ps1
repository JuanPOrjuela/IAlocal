$ErrorActionPreference = "Stop"
$out = New-Object System.Collections.Generic.List[string]
function P($cmd) {
  $out.Add("PS C:\Users\juanp> $cmd")
  $__o = Invoke-Expression $cmd | Out-String -Width 200
  foreach ($l in ($__o.TrimEnd() -split "`r?`n")) { $out.Add($l) }
}
. P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
. P 'Get-Date'
. P '(Invoke-RestMethod -Uri "http://localhost:11434/api/tags").models.name'
. P '$body = @{ model = "asistente-ciberseguridad"; prompt = "¿Qué es ciberseguridad? Máximo 40 palabras."; stream = $false } | ConvertTo-Json'
. P '$r = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json; charset=utf-8" -Body $body'
. P '$r.response'
. P '"tokens: {0} | tiempo total: {1:N1} s" -f $r.eval_count, ($r.total_duration / 1e9)'
$out | Set-Content -Encoding utf8 "$PSScriptRoot\ps_api_salida.txt"
$out
