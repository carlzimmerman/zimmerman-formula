#!/bin/bash

echo "[*] Initiating AGPL-3.0 Prior Art Timestamp Sequence..."

# Ensure we are in a git repository
if [ -d "../../../../.git" ]; then
    # Add the newly generated Z2 batches and target metadata
    git add z2_batches/*.json
    git add sanitized_targets.json
    
    # Create the timestamped commit
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    COMMIT_MSG="Automated Z2 geometric mapping timestamp - $TIMESTAMP"
    
    git commit -m "$COMMIT_MSG"
    
    # Push to public repository
    git push origin main
    
    echo "[+] Timestamp secured. Theoretical coordinates pushed to public domain."
else
    echo "[!] Error: Not a git repository. Run 'git init' first."
fi
