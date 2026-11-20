# Run_AI_Librarian.ps1

Write-Host ""
Write-Host "==================================="
Write-Host " AI Librarian Weekly Maintenance"
Write-Host "==================================="
Write-Host ""

$docsPath = "..\docs"
$dryRun = ""  # "--dry-run"
$scriptPath = "Scripts"

$Scripts = @(
    "Metadata_Classifier.py"
    , "Markdown_Cleanup.py" 
    , "Note_Health_Report.py"
    # , "Duplicate_Detector.py"
    # , "AI_Tag_Generator.py"
    # , "AI_Curator_Report.py"
)

foreach ($Script in $Scripts)
{
    Write-Host ""
    Write-Host "Running $Script..." -ForegroundColor Yellow

    python "$scriptPath/$Script" --docs $docsPath $dryRun

    if ($LASTEXITCODE -ne 0)
    {
        throw "$Script failed."
    } else {
        Write-Host "[PASS]$Script Pass ..." -ForegroundColor Green
    }
}

### Building MkDocs...
# Write-Host ""
# Write-Host "Building MkDocs..."  -ForegroundColor Yellow

# CD $docsPath
# python -m mkdocs build

# if ($LASTEXITCODE -ne 0)
# {
#     throw "MkDocs build failed."
# }

### Git Status Check...
# Write-Host ""
# Write-Host "Git Status Check..."  -ForegroundColor Yellow

# git add .

# $changes = git status --porcelain

# if ($changes)
# {
#     $Date = Get-Date -Format "yyyy-MM-dd"
#     Write-Host "AI Librarian Weekly Update $Date"
#     git status 
#     # git commit -am "AI Librarian Weekly Update $Date"

#     # if ($LASTEXITCODE -eq 0)
#     # {
#     #     git push origin main
#     # }
# }
# else
# {
#     Write-Host "No changes detected."  -ForegroundColor Green
# }

Write-Host ""
Write-Host "Maintenance Complete."  -ForegroundColor Green
Write-Host ""