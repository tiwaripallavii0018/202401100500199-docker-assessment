
## Stage 3: Trivy Vulnerability Scan

### Before and After Comparison

| Image                | CRITICAL Vulnerabilities | HIGH Vulnerabilities | Image Size |
| -------------------- | -----------------------: | -------------------: | ---------: |
| `fest-backend:0.1` |                      234 |                 2250 |    1.61 GB |
| `fest-backend:0.2` |                        0 |                   49 |     235 MB |

The `fest-backend:0.2` image uses a version-pinned slim Python base image, upgraded Python packages, and runs the application as a non-root user.

### Scan Reports

- Before scan report: `reports/trivy-before.txt`
- After scan report: `reports/trivy-after.txt`

### Evidence Screenshots

- Baseline scan: `screenshots/S3-1.png`
- Updated Dockerfile and requirements: `screenshots/S3-2.png`
- Final scan and security check: `screenshots/S3-3.png`
git status --short
