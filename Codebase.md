# TIMSAdvantaged Codebase

Generated: 10/17/2026 14:27:15

---

## Table of Contents

- .gitignore
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\.platform
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\alm.settings.json
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\lakehouse.metadata.json
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\shortcuts.metadata.json
- britam_claims_lakehouse\Readme.md
- Generate-Codebook-TIMSAdvantaged.ps1
- Readme.md
- requirements.txt
- scripts\generate_data.py

---


<div style='page-break-after: always;'></div>

# File: .gitignore

```gitignore

# Python
__pycache__/
*.py[cod]
*.class
*.so
.Python
env/
venv/
.venv/

# Jupyter / Fabric Notebooks
.ipynb_checkpoints/

# Data (We will commit the small synthetic CSVs, but ignore large/real data)
*.parquet
*.db
!data/claims_batch_1.csv
!data/claims_batch_2.csv

# OS
.DS_Store
Thumbs.db


```


<div style='page-break-after: always;'></div>

# File: britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\.platform

```platform
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Lakehouse",
    "displayName": "britam_claims_lakehouse"
  },
  "config": {
    "version": "2.0",
    "logicalId": "6692d188-b2f5-b189-4a2d-5b6f01c2b3de"
  }
}
```


<div style='page-break-after: always;'></div>

# File: britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\alm.settings.json

```json
{
  "version": "1.0.1",
  "objectTypes": [
    {
      "name": "Shortcuts",
      "state": "Enabled",
      "subObjectTypes": [
        {
          "name": "Shortcuts.OneLake",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.AdlsGen2",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.Dataverse",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.AmazonS3",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.S3Compatible",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.GoogleCloudStorage",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.AzureBlobStorage",
          "state": "Enabled"
        },
        {
          "name": "Shortcuts.OneDriveSharePoint",
          "state": "Enabled"
        }
      ]
    },
    {
      "name": "DataAccessRoles",
      "state": "Disabled"
    }
  ]
}
```


<div style='page-break-after: always;'></div>

# File: britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\lakehouse.metadata.json

```json
{"defaultSchema":"dbo"}
```


<div style='page-break-after: always;'></div>

# File: britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\shortcuts.metadata.json

```json
[]
```


<div style='page-break-after: always;'></div>

# File: britam_claims_lakehouse\Readme.md

```md
This is an auto-created file for britam_claims_lakehouse
```


<div style='page-break-after: always;'></div>

# File: Generate-Codebook-TIMSAdvantaged.ps1

```ps1
<#
.EXAMPLE
.\Generate-Codebook-TIMSAdvantaged.ps1 -ProjectPath "C:\Data\britam-claims-analytics-fabric"
#>

param(
    [string]$ProjectPath = (Get-Location).Path,
    [switch]$GeneratePdf
)

# ============================================================
# Configuration
# ============================================================

$Root = (Resolve-Path $ProjectPath).Path

$MarkdownFile = Join-Path $Root "Codebase.md"
$PdfFile      = Join-Path $Root "Codebase.pdf"

# 1. Directories to completely ignore (Added TIMS specific folders)
$ExcludedDirectories = @(
    ".git", ".github", ".idea", ".vscode", ".cursor",
    "node_modules", "venv", ".venv", "env", "Lib", "Include", "site-packages",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov",
    "coverage", "dist", "build", "bin", "obj", "out", ".next",
    "migrations", "trash", "staticfiles", "media",
    ".cache", ".data", ".logs", ".reports" 
)

# 2. File extensions to ignore (Added Excel, Certs, CSVs)
$ExcludedExtensions = @(
    ".png",".jpg",".jpeg",".gif",".bmp",".ico",".svg",".webp",".avif",
    ".pdf",".zip",".7z",".rar",".tar",".gz",
    ".exe",".dll",".so",".dylib",".pyd",
    ".woff",".woff2",".ttf",".eot",
    ".pyc",".pyo",".class",
    ".db",".sqlite3",".sqlite",".log",
    ".map", ".mo", ".lock", ".pth", ".bak", ".tmp",
    ".xlsx", ".xls", ".csv", ".pem", ".crt", ".key", ".tpl", ".mp4", ".pbix"
)

# 3. Specific files to ignore (CRITICAL: Added .secrets.toml for security)
$ExcludedFiles = @(
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Pipfile.lock",
    "poetry.lock",
    "db.sqlite3",
    ".secrets.toml", 
    "Codebase.md",
    "Codebase.pdf"
)

# Delete old markdown if it exists
if (Test-Path $MarkdownFile) {
    Remove-Item $MarkdownFile -Force
}

# ============================================================
# Helper Function
# ============================================================

function Add-Line {
    param([string]$Text)
    Add-Content -Path $MarkdownFile -Value $Text -Encoding UTF8
}

# ============================================================
# Scan Files
# ============================================================

Write-Host ""
Write-Host "Scanning TIMSAdvantaged repository..."
Write-Host ""

$Files = Get-ChildItem -Path $Root -Recurse -File | Where-Object {
    $relative = $_.FullName.Substring($Root.Length).TrimStart('\', '/')
    $fileName = $_.Name

    # Check Directories (Windows and Linux/Mac path separators)
    $pathParts = $relative -split '[\\/]'
    foreach ($dir in $ExcludedDirectories) {
        if ($pathParts -contains $dir) {
            return $false
        }
    }

    # Check Extensions
    if ($ExcludedExtensions -contains $_.Extension.ToLower()) {
        return $false
    }

    # Check Exact Filenames
    if ($ExcludedFiles -contains $fileName) {
        return $false
    }

    return $true

} | Sort-Object FullName

Write-Host "Found $($Files.Count) valid source code files."
Write-Host ""

# ============================================================
# Markdown Header
# ============================================================

Add-Line "# TIMSAdvantaged Codebase"
Add-Line ""
Add-Line "Generated: $(Get-Date)"
Add-Line ""
Add-Line "---"
Add-Line ""

# ============================================================
# Table of Contents
# ============================================================

Add-Line "## Table of Contents"
Add-Line ""

foreach ($file in $Files) {
    $relative = $file.FullName.Substring($Root.Length).TrimStart('\', '/')
    Add-Line "- $relative"
}

Add-Line ""
Add-Line "---"
Add-Line ""

# ============================================================
# Add Every File
# ============================================================

$index = 1

foreach ($file in $Files) {
    $relative = $file.FullName.Substring($Root.Length).TrimStart('\', '/')

    Write-Host "[$index/$($Files.Count)] $relative"

    $language = $file.Extension.TrimStart('.')
    if ([string]::IsNullOrWhiteSpace($language)) { $language = "text" }
    
    # Map specific extensions to markdown code block languages
    switch ($language) {
        "py" { $language = "python" }
        "js" { $language = "javascript" }
        "ts" { $language = "typescript" }
        "tsx" { $language = "tsx" }
        "jsx" { $language = "jsx" }
        "yml" { $language = "yaml" }
        "sh" { $language = "bash" }
        "toml" { $language = "toml" }
    }

    Add-Line ""
    Add-Line "<div style='page-break-after: always;'></div>"
    Add-Line ""
    Add-Line "# File: $relative"
    Add-Line ""
    Add-Line ('```' + $language)

    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        Add-Content -Path $MarkdownFile -Value $content -Encoding UTF8
    }
    catch {
        Add-Line "[Unable to read file.]"
    }

    Add-Line '```'
    Add-Line ""
    $index++
}

Write-Host ""
Write-Host "Markdown created successfully!"
Write-Host $MarkdownFile



# ============================================================
# Optional PDF Generation
# ============================================================

if ($GeneratePdf) {

    $Pandoc = Get-Command pandoc -ErrorAction SilentlyContinue

    if ($Pandoc) {

        Write-Host ""
        Write-Host "Generating PDF..."

        & pandoc `
            $MarkdownFile `
            -o $PdfFile `
            --toc `
            --highlight-style=tango

        Write-Host ""
        Write-Host "PDF created:"
        Write-Host $PdfFile

    }
    else {

        Write-Host ""
        Write-Host "Pandoc was not found."
        Write-Host ""
        Write-Host "Install it from:"
        Write-Host "https://pandoc.org/installing.html"

    }

}
```


<div style='page-break-after: always;'></div>

# File: Readme.md

```md
First Update via feature branch
```


<div style='page-break-after: always;'></div>

# File: requirements.txt

```txt
pandas>=2.0.0
numpy>=1.24.0

```


<div style='page-break-after: always;'></div>

# File: scripts\generate_data.py

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_claims_data(num_records, start_id, batch_id, start_date):
    np.random.seed(42)
    random.seed(42)
    
    claim_ids = [f"CLM-{str(i).zfill(5)}" for i in range(start_id, start_id + num_records)]
    policy_ids = [f"POL-{str(random.randint(10000, 99999))}" for _ in range(num_records)]
    
    # Generate dates within the last 2 years
    dates = [start_date - timedelta(days=random.randint(0, 730)) for _ in range(num_records)]
    date_strings = [d.strftime('%Y-%m-%d') for d in dates]
    
    # Categories (with intentional casing messiness for cleaning demo)
    categories = ['Sedan', 'SUV', 'Truck', 'Motorcycle', 'Van']
    messy_categories = [random.choice(categories) for _ in range(num_records)]
    for i in range(int(num_records * 0.05)): # 5% messy
        idx = random.randint(0, num_records - 1)
        messy_categories[idx] = messy_categories[idx].lower()
    if num_records > 100:
        messy_categories[5] = "S.U.V" # Edge case
    
    # Regions (Kenya-specific for Britam relevance)
    regions = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Nyeri']
    region_choices = [random.choice(regions) for _ in range(num_records)]
    
    # Claim amounts (Log-normal distribution to mimic real insurance skew)
    amounts = np.round(np.random.lognormal(mean=9.5, sigma=0.8, size=num_records), 2)
    
    # Status (with intentional typos for cleaning demo)
    statuses = ['Approved', 'Pending', 'Rejected', 'Under Review']
    messy_statuses = [random.choice(statuses) for _ in range(num_records)]
    for i in range(int(num_records * 0.03)): # 3% typos
        idx = random.randint(0, num_records - 1)
        if messy_statuses[idx] == 'Pending':
            messy_statuses[idx] = 'Pendng'
        elif messy_statuses[idx] == 'Approved':
            messy_statuses[idx] = 'Aproved'

    # Fraud flag (15% probability, slightly higher for certain regions/categories)
    fraud_flags = []
    for i in range(num_records):
        base_prob = 0.05
        if region_choices[i] == 'Nairobi' and messy_categories[i].upper() == 'SUV':
            base_prob = 0.15
        fraud_flags.append(1 if random.random() < base_prob else 0)
        
    # Introduce missing values in claim_amount (~5%)
    for i in range(int(num_records * 0.05)):
        idx = random.randint(0, num_records - 1)
        amounts[idx] = np.nan

    batch_ids = [batch_id] * num_records

    df = pd.DataFrame({
        'claim_id': claim_ids,
        'policy_id': policy_ids,
        'claim_date': date_strings,
        'vehicle_category': messy_categories,
        'region': region_choices,
        'claim_amount': amounts,
        'claim_status': messy_statuses,
        'is_fraud_flag': fraud_flags,
        'batch_id': batch_ids
    })
    
    return df

if __name__ == "__main__":
    print("Generating Batch 1 (1,200 records)...")
    df_batch1 = generate_claims_data(
        num_records=1200, 
        start_id=1001, 
        batch_id=1, 
        start_date=datetime(2026, 10, 17)
    )
    df_batch1.to_csv('data/claims_batch_1.csv', index=False)
    print("Saved: data/claims_batch_1.csv")

    print("Generating Batch 2 (300 records for incremental update demo)...")
    df_batch2 = generate_claims_data(
        num_records=300, 
        start_id=2201, 
        batch_id=2, 
        start_date=datetime(2026, 10, 17)
    )
    df_batch2.to_csv('data/claims_batch_2.csv', index=False)
    print("Saved: data/claims_batch_2.csv")
    
    print("\nDataset generation complete! Total records: 1,500")
```

