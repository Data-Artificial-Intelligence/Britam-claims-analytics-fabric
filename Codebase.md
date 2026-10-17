# TIMSAdvantaged Codebase

Generated: 10/17/2026 23:18:35

---

## Table of Contents

- .gitignore
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\.platform
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\alm.settings.json
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\lakehouse.metadata.json
- britam_claims_lakehouse\britam_claims_lakehouse.Lakehouse\shortcuts.metadata.json
- britam_claims_lakehouse\Readme.md
- docs\architecture.html
- Generate-Codebook-TIMSAdvantaged.ps1
- Readme.md
- requirements.txt
- scripts\generate_data.py
- tests\__init__.py
- tests\test_data_generation.py

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

# File: docs\architecture.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Britam Claims Analytics - Architecture</title>
<style>
  :root{
    --ink:#0f172a; --muted:#64748b; --line:#e2e8f0; --bg:#f1f5f9;
    --t1:#4f46e5; --t2:#0d9488; --t3:#7c3aed; --t4:#ea580c; --gov:#334155;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);padding:32px;display:flex;justify-content:center}
  .card{background:#fff;width:1280px;max-width:100%;border-radius:18px;box-shadow:0 10px 40px rgba(15,23,42,.12);padding:34px 38px;border:1px solid var(--line)}
  .head{display:flex;align-items:baseline;justify-content:space-between;border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:22px}
  .head h1{font-size:22px;letter-spacing:.2px}
  .head .sub{font-size:12px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:1px}
  .layout{display:flex;gap:18px;align-items:stretch}
  .stack{flex:1;display:flex;flex-direction:column}
  .tier{border:1px solid var(--line);border-left:6px solid var(--c);border-radius:12px;padding:14px 16px;background:#fff}
  .tier .tag{display:inline-block;font-size:10px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:#fff;background:var(--c);padding:3px 9px;border-radius:20px;margin-bottom:10px}
  .boxes{display:flex;gap:12px;flex-wrap:wrap}
  .box{flex:1;min-width:150px;border:1px solid var(--line);border-radius:9px;padding:10px 12px;background:#f8fafc}
  .box b{display:block;font-size:13px;margin-bottom:3px}
  .box span{display:block;font-size:11px;color:var(--muted);line-height:1.45}
  .chip{margin-top:9px;display:inline-block;font-size:11px;font-weight:700;color:var(--c);background:color-mix(in srgb,var(--c) 12%,#fff);border:1px solid color-mix(in srgb,var(--c) 30%,#fff);padding:3px 10px;border-radius:7px}
  .arrow{align-self:center;text-align:center;color:var(--muted);font-size:11px;font-weight:700;letter-spacing:.4px;padding:6px 0}
  .arrow .v{display:block;font-size:16px;color:var(--ink);line-height:1}
  .gov{width:230px;border:1px dashed var(--gov);border-radius:12px;padding:14px;background:#f8fafc;display:flex;flex-direction:column}
  .gov .tag{align-self:flex-start;font-size:10px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#fff;background:var(--gov);padding:3px 9px;border-radius:20px;margin-bottom:10px}
  .gov ul{list-style:none;display:flex;flex-direction:column;gap:8px}
  .gov li{font-size:11.5px;line-height:1.4;padding-left:16px;position:relative;color:#1e293b}
  .gov li:before{content:"";position:absolute;left:0;top:5px;width:7px;height:7px;border-radius:2px;background:var(--gov)}
  .foot{margin-top:18px;padding-top:12px;border-top:1px solid var(--line);font-size:11px;color:var(--muted);display:flex;justify-content:space-between}
  .t1{--c:var(--t1)} .t2{--c:var(--t2)} .t3{--c:var(--t3)} .t4{--c:var(--t4)}
</style>
</head>
<body>
  <div class="card">
    <div class="head">
      <h1>Motor Claims Analytics &mdash; End-to-End Architecture</h1>
      <div class="sub">Microsoft Fabric &middot; Lakehouse &middot; PySpark &middot; DirectLake</div>
    </div>

    <div class="layout">
      <div class="stack">

        <!-- TIER 1 -->
        <div class="tier t1">
          <span class="tag">1 &middot; Local Dev &amp; Source Control</span>
          <div class="boxes">
            <div class="box"><b>VS Code + Python venv</b><span>requirements.txt pinned &middot; reproducible build</span></div>
            <div class="box"><b>generate_data.py</b><span>Synthetic motor claims &middot; intentional messiness (casing, typos, nulls)</span></div>
            <div class="box"><b>GitHub &middot; branch protection</b><span>main &#8656; develop &#8656; fabric-integration &middot; PR + code review</span></div>
          </div>
        </div>
        <div class="arrow"><span class="v">&#9660;</span>commit &amp; auto-sync</div>

        <!-- TIER 2 -->
        <div class="tier t2">
          <span class="tag">2 &middot; Ingestion &amp; Storage (Fabric)</span>
          <div class="boxes">
            <div class="box"><b>Lakehouse: britam_claims_lakehouse</b><span>OneLake &middot; raw CSV staged in Files/ &middot; open Delta Parquet format</span></div>
          </div>
          <span class="chip">Batch 1 = 1,200 &nbsp;|&nbsp; Batch 2 = 300</span>
        </div>
        <div class="arrow"><span class="v">&#9660;</span>read Files/ via PySpark</div>

        <!-- TIER 3 -->
        <div class="tier t3">
          <span class="tag">3 &middot; Transformation &amp; Orchestration</span>
          <div class="boxes">
            <div class="box"><b>Notebook 01_data_cleaning...</b><span>clean_claims_data(): upper&middot;trim &middot; typo map &middot; coalesce nulls &middot; date cast &middot; claim_severity feature</span></div>
            <div class="box"><b>Delta Lake MERGE (upsert)</b><span>match on claim_id &middot; idempotent &middot; ACID &middot; no duplicate on retry</span></div>
          </div>
          <span class="chip">&#8594; 1,500 validated records &middot; 2 batches</span>
        </div>
        <div class="arrow"><span class="v">&#9660;</span>managed Delta table</div>

        <!-- TIER 4 -->
        <div class="tier t4">
          <span class="tag">4 &middot; Semantic Layer &amp; BI</span>
          <div class="boxes">
            <div class="box"><b>DirectLake Semantic Model</b><span>britam_claims_semantic_model &middot; queries Delta in-place &middot; zero import</span></div>
            <div class="box"><b>Power BI Executive Dashboard</b><span>DAX: Fraud Rate 5.4% &middot; Avg Severity &middot; region / category / status &middot; date slicer</span></div>
          </div>
        </div>

      </div>

      <!-- GOVERNANCE RAIL -->
      <div class="gov">
        <span class="tag">Governance &amp; Quality</span>
        <ul>
          <li>Peer-reviewed code via protected branches &amp; PRs</li>
          <li>Data-quality exception queue for null financials</li>
          <li>PII masking &middot; ODPC / Data Protection Act</li>
          <li>Row-Level Security by region</li>
          <li>Lineage &amp; audit trail (OneLake + Git)</li>
          <li>Reproducible, version-controlled pipelines</li>
        </ul>
      </div>
    </div>

    <div class="foot">
      <span>Antony Henry Oduor Onyango &middot; Data Scientist Candidate</span>
      <span>Britam General Insurance &middot; Assessment &middot; 22 Oct 2026</span>
    </div>
  </div>
</body>
</html>
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
## 📊 Britam claims analytics fabric architecture

### Mermaid Architecture Diagram
![Architecture](images/mermaid_architecture.png)

### HTML Architecture Diagram
![Architecture](images/html_architecture.png)
![Open this file in a browser](docs/architecture.html)
```


<div style='page-break-after: always;'></div>

# File: requirements.txt

```txt
pandas>=2.0.0
numpy>=1.24.0
pytest>=7.0.0
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


<div style='page-break-after: always;'></div>

# File: tests\__init__.py

```python
```


<div style='page-break-after: always;'></div>

# File: tests\test_data_generation.py

```python
"""
Unit tests for synthetic motor claims data generation.
Validates that generated datasets meet interview requirements:
- Minimum 1,000 total records
- Required schema columns present
- Date and category columns exist
- Incremental update capability (batch_id column)
"""

import os
import sys
import pandas as pd


def test_data_files_exist():
    """Verify that the generation script produced the expected CSV files."""
    batch1_path = 'data/claims_batch_1.csv'
    batch2_path = 'data/claims_batch_2.csv'
    
    assert os.path.exists(batch1_path), f"❌ FAIL: {batch1_path} not found!"
    assert os.path.exists(batch2_path), f"❌ FAIL: {batch2_path} not found!"
    print(f"✅ PASS: Both CSV files exist.")


def test_row_counts():
    """Verify the dataset meets the interview requirement (>1,000 records total)."""
    df1 = pd.read_csv('data/claims_batch_1.csv')
    df2 = pd.read_csv('data/claims_batch_2.csv')
    
    # Check Batch 1 (Expect 1200)
    assert len(df1) == 1200, f"❌ FAIL: Expected 1200 rows in Batch 1, got {len(df1)}"
    
    # Check Batch 2 (Expect 300)
    assert len(df2) == 300, f"❌ FAIL: Expected 300 rows in Batch 2, got {len(df2)}"
    
    total_rows = len(df1) + len(df2)
    assert total_rows >= 1000, f"❌ FAIL: Total rows ({total_rows}) must be >= 1000"
    
    print(f"✅ PASS: Row counts verified (Total: {total_rows}).")


def test_schema_integrity():
    """Ensure critical columns required by the brief are present."""
    df = pd.read_csv('data/claims_batch_1.csv')
    required_cols = [
        'claim_id', 
        'policy_id', 
        'claim_date',      # At least one date column ✓
        'vehicle_category', # At least one category column ✓
        'region', 
        'claim_amount',
        'claim_status',
        'is_fraud_flag',
        'batch_id'          # For incremental updates ✓
    ]
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise AssertionError(f"❌ FAIL: Missing required columns: {missing}")
        
    print("✅ PASS: Schema integrity verified (all 9 required columns present).")


def test_incremental_update_capability():
    """Verify that batch_id exists and supports incremental loading logic."""
    df1 = pd.read_csv('data/claims_batch_1.csv')
    df2 = pd.read_csv('data/claims_batch_2.csv')
    
    # All Batch 1 records should have batch_id = 1
    assert (df1['batch_id'] == 1).all(), "❌ FAIL: Batch 1 records do not all have batch_id=1"
    
    # All Batch 2 records should have batch_id = 2
    assert (df2['batch_id'] == 2).all(), "❌ FAIL: Batch 2 records do not all have batch_id=2"
    
    # Verify no overlapping claim_ids between batches (critical for merge/upsert safety)
    overlap = set(df1['claim_id']).intersection(set(df2['claim_id']))
    assert len(overlap) == 0, f"❌ FAIL: Found {len(overlap)} duplicate claim_ids across batches!"
    
    print("✅ PASS: Incremental update capability verified (unique batch_ids, no ID overlaps).")


if __name__ == "__main__":
    try:
        test_data_files_exist()
        test_row_counts()
        test_schema_integrity()
        test_incremental_update_capability()
        print("\n🎉 ALL TESTS PASSED! Pipeline is healthy.")
        sys.exit(0)
    except AssertionError as e:
        print(e)
        sys.exit(1)
```

