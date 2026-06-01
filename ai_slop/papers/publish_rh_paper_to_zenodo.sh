#!/bin/bash
# Zenodo Publication Script for RH Symmetry-Identity Gap Paper
# Author: Carl Zimmerman
# License: CC BY-SA 4.0

# Configuration
ZIP_FILE="/Users/carlzimmerman/new_physics/zimmerman-formula/papers/RH_Symmetry_Identity_Gap_Zenodo.zip"
PAPER_TITLE="The Symmetry-Identity Gap: A Structural Synthesis of Frontier Approaches to the Riemann Hypothesis"
AUTHOR_NAME="Zimmerman, Carl"

# Check for token
if [ -z "$ZENODO_TOKEN" ]; then
    echo "ERROR: ZENODO_TOKEN environment variable not set"
    echo ""
    echo "To get a token:"
    echo "1. Go to https://zenodo.org/account/settings/applications/tokens/new/"
    echo "2. Create a token with 'deposit:write' and 'deposit:actions' scopes"
    echo "3. Run: export ZENODO_TOKEN='your_token_here'"
    echo "4. Then run this script again"
    exit 1
fi

ZENODO_URL="https://zenodo.org"

echo "=== Zenodo Publication Script ==="
echo "IMPORTANT: This paper documents RH approaches - RH REMAINS UNSOLVED"
echo ""

# Step 1: Create a new deposition
echo "Step 1: Creating new deposition..."
RESPONSE=$(curl -s -X POST "$ZENODO_URL/api/deposit/depositions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ZENODO_TOKEN" \
    -d '{}')

DEPOSITION_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
BUCKET_URL=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['links']['bucket'])" 2>/dev/null)

if [ -z "$DEPOSITION_ID" ]; then
    echo "ERROR: Failed to create deposition"
    echo "Response: $RESPONSE"
    exit 1
fi

echo "Deposition ID: $DEPOSITION_ID"
echo "Bucket URL: $BUCKET_URL"

# Step 2: Upload the zip file
echo ""
echo "Step 2: Uploading paper package..."

FILENAME=$(basename "$ZIP_FILE")
curl -s --upload-file "$ZIP_FILE" "$BUCKET_URL/$FILENAME?access_token=$ZENODO_TOKEN"
echo "  Uploaded: $FILENAME"

echo "Upload complete"

# Step 3: Add metadata
echo ""
echo "Step 3: Adding metadata..."

METADATA='{
  "metadata": {
    "title": "'"$PAPER_TITLE"'",
    "upload_type": "publication",
    "publication_type": "article",
    "description": "IMPORTANT: The Riemann Hypothesis REMAINS UNSOLVED. This paper presents a structural synthesis of frontier approaches to RH, demonstrating that current mathematics can generate the functional equation symmetry but lacks the geometric substrate to collapse this symmetry into an identity. We identify the Positivity Bedrock: every approach (Connes NCG, Motives, SUSY, Fargues-Fontaine) requires proving a positivity condition equivalent to knowing the zeros. We propose a Scholze-Connes hybrid architecture combining condensed mathematics with non-commutative geometry, reducing RH to ampleness of a scaling bundle. Despite sophisticated reformulations, circularity persists. Architecture: 100% complete. Proof of RH: 0% complete.",
    "creators": [
      {
        "name": "'"$AUTHOR_NAME"'"
      }
    ],
    "access_right": "open",
    "license": "cc-by-sa-4.0",
    "keywords": [
      "Riemann Hypothesis",
      "Condensed Mathematics",
      "Non-Commutative Geometry",
      "Fargues-Fontaine Curve",
      "Positivity",
      "Scholze",
      "Connes",
      "Number Theory",
      "Mathematics",
      "UNSOLVED"
    ],
    "notes": "DISCLAIMER: The Riemann Hypothesis remains an open problem. This paper is a structural survey, not a proof.",
    "version": "1.0",
    "related_identifiers": [
      {
        "identifier": "https://github.com/carlzimmerman/zimmerman-formula",
        "relation": "isSupplementedBy",
        "resource_type": "software"
      }
    ]
  }
}'

METADATA_RESPONSE=$(curl -s -X PUT "$ZENODO_URL/api/deposit/depositions/$DEPOSITION_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ZENODO_TOKEN" \
    -d "$METADATA")

echo "Metadata added"

# Step 4: Publish
echo ""
echo "Step 4: Publishing..."
echo ""
echo "*** REMINDER: This paper does NOT solve RH - it maps existing approaches ***"
echo ""
read -p "Ready to publish? This will create a permanent DOI. (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Publication cancelled."
    echo "Your draft is saved at: $ZENODO_URL/deposit/$DEPOSITION_ID"
    exit 0
fi

PUBLISH_RESPONSE=$(curl -s -X POST "$ZENODO_URL/api/deposit/depositions/$DEPOSITION_ID/actions/publish" \
    -H "Authorization: Bearer $ZENODO_TOKEN")

DOI=$(echo $PUBLISH_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('doi', 'N/A'))" 2>/dev/null)
RECORD_URL=$(echo $PUBLISH_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['links']['record_html'])" 2>/dev/null)

echo ""
echo "=== PUBLICATION COMPLETE ==="
echo ""
echo "DOI: $DOI"
echo "URL: $RECORD_URL"
echo ""
echo "Paper published to Zenodo under Creative Commons CC-BY-SA 4.0"
echo "Author: Carl Zimmerman"
echo ""
echo "NOTE: The Riemann Hypothesis remains an UNSOLVED problem in mathematics."
