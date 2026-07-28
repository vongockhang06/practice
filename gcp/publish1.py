from google.cloud import pubsub_v1
import json

project_id = 'cloud-migrate-crypto-pipeline'
topic_id = "crypto-prices-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data = {"coin": "bitcoin", "price": 65000}
message = json.dumps(data).encode("utf-8")

future = publisher.publish(topic_path, message)
print(f"Published message ID: {future.result()}")