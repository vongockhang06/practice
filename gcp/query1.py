from google.cloud import bigquery

# Tự động dùng ADC — không cần key file
client = bigquery.Client(project='cloud-migrate-crypto-pipeline')

query = """
    SELECT coin, AVG(price_usd) as avg_price
    FROM `cloud-migrate-crypto-pipeline.crypto_data.crypto_prices`
    GROUP BY coin
"""

results = client.query(query).result()
for row in results:
    print(f"{row.coin}: ${row.avg_price:.2f}")