#!/bin/bash

# 🛡️ GitHub Branch Protection Setup Script
# This script helps configure branch protection rules for the Spaceflights project

set -e

echo "🛡️ Setting up GitHub Branch Protection Rules"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed. Please install it first:"
    echo "  brew install gh  # macOS"
    echo "  apt install gh   # Ubuntu"
    echo "  https://cli.github.com/  # Other systems"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    print_error "Not authenticated with GitHub. Please run:"
    echo "  gh auth login"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
print_info "Repository: $REPO"

echo ""
print_info "Setting up branch protection rules..."

# Configure main branch protection
echo ""
print_info "Configuring main branch protection..."

gh api repos/:owner/:repo/branches/main/protection \
    --method PUT \
    --field required_status_checks='{"strict":true,"contexts":["lint-and-format","unit-tests","integration-tests","functional-tests","docker-tests","e2e-tests"]}' \
    --field enforce_admins=true \
    --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false}' \
    --field restrictions='{"users":[],"teams":[]}' \
    --field allow_force_pushes=false \
    --field allow_deletions=false \
    --field block_creations=true \
    --field required_conversation_resolution=true \
    --field lock_branch=false \
    --field allow_fork_syncing=true

if [ $? -eq 0 ]; then
    print_status "Main branch protection configured successfully"
else
    print_error "Failed to configure main branch protection"
    exit 1
fi

# Configure develop branch protection (if exists)
echo ""
print_info "Configuring develop branch protection..."

gh api repos/:owner/:repo/branches/develop/protection \
    --method PUT \
    --field required_status_checks='{"strict":true,"contexts":["pr-validation","quick-tests","docker-build-test"]}' \
    --field enforce_admins=false \
    --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false}' \
    --field restrictions='{"users":[],"teams":[]}' \
    --field allow_force_pushes=false \
    --field allow_deletions=false \
    --field block_creations=false \
    --field required_conversation_resolution=true \
    --field lock_branch=false \
    --field allow_fork_syncing=true 2>/dev/null || print_warning "Develop branch doesn't exist or protection already configured"

echo ""
print_info "Configuring repository settings..."

# Enable vulnerability alerts
gh api repos/:owner/:repo \
    --method PATCH \
    --field vulnerability_alerts=true \
    --field allow_rebase_merge=true \
    --field allow_squash_merge=true \
    --field allow_merge_commit=true \
    --field delete_branch_on_merge=true \
    --field allow_auto_merge=true

if [ $? -eq 0 ]; then
    print_status "Repository settings updated"
else
    print_warning "Failed to update repository settings"
fi

# Create issue templates
echo ""
print_info "Creating issue templates..."

mkdir -p .github/ISSUE_TEMPLATE

# Bug report template
cat > .github/ISSUE_TEMPLATE/bug_report.yml << 'EOF'
name: 🐛 Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["bug", "needs-triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: bug-description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
      placeholder: Tell us what you see!
    validations:
      required: true

  - type: textarea
    id: reproduction-steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: A clear and concise description of what you expected to happen.
    validations:
      required: true

  - type: textarea
    id: actual-behavior
    attributes:
      label: Actual Behavior
      description: A clear and concise description of what actually happened.
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: |
        - OS: [e.g. macOS, Ubuntu]
        - Python version: [e.g. 3.11]
        - Kedro version: [e.g. 1.0.0]
        - Airflow version: [e.g. 2.8.0]
      value: |
        - OS: 
        - Python version: 
        - Kedro version: 
        - Airflow version: 
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs
      description: Please paste any relevant logs here.
      render: shell

  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our Code of Conduct
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
EOF

# Feature request template
cat > .github/ISSUE_TEMPLATE/feature_request.yml << 'EOF'
name: ✨ Feature Request
description: Suggest an idea for this project
title: "[Feature]: "
labels: ["enhancement", "needs-triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a new feature!

  - type: textarea
    id: feature-description
    attributes:
      label: Feature Description
      description: A clear and concise description of the feature you'd like to see.
    validations:
      required: true

  - type: textarea
    id: problem-statement
    attributes:
      label: Problem Statement
      description: Is your feature request related to a problem? Please describe.
      placeholder: A clear and concise description of what the problem is.
    validations:
      required: true

  - type: textarea
    id: proposed-solution
    attributes:
      label: Proposed Solution
      description: Describe the solution you'd like.
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Describe any alternative solutions or features you've considered.

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How important is this feature to you?
      options:
        - Low
        - Medium
        - High
        - Critical
    validations:
      required: true

  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our Code of Conduct
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
EOF

print_status "Issue templates created"

# Create CODEOWNERS file
echo ""
print_info "Creating CODEOWNERS file..."

cat > CODEOWNERS << 'EOF'
# Global code owners
* @giocrisraigodoy

# Pipeline-specific owners
/src/spaceflights/pipelines/ @giocrisraigodoy

# DAG-specific owners
/dags/ @giocrisraigodoy

# Docker-specific owners
/docker/ @giocrisraigodoy

# Testing-specific owners
/tests/ @giocrisraigodoy

# Configuration-specific owners
/conf/ @giocrisraigodoy

# Scripts-specific owners
/scripts/ @giocrisraigodoy
EOF

print_status "CODEOWNERS file created"

# Create SECURITY.md file
echo ""
print_info "Creating SECURITY.md file..."

cat > SECURITY.md << 'EOF'
# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **DO NOT** create a public GitHub issue
2. Email us at: security@spaceflights.com
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond to security reports within 48 hours and provide updates on the resolution process.

## Security Measures

This project implements the following security measures:

- Regular dependency updates
- Automated security scanning
- Code review requirements
- Branch protection rules
- Secure coding practices

## Security Contact

For security-related questions or concerns, please contact:
- Email: security@spaceflights.com
- GitHub: @giocrisraigodoy
EOF

print_status "SECURITY.md file created"

echo ""
print_info "Setting up GitHub Actions secrets and variables..."

# Create a script to help users set up secrets
cat > scripts/setup-secrets.md << 'EOF'
# GitHub Secrets Setup

To complete the CI/CD setup, you need to configure the following secrets in your GitHub repository:

## Required Secrets

1. Go to your repository settings
2. Navigate to "Secrets and variables" > "Actions"
3. Add the following repository secrets:

### For Docker Registry (if using private registry)
- `DOCKER_USERNAME`: Your Docker registry username
- `DOCKER_PASSWORD`: Your Docker registry password/token

### For Deployment (if using cloud providers)
- `AWS_ACCESS_KEY_ID`: AWS access key (if deploying to AWS)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `GCP_SA_KEY`: Google Cloud Service Account key (if deploying to GCP)
- `AZURE_CREDENTIALS`: Azure credentials (if deploying to Azure)

### For Notifications (optional)
- `SLACK_WEBHOOK`: Slack webhook URL for notifications
- `TEAMS_WEBHOOK`: Microsoft Teams webhook URL for notifications

## Environment Variables

You may also want to set up environment-specific variables:

### Staging Environment
- `STAGING_DB_URL`: Staging database URL
- `STAGING_API_URL`: Staging API URL

### Production Environment
- `PROD_DB_URL`: Production database URL
- `PROD_API_URL`: Production API URL

## How to Add Secrets

1. Go to your repository on GitHub
2. Click on "Settings" tab
3. In the left sidebar, click on "Secrets and variables" > "Actions"
4. Click "New repository secret"
5. Enter the secret name and value
6. Click "Add secret"

Repeat this process for all required secrets.
EOF

print_status "Secrets setup guide created"

echo ""
print_status "GitHub protection setup completed!"
echo ""
print_info "Summary of changes:"
echo "  ✅ Main branch protection configured"
echo "  ✅ Develop branch protection configured (if exists)"
echo "  ✅ Repository settings updated"
echo "  ✅ Issue templates created"
echo "  ✅ CODEOWNERS file created"
echo "  ✅ SECURITY.md file created"
echo "  ✅ Secrets setup guide created"
echo ""
print_info "Next steps:"
echo "  1. Review and commit the new files"
echo "  2. Set up repository secrets (see scripts/setup-secrets.md)"
echo "  3. Test the CI/CD pipeline by creating a pull request"
echo ""
print_warning "Note: Some settings may require repository admin permissions"
