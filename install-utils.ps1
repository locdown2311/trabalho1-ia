# Verifica se o script está sendo executado com privilégios de administrador
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Este script precisa ser executado como administrador"
    exit
}

# Define as URLs de download do Git e do Visual Studio Code
$gitDownloadUrl = "https://github.com/git-for-windows/git/releases/download/v2.34.1.windows.1/Git-2.34.1-64-bit.exe"
$vsCodeDownloadUrl = "https://aka.ms/win32-x64-user-stable"

# Define os nomes dos arquivos de instalação do Git e do Visual Studio Code
$gitInstallerFileName = "GitInstaller.exe"
$vsCodeInstallerFileName = "VSCodeInstaller.exe"

# Define o diretório onde os arquivos de instalação serão baixados
$tempDirectory = "$($env:USERPROFILE)\Downloads"

# Cria o diretório, caso não exista
if (-not (Test-Path $tempDirectory)) {
    New-Item -ItemType Directory -Path $tempDirectory | Out-Null
}

# Faz o download do Git e do Visual Studio Code
Invoke-WebRequest -Uri $gitDownloadUrl -OutFile "$tempDirectory\$gitInstallerFileName"
Invoke-WebRequest -Uri $vsCodeDownloadUrl -OutFile "$tempDirectory\$vsCodeInstallerFileName"

# Instala o Git
Start-Process "$tempDirectory\$gitInstallerFileName" -ArgumentList "/SILENT" -Wait

# Instala o Visual Studio Code
Start-Process "$tempDirectory\$vsCodeInstallerFileName" -ArgumentList "/VERYSILENT /NORESTART" -Wait

# Remove os arquivos de instalação baixados
Remove-Item "$tempDirectory\$gitInstallerFileName"
Remove-Item "$tempDirectory\$vsCodeInstallerFileName"
