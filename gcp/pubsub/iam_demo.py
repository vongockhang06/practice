from google.cloud import bigquery
from google.auth import impersonated_credentials
import google.auth

# Lấy credentials hiện tại (tài khoản cá nhân)
source_credentials, project = google.auth.default()

# Impersonate readonly-sa
target_credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal='readonly-sa@cloud-migrate-crypto-pipeline.iam.gserviceaccount.com',
    target_scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Dùng credentials của readonly-sa
client = bigquery.Client(
    project='cloud-migrate-crypto-pipeline',
    credentials=target_credentials
)

# Test 1 — đọc (phải SUCCESS)
try:
    results = client.query("""
        SELECT * FROM `cloud-migrate-crypto-pipeline.crypto_data.crypto_prices`
        LIMIT 5
    """).result()
    print("READ SUCCESS:")
    for row in results:
        print(dict(row))
except Exception as e:
    print(f"READ FAILED: {e}")

# Test 2 — insert (phải FAIL)
try:
    errors = client.insert_rows_json(
        'cloud-migrate-crypto-pipeline.crypto_data.crypto_prices',
        [{'coin': 'test', 'price_usd': 1.0,
          'usd_24h_change': 0.0,
          'collected_at': '2026-07-27T00:00:00'}]
    )
    if errors:
        print(f"INSERT FAILED (expected): {errors}")
    else:
        print("INSERT SUCCESS (unexpected)")
except Exception as e:
    print(f"INSERT FAILED (expected): {e}")