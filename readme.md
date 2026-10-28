
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



## Stage 4: Docker Hub Publishing

- Docker Hub repository: https://hub.docker.com/r/tiwaripallavii/fest-backend
- Published tags: `1.0.0`, `1.0`
- Image digest for `1.0.0`: `sha256:82d26abc4fb18554c4ec041538f8ace554edb04385b989f3644e3a39ec2d8a34`
- Image digest for `1.0`: `sha256:82d26abc4fb18554c4ec041538f8ace554edb04385b989f3644e3a39ec2d8a34`





## Stage 5: Image Signing with Cosign

- Generated a password-protected Cosign key pair.
- Used `cosign.key` to sign the Docker image `tiwaripallavii/fest-backend` version `1.0.0` by digest.
- Used `cosign.pub` to verify the signature.
- Built and pushed version `1.0.1` without signing it.
- Verification of the unsigned `1.0.1` image returned `Error: no signatures found`, as expected.
- The private key `cosign.key` is excluded from Git using `.gitignore`. Only `cosign.pub` is included in the repository.

### AI Tools Used

- **ChatGPT:** Used to understand the assessment requirements, explain Docker and Docker Compose commands, troubleshoot container and network issues, interpret Trivy scan results, and guide Cosign signing and verification.
