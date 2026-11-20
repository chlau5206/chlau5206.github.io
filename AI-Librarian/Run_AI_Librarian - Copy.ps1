Write-Host "AI Librarian Weekend Maintenance"
$docsPath = "..\..\docs"

# Write-Host "Running Metadata Classifier..." -ForegroundColor Yellow
# ###########################################
# python Scripts\Metadata_Classifier.py --docs $docsPath --dry-run
# if ($LASTEXITCODE -ne 0)
# {
#     throw "[FAIL]Metadata Classifier failed"
# } else {
#     Write-Host "[PASS]Metadata Classifier Pass ..." -ForegroundColor Green
#     Write-Host " "
# }

Write-Host "Running AI Tag Generator ..." -ForegroundColor Cyan
#########################################
python Scripts\AI_Tag_Generator.py --docs $docsPath --dry-run
if ($LASTEXITCODE -ne 0)
{
    throw "[FAIL]AI Tag Generator failed"
} else {
    Write-Host "[PASS]AI Tag Generator Pass ..." -ForegroundColor Green
}

# Write-Host "Running Duplicate Detector ..." -ForegroundColor Yellow
# ##########################################
# python Scripts\Duplicate_Detector.py --docs $docsPath
# if ($LASTEXITCODE -ne 0)
# {
#     throw "[FAIL]Duplicate Detector failed"
# } else {
#     Write-Host "[PASS]Duplicate Detector Pass ..." -ForegroundColor Green
#     Write-Host " "
# }

# Write-Host "Running AI Curator Report ..." -ForegroundColor Yellow
# ##########################################
# python Scripts\AI_Curator_Report.py --docs $docsPath
# if ($LASTEXITCODE -ne 0)
# {
#     throw "[FAIL]AI Curator Report failed"
# } else {
#     Write-Host "[PASS]AI Curator Report Pass ..." -ForegroundColor Green
# }

# Write-Host "Running Note Health Report ..." -ForegroundColor Yellow
# ##########################################
# python Scripts\Note_Health_Report.py --docs $docsPath
# if ($LASTEXITCODE -ne 0)
# {
#     throw "[FAIL]Health Report failed"
# } else {
#     Write-Host "[PASS]Health Report Pass ..." -ForegroundColor Green
#     Write-Host " "
# }

# Write-Host "[git]Update notes" -ForegroundColor Yellow
# git add .

# $changes = git status --porcelain

# if ($changes)
# {
#     Write-Host "[git]commit change" -ForegroundColor Yellow
#     git commit -m "Weekly AI Librarian Update"
#     git push
# }
# else
# {
#     Write-Host "[git]No changes detected." -ForegroundColor Yellow
# }

Write-Host "[Completed] AI Librarian Weekend Maintenance" -ForegroundColor Green