# PowerShell snippet leveraging RoboCopy with parallel thread orchestration
# Designed for ultra-fast migration of massive GIS datasets (SHAPE/OTA/Layer)

$Source = "K:\PROJECT_SERVER\SHAPE"
$Dest   = "C:\LOCAL_STAGING\SHAPE"
$MaxParallel = 6  # Number of simultaneous folder operations
$RoboThreads = 8  # Parallel threads per RoboCopy process (total 48 threads)

# Building a dynamic task list using PSCustomObject for traceability
$Tasks = New-Object System.Collections.Generic.List[PSCustomObject]
foreach ($code in $OTA_Codes) {
    $srcPath = Join-Path $Source $code
    if (Test-Path $srcPath) {
        $Tasks.Add([PSCustomObject]@{ 
            Src = $srcPath; 
            Dst = Join-Path $Dest $code 
        })
    }
}

# Executing Parallel Copy using the ForEach-Object -Parallel throttle limit
# Optimized for network environments (low latency, high throughput)
$Tasks | ForEach-Object -ThrottleLimit $MaxParallel -Parallel {
    $task = $_
    $threads = $using:RoboThreads
    if (Test-Path $task.Src) {
        # Ensuring destination existence with -Force
        New-Item -ItemType Directory -Path $task.Dst -Force | Out-Null
        # RoboCopy with multi-threading (/MT) and silent logging for speed
        robocopy $task.Src $task.Dst /E /MT:$threads /R:1 /W:1 /NFL /NDL /NJH /NJS | Out-Null
    }
}
