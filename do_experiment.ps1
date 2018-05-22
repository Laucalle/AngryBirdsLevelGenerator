For ($i=0; $i -le 15; $i++) {
Start-Job { Set-Location $using:PWD; python main.py ga_parameters.json }

Get-Job | Wait-Job
}