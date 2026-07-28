# GCP IAM Notes

## Core Concepts

### Permission vs Role
- Permission = right to perform a specific action
  (e.g., bigquery.tables.getData)
- Role = a set of multiple pre-packaged permissions
  (e.g., roles/bigquery.dataViewer = 4-5 read-related permissions)
- Grant a Role to a principal, not individual Permissions

### Principle of Least Privilege
- Grant only the minimum permissions necessary to perform a task
- Example in crypto pipeline: Airflow SA only needs
  bigquery.dataEditor + bigquery.jobUser + storage.objectAdmin
  No need for roles/owner or roles/editor

### Service Account vs Personal Account
- Personal account: used to manage GCP (Console, CLI)
- Service Account: used for applications and automated pipelines
- Never use personal account credentials inside code

## Why Impersonation is Needed

Problem: personal account has full permissions
→ Testing code with personal account → always passes
→ No way to know if SA has sufficient permissions

Solution: impersonate the SA
→ Code runs with the SA's permissions
→ Sees how actually SA runs in production
→ Catches missing permissions before deploying

## Workflow: Creating and Using a SA

### 1. Create SA
```bash
gcloud iam service-accounts create <name> \
    --display-name="<description>"
```

### 2. Grant roles
```bash
gcloud projects add-iam-policy-binding <project> \
    --member="serviceAccount:<sa-email>" \
    --role="<role>"
```

### 3. Verify
```bash
gcloud projects get-iam-policy <project> \
    --flatten="bindings[].members" \
    --filter="bindings.members:<sa-email>" \
    --format="table(bindings.role)"
```

### 4. Impersonate for testing
```python
from google.auth import impersonated_credentials
import google.auth

source_credentials, _ = google.auth.default()
target_credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal='<sa-email>',
    target_scopes=['https://www.googleapis.com/auth/cloud-platform']
)
client = bigquery.Client(credentials=target_credentials)
```

## 3 Ways to Authenticate in GCP

| Method | When to use | Key file? |
|---|---|---|
| ADC | Local dev, personal account | No |
| Impersonation | Testing SA permissions | No |
| Workload Identity | Production on GCP | No |
| SA Key File | App running outside GCP | Yes |
# For SA key file:
Risk to be leaked 
## Real Errors Encountered
- `FAILED_PRECONDITION: Key creation is not allowed`
  → Org policy blocks SA key file creation (because of security risk)
  → use Workload Identity or ADC instead
- Local development → ADC:
`gcloud auth application-default login`
- Production on GCP → Workload Identity
- `permission denied` when inserting into BigQuery with dataViewer role
  → Expected behavior — dataEditor role required for insert operations