# Bitbucket TMAS Integration Setup Guide

This guide provides step-by-step instructions for setting up TMAS (Trend Micro Artifact Scanner) integration with Bitbucket Pipelines.

## 📋 Prerequisites

### 1. Bitbucket Requirements
- **Bitbucket Cloud** or **Bitbucket Server** account
- **Repository with Pipelines enabled**
- **Admin access** to repository settings
- **Docker support** enabled (for container scanning)

### 2. Vision One Requirements
- **Vision One Code Security** subscription
- **TMAS API credentials** (API Key and Secret)
- **Regional endpoint** access

### 3. Technical Requirements
- **Linux-based pipeline runners** (default Atlassian images)
- **Internet connectivity** for TMAS CLI download
- **Docker service** for container scanning

## 🔧 Step 1: Enable Bitbucket Pipelines

### For New Repositories
1. Navigate to your Bitbucket repository
2. Go to **Repository settings** → **Pipelines**
3. Click **Enable Pipelines**
4. Choose **Starter pipeline** or **Skip and configure manually**

### For Existing Repositories
1. Ensure Pipelines are enabled in repository settings
2. Verify you have sufficient build minutes
3. Check Docker support is enabled if needed

## 🔑 Step 2: Configure Repository Variables

Repository variables store sensitive configuration securely.

### Navigate to Variables
1. Go to **Repository settings**
2. Select **Pipelines** → **Repository variables**
3. Add the following variables:

### Required Variables

| Variable Name | Value | Secured | Description |
|---------------|-------|---------|-------------|
| `TMAS_REGION` | `us-east-1` | ❌ | Your TMAS region |
| `TMAS_API_KEY` | `your-api-key` | ✅ | TMAS API Key |
| `TMAS_API_SECRET` | `your-secret` | ✅ | TMAS API Secret |

### Optional Variables

| Variable Name | Value | Secured | Description |
|---------------|-------|---------|-------------|
| `TMAS_ENDPOINT` | `https://api.tmas.trendmicro.com` | ❌ | Custom endpoint |
| `TMAS_TIMEOUT` | `1800` | ❌ | Scan timeout (seconds) |
| `DOCKER_REGISTRY` | `your-registry.com` | ❌ | Custom Docker registry |

### Getting TMAS Credentials

1. **Log into Vision One Console**
   ```
   https://portal.xdr.trendmicro.com/
   ```

2. **Navigate to Code Security**
   - Go to **Code Security** → **Settings**
   - Select **API Keys** tab

3. **Create New API Key**
   - Click **Add API Key**
   - Name: `Bitbucket-TMAS-Integration`
   - Permissions: `Artifact Scanning`
   - Copy **API Key** and **Secret**

4. **Note Your Region**
   - Check your Vision One region
   - Common regions: `us-east-1`, `eu-central-1`, `ap-southeast-1`

## 📄 Step 3: Add Pipeline Configuration

### Create bitbucket-pipelines.yml

Create `bitbucket-pipelines.yml` in your repository root:

```yaml
image: atlassian/default-image:4

definitions:
  services:
    docker:
      memory: 2048
  caches:
    tmas-cli: ~/.tmas-cli

pipelines:
  default:
    - step:
        name: Repository Security Scan
        script:
          # Download TMAS CLI
          - curl -L -o tmas-cli.tar.gz "https://cli.artifactscan.cloudone.trendmicro.com/tmas-cli/latest/tmas-cli_Linux_x86_64.tar.gz"
          - tar -xzf tmas-cli.tar.gz
          - chmod +x tmas
          
          # Run repository scan
          - ./tmas scan dir:$BITBUCKET_CLONE_DIR --vulnerabilities --secrets --region $TMAS_REGION
        artifacts:
          - "*.json"
```

### Advanced Pipeline Configuration

For comprehensive scanning, use the full pipeline configuration from this repository:

```bash
# Copy the complete bitbucket-pipelines.yml from this demo
cp bitbucket-pipelines.yml /path/to/your/repository/
```

## 🔧 Step 4: Configure TMAS Overrides

### Create tmas-overrides.yml

Create `tmas-overrides.yml` to customize scanning behavior:

```yaml
# Basic configuration
scan:
  verbose: true
  timeout: 1800

vulnerabilities:
  enabled: true
  severity_levels: ["critical", "high", "medium", "low"]

secrets:
  enabled: true
  rules:
    - name: "aws_access_key"
      pattern: "AKIA[0-9A-Z]{16}"
    - name: "github_token"
      pattern: "ghp_[A-Za-z0-9]{36}"

policy:
  enabled: true
  enforcement:
    block_on_critical: false  # Set to true for production
```

### Copy Complete Configuration

For advanced configuration, copy from this demo:

```bash
# Copy the complete tmas-overrides.yml from this demo
cp tmas-overrides.yml /path/to/your/repository/
```

## 🚀 Step 5: Test the Integration

### Initial Test

1. **Commit and Push**
   ```bash
   git add bitbucket-pipelines.yml tmas-overrides.yml
   git commit -m "Add TMAS security scanning"
   git push origin main
   ```

2. **Monitor Pipeline**
   - Go to **Pipelines** in Bitbucket
   - Watch the pipeline execution
   - Check for successful TMAS CLI download and scan

3. **Verify Results**
   - Check pipeline logs for scan results
   - Download artifacts to review detailed findings
   - Ensure no authentication errors

### Test Different Triggers

1. **Branch Push Test**
   ```bash
   git checkout -b feature/test-scanning
   git push origin feature/test-scanning
   ```

2. **Pull Request Test**
   - Create a pull request
   - Verify PR pipeline runs
   - Check for policy evaluation

3. **Manual Pipeline Test**
   - Go to **Pipelines** → **Run pipeline**
   - Select custom pipeline: `full-security-scan`
   - Monitor comprehensive scanning

## 🔍 Step 6: Verify Scanning Results

### Expected Outputs

#### Repository Scan
```
=== SCAN SUMMARY ===
📊 VULNERABILITY SUMMARY:
  Total Vulnerabilities: 15
  Critical: 2
  High: 5
  Medium: 8

🔐 SECRET SUMMARY:
  Total Secret Findings: 5
  Unmitigated Secrets: 3
```

#### Container Scan
```
=== CONTAINER SCAN SUMMARY ===
🐳 CONTAINER VULNERABILITIES:
  Total: 127
  Critical: 8
  High: 23

📋 SBOM GENERATION:
  ✅ Software Bill of Materials generated
```

#### Policy Evaluation
```
=== POLICY EVALUATION SUMMARY ===
📋 POLICY EVALUATION:
  Result: in-violation-of-log-and-block-rules
  Blocking Violations: 2
  Log-Only Violations: 5
```

### Troubleshooting Common Issues

#### 1. TMAS CLI Download Fails
```bash
# Check network connectivity
curl -I https://cli.artifactscan.cloudone.trendmicro.com

# Verify URL is accessible
wget --spider https://cli.artifactscan.cloudone.trendmicro.com/tmas-cli/latest/tmas-cli_Linux_x86_64.tar.gz
```

#### 2. Authentication Errors
```bash
# Verify variables are set
echo "Region: $TMAS_REGION"
echo "API Key length: ${#TMAS_API_KEY}"
echo "API Secret length: ${#TMAS_API_SECRET}"

# Test authentication
./tmas auth test --region $TMAS_REGION
```

#### 3. Docker Service Issues
```yaml
# Ensure Docker service is enabled
definitions:
  services:
    docker:
      memory: 2048  # Increase memory if needed

# In your step
- step:
    name: Container Scan
    services:
      - docker  # Enable Docker service
```

#### 4. Scan Timeouts
```yaml
# Increase timeout in tmas-overrides.yml
scan:
  timeout: 3600  # 1 hour

# Or in pipeline step
- step:
    name: Long Running Scan
    max-time: 60  # 60 minutes
```

## 🔧 Step 7: Advanced Configuration

### Conditional Scanning

Run container scans only when relevant files change:

```yaml
- step:
    name: Container Security Scan
    condition:
      changesets:
        includePaths:
          - "Dockerfile"
          - "requirements.txt"
          - "src/**"
    services:
      - docker
```

### Parallel Execution

Run multiple scans in parallel:

```yaml
- parallel:
    - step:
        name: Repository Scan
        script:
          - ./tmas scan dir:. --vulnerabilities --secrets
    - step:
        name: Container Scan
        services:
          - docker
        script:
          - docker build -t app:latest .
          - ./tmas scan docker:app:latest
```

### Artifact Management

Store scan results as artifacts:

```yaml
- step:
    name: Security Scan
    script:
      - ./tmas scan dir:. > scan-results.json
    artifacts:
      - scan-results.json
      - "*.sbom"
      - "*.sarif"
```

### Caching

Cache TMAS CLI for faster builds:

```yaml
definitions:
  caches:
    tmas-cli: ~/.tmas-cli

- step:
    name: Install TMAS CLI
    caches:
      - tmas-cli
    script:
      - mkdir -p ~/.tmas-cli
      - cp tmas ~/.tmas-cli/
```

## 🔒 Step 8: Security Best Practices

### Variable Security

1. **Mark Sensitive Variables as Secured**
   - Always secure API keys and secrets
   - Use repository variables, not environment variables in code

2. **Principle of Least Privilege**
   - Create dedicated API keys for Bitbucket
   - Limit permissions to artifact scanning only

3. **Regular Rotation**
   - Rotate API keys regularly
   - Monitor API key usage in Vision One

### Pipeline Security

1. **Validate Inputs**
   ```yaml
   script:
     - |
       if [ -z "$TMAS_API_KEY" ]; then
         echo "Error: TMAS_API_KEY not set"
         exit 1
       fi
   ```

2. **Secure Artifact Storage**
   ```yaml
   artifacts:
     - "scan-results.json"
   # Artifacts are automatically secured in Bitbucket
   ```

3. **Network Security**
   ```yaml
   # Use HTTPS endpoints only
   - curl -L https://cli.artifactscan.cloudone.trendmicro.com/...
   ```

## 📊 Step 9: Monitoring and Reporting

### Pipeline Monitoring

1. **Set up Notifications**
   - Go to **Repository settings** → **Webhooks**
   - Add webhook for pipeline failures
   - Configure Slack/email notifications

2. **Monitor Build Minutes**
   - Check **Account settings** → **Billing**
   - Monitor pipeline execution time
   - Optimize scans to reduce build time

### Reporting Integration

1. **SARIF Integration**
   ```yaml
   script:
     - ./tmas scan dir:. --format sarif > results.sarif
   artifacts:
     - results.sarif
   ```

2. **Custom Reporting**
   ```yaml
   script:
     - ./tmas scan dir:. --format json > results.json
     - python generate_report.py results.json
   artifacts:
     - results.json
     - security-report.html
   ```

## 🎯 Step 10: Production Deployment

### Production Configuration

1. **Enable Security Gates**
   ```yaml
   # In tmas-overrides.yml
   policy:
     enforcement:
       block_on_critical: true
       block_on_high: true
       block_on_secrets: true
   ```

2. **Configure Notifications**
   ```yaml
   # Add notification step
   - step:
       name: Notify Security Team
       script:
         - |
           if [ "$SCAN_RESULT" = "FAILED" ]; then
             curl -X POST $SLACK_WEBHOOK -d '{"text":"Security scan failed"}'
           fi
   ```

3. **Set up Compliance Reporting**
   ```yaml
   - step:
       name: Compliance Report
       script:
         - ./tmas scan dir:. --compliance-report
         - upload_to_compliance_system.sh
   ```

### Scaling Considerations

1. **Build Minutes Management**
   - Monitor usage across repositories
   - Optimize scan frequency
   - Use conditional scanning

2. **Resource Optimization**
   ```yaml
   definitions:
     services:
       docker:
         memory: 4096  # Increase for large images
   ```

3. **Multi-Repository Setup**
   - Use shared pipeline templates
   - Centralize TMAS configuration
   - Implement organization-wide policies

## 📚 Additional Resources

### Documentation
- [TMAS CLI Reference](https://docs.trendmicro.com/en-us/enterprise/trend-micro-artifact-scanner.aspx)
- [Bitbucket Pipelines Documentation](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)
- [Vision One Code Security](https://docs.trendmicro.com/en-us/enterprise/trend-micro-vision-one/code-security.aspx)

### Support
- **Vision One Support**: [Trend Micro Support](https://success.trendmicro.com/)
- **Bitbucket Support**: [Atlassian Support](https://support.atlassian.com/)
- **Community Forums**: [Trend Micro Community](https://community.trendmicro.com/)

### Training
- [Vision One Code Security Training](https://docs.trendmicro.com/en-us/enterprise/trend-micro-vision-one/code-security/getting-started.aspx)
- [Bitbucket Pipelines Tutorial](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)

---

**🎉 Congratulations!** You have successfully set up TMAS integration with Bitbucket Pipelines. Your repository is now protected with automated security scanning for vulnerabilities, secrets, and policy compliance.
