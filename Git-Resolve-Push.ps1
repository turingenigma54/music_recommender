# PowerShell Script to resolve Git push conflicts and update remote repository

# Ensure we're on the master branch
git checkout master

# Fetch the latest changes from the remote
git fetch origin

# Try to merge the changes
$mergeResult = git merge origin/master 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Merge successful."
} else {
    Write-Host "Merge conflicts detected. Aborting merge."
    git merge --abort

    # Create a backup branch
    $backupBranch = "backup-" + (Get-Date -Format "yyyyMMddHHmmss")
    git checkout -b $backupBranch
    git checkout master

    # Pull changes
    git pull origin master

    Write-Host "Please resolve conflicts manually, then run:"
    Write-Host "git add ."
    Write-Host "git commit -m 'Resolve merge conflicts'"
    exit 1
}

# Stage all changes
git add .

# Commit changes
git commit -m "Merge remote changes and resolve conflicts"

# Try to push changes
$pushResult = git push origin master 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Push successful."
} else {
    Write-Host "Push failed. Trying to pull and rebase..."
    git pull --rebase origin master

    # Try pushing again
    $pushResult = git push origin master 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push after rebase successful."
    } else {
        Write-Host "Push still failed. Please review your changes and the remote repository."
        Write-Host "You might need to force push with 'git push -f origin master' if appropriate."
        exit 1
    }
}

Write-Host "All operations completed successfully."