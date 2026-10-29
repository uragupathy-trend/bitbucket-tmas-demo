# Bitbucket TMAS Security Scanning Demo

This repository demonstrates the integration of **Trend Micro Artifact Scanner (TMAS)** with **Bitbucket Pipelines** for comprehensive security scanning of both repositories and container images.

## 🎯 Overview

This demo showcases how to implement automated security scanning in Bitbucket using TMAS to detect:

- **Vulnerabilities** in dependencies and container images
- **Secrets** and sensitive data in source code
- **Malware** in container images
- **Policy violations** against Vision One Code Security policies
- **Software Bill of Materials (SBOM)** generation

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Bitbucket     │    │  Bitbucket       │    │  Vision One     │
│   Repository    │───▶│  Pipelines       │───▶│  Code Security  │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  TMAS CLI        │
                       │  - Repository    │
                       │  - Container     │
                       │  - Policy        │
                       └──────────────────┘
```

## 📋 Features

### Repository Scanning
- **Source code vulnerability detection**
- **Secret scanning** with custom patterns
- **Dependency analysis**
- **License compliance checking**

### Container Scanning
- **Base image vulnerability assessment**
- **Layer-by-layer analysis**
- **Malware detection**
- **SBOM generation**

### Policy Evaluation
- **Custom security policies**
- **Compliance checking**
- **Automated enforcement**
- **Violation reporting**

### Bitbucket Integration
- **Parallel pipeline execution**
- **Conditional scanning** based on file changes
- **Artifact management**
- **Pull request annotations**

## 🚀 Quick Start

### Prerequisites

1. **Bitbucket Repository** with Pipelines enabled
2. **Vision One Code Security** account
3. **TMAS API credentials** configured as repository variables

### Repository Variables Setup

Configure these variables in your Bitbucket repository settings:

```bash
# Required TMAS Configuration
TMAS_REGION=us-east-1                    # Your TMAS region
TMAS_API_KEY=your-api-key-here          # Your TMAS API key
TMAS_API_SECRET=your-api-secret-here    # Your TMAS API secret

# Optional Configuration
TMAS_ENDPOINT=https://api.tmas.trendmicro.com  # Custom endpoint if needed
```

### Pipeline Configuration

The repository includes a comprehensive `bitbucket-pipelines.yml` with multiple scanning workflows:

#### Default Pipeline
- Runs repository security scan on every push

#### Branch-Specific Pipelines
- **main**: Repository + Container scanning (parallel)
- **develop**: Repository scanning only
- **feature/***: Repository scanning only

#### Pull Request Pipeline
- Repository scanning + Policy evaluation (parallel)

#### Custom Pipelines
- **full-security-scan**: All scanning types (parallel)
- **container-scan-only**: Container scanning only
- **policy-check-only**: Policy evaluation only

## 📁 Repository Structure

```
bitbucket-tmas-demo/
├── bitbucket-pipelines.yml      # Main pipeline configuration
├── tmas-overrides.yml           # TMAS scanning configuration
├── Dockerfile                   # Container definition for scanning
├── requirements.txt             # Python dependencies (with vulnerabilities)
├── src/                         # Application source code
│   ├── app.py                   # Main Flask application
│   ├── auth.py                  # Authentication module (with secrets)
│   ├── config.py                # Configuration settings
│   ├── database.py              # Database operations
│   └── utils.py                 # Utility functions
├── docs/                        # Documentation
│   ├── SETUP_GUIDE.md          # Detailed setup instructions
│   ├── BITBUCKET_INTEGRATION.md # Bitbucket-specific integration guide
│   └── SECURITY_FINDINGS.md    # Expected security findings
└── README.md                    # This file
```

## 🔧 Pipeline Workflows

### 1. Repository Security Scan

Scans source code for vulnerabilities and secrets:

```yaml
- step:
    name: Repository Security Scan
    script:
      - ./tmas scan dir:$BITBUCKET_CLONE_DIR --vulnerabilities --secrets
```

**Detects:**
- Hardcoded API keys and passwords
- Vulnerable dependencies
- Insecure code patterns
- License violations

### 2. Container Security Scan

Builds and scans Docker images:

```yaml
- step:
    name: Container Security Scan
    services:
      - docker
    script:
      - docker build -t demo:$BITBUCKET_BUILD_NUMBER .
      - ./tmas scan docker:demo:$BITBUCKET_BUILD_NUMBER --vulnerabilities --malware --saveSBOM
```

**Detects:**
- Container vulnerabilities
- Malware in images
- Insecure configurations
- Generates SBOM

### 3. Policy Evaluation

Evaluates against Vision One policies:

```yaml
- step:
    name: Policy Evaluation
    script:
      - ./tmas scan dir:$BITBUCKET_CLONE_DIR --evaluatePolicy
```

**Evaluates:**
- Security policy compliance
- Vulnerability thresholds
- Secret detection policies
- Custom compliance rules

## 🎮 Running Scans

### Automatic Triggers

Scans run automatically on:
- **Push to any branch** → Repository scan
- **Push to main** → Repository + Container scan
- **Pull requests** → Repository scan + Policy evaluation
- **File changes** → Conditional container scanning

### Manual Triggers

Run custom pipelines manually:

1. Go to **Pipelines** in your Bitbucket repository
2. Click **Run pipeline**
3. Select branch and custom pipeline:
   - `full-security-scan` - Complete security assessment
   - `container-scan-only` - Container scanning only
   - `policy-check-only` - Policy evaluation only

### Local Testing

Test TMAS scanning locally:

```bash
# Install TMAS CLI
curl -L -o tmas-cli.tar.gz "https://cli.artifactscan.cloudone.trendmicro.com/tmas-cli/latest/tmas-cli_Linux_x86_64.tar.gz"
tar -xzf tmas-cli.tar.gz
chmod +x tmas

# Repository scan
./tmas scan dir:. --vulnerabilities --secrets --override tmas-overrides.yml

# Container scan
docker build -t demo:local .
./tmas scan docker:demo:local --vulnerabilities --malware --saveSBOM
```

## 📊 Understanding Results

### Scan Artifacts

Each pipeline run generates artifacts:
- `tmas-repository-scan-results.json` - Repository scan results
- `tmas-container-scan-results.json` - Container scan results
- `tmas-policy-evaluation-results.json` - Policy evaluation results
- `*.sbom` - Software Bill of Materials

### Result Interpretation

#### Repository Scan Results
```json
{
  "totalVulnCount": 15,
  "criticalCount": 2,
  "highCount": 5,
  "unmitigatedFindingsCount": 3
}
```

#### Container Scan Results
```json
{
  "totalVulnCount": 127,
  "criticalCount": 8,
  "highCount": 23,
  "sbom": "generated"
}
```

#### Policy Evaluation Results
```json
{
  "result": "in-violation-of-log-and-block-rules",
  "blockPolicyViolations": 2,
  "logPolicyViolations": 5
}
```

## 🔒 Security Gates

The demo includes configurable security gates:

### Demo Mode (Current)
- **Secrets detected** → ✅ Continue (log violation)
- **Critical vulnerabilities** → ✅ Continue (log violation)
- **Policy violations** → ✅ Continue (log violation)

### Production Mode (Recommended)
```yaml
# In tmas-overrides.yml
policy:
  enforcement:
    block_on_critical: true
    block_on_high: true
    block_on_secrets: true
```

## 🎯 Expected Findings

This demo repository contains intentional security issues for testing:

### Repository Findings
- **3-5 hardcoded secrets** (API keys, passwords)
- **15+ vulnerable dependencies**
- **2-3 critical vulnerabilities**
- **Multiple license violations**

### Container Findings
- **100+ vulnerabilities** (from base image and dependencies)
- **5-10 critical vulnerabilities**
- **Insecure configurations**

### Policy Violations
- **Secret detection violations**
- **Vulnerability threshold violations**
- **License compliance violations**

## 📚 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed setup instructions
- [Bitbucket Integration](docs/BITBUCKET_INTEGRATION.md) - Bitbucket-specific configuration
- [Security Findings](docs/SECURITY_FINDINGS.md) - Expected security findings
- [TMAS CLI Reference](https://docs.trendmicro.com/en-us/enterprise/trend-micro-artifact-scanner.aspx)

## 🔧 Configuration

### TMAS Override Configuration

The `tmas-overrides.yml` file controls scanning behavior:

```yaml
# Enable comprehensive scanning
vulnerabilities:
  enabled: true
  severity_levels: ["critical", "high", "medium", "low"]

secrets:
  enabled: true
  rules:
    - name: "aws_access_key"
      pattern: "AKIA[0-9A-Z]{16}"

policy:
  enabled: true
  enforcement:
    block_on_critical: false  # Demo mode
```

### Bitbucket Pipeline Configuration

Key pipeline features:

```yaml
# Parallel execution
- parallel:
    - step: Repository Scan
    - step: Container Scan

# Conditional execution
condition:
  changesets:
    includePaths:
      - "Dockerfile"
      - "requirements.txt"

# Artifact management
artifacts:
  - "*.json"
  - "*.sbom"
```

## 🚨 Troubleshooting

### Common Issues

1. **TMAS CLI Download Fails**
   ```bash
   # Check network connectivity
   curl -I https://cli.artifactscan.cloudone.trendmicro.com
   ```

2. **Authentication Errors**
   ```bash
   # Verify repository variables are set
   echo $TMAS_API_KEY
   echo $TMAS_REGION
   ```

3. **Docker Build Fails**
   ```bash
   # Check Dockerfile syntax
   docker build --dry-run .
   ```

4. **Scan Timeout**
   ```yaml
   # Increase timeout in tmas-overrides.yml
   scan:
     timeout: 3600  # 1 hour
   ```

### Debug Mode

Enable verbose logging:

```yaml
# In bitbucket-pipelines.yml
script:
  - ./tmas scan dir:. --verbose --debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with TMAS scanning
5. Submit a pull request

## 📄 License

This demo is provided under the MIT License. See LICENSE file for details.

## 🆘 Support

- **TMAS Documentation**: [Trend Micro Artifact Scanner](https://docs.trendmicro.com/en-us/enterprise/trend-micro-artifact-scanner.aspx)
- **Vision One Support**: [Trend Micro Vision One](https://success.trendmicro.com/)
- **Bitbucket Pipelines**: [Atlassian Documentation](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)

---

**⚠️ Security Notice**: This repository contains intentional security vulnerabilities for demonstration purposes. Do not use this code in production environments without proper security review and remediation.
