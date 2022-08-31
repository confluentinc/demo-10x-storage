#!/bin/bash

echo "Source this script with \". ./env.sh\" to set environment variables and create api keys necessary for this demo.

This script assumes:
1. You have signed up for Confluent Cloud at https://confluent.cloud.
2. You have a Confluent Cloud environment running named \"demo-10x-storage\".
3. You have a Confluent Kafka cluster running named \"demo-10x-storage\".
4. You have a Confluent Schema Registry cluster running.

You can override the environment and kafka cluster names by exporting these environment variables:
CCLOUD_ENV_NAME
CCLOUD_CLUSTER_NAME
"

# Use confluent environment
confluent login --save
CCLOUD_ENV_ID=$(confluent environment list -o json \
    | jq -r '.[] | select(.name | contains('\"${CCLOUD_ENV_NAME:-demo-10x-storage}\"')) | .id')
confluent env use $CCLOUD_ENV_ID

# Use kafka cluster
CCLOUD_CLUSTER_ID=$(confluent kafka cluster list -o json \
    | jq -r '.[] | select(.name | contains('\"${CCLOUD_CLUSTER_NAME:-demo-10x-storage}\"')) | .id')
confluent kafka cluster use $CCLOUD_CLUSTER_ID

# Get cluster bootstrap endpoint
CCLOUD_BOOTSTRAP_ENDPOINT=$(confluent kafka cluster describe -o json | jq -r .endpoint)

# Create Kafka cluster API key
confluent api-key create \
    --resource $CCLOUD_CLUSTER_ID \
    --description "demo-10x-storage" \
    -o json > .env.CCLOUD_CLUSTER_API.json
CCLOUD_CLUSTER_API_KEY=$(cat .env.CCLOUD_CLUSTER_API.json | jq -r .key)
CCLOUD_CLUSTER_API_SECRET=$(cat .env.CCLOUD_CLUSTER_API.json | jq -r .secret)

# Get schema registry info
CCLOUD_SCHEMA_REGISTRY_ID=$(confluent sr cluster describe -o json | jq -r .cluster_id)
CCLOUD_SCHEMA_REGISTRY_ENDPOINT=$(confluent sr cluster describe -o json | jq -r .endpoint_url)

# Create schema registry API key
confluent api-key create \
    --resource $CCLOUD_SCHEMA_REGISTRY_ID \
    --description "demo-10x-storage" \
    -o json > .env.CCLOUD_SCHEMA_REGISTRY_API.json
CCLOUD_SCHEMA_REGISTRY_API_KEY=$(cat .env.CCLOUD_SCHEMA_REGISTRY_API.json | jq -r .key)
CCLOUD_SCHEMA_REGISTRY_API_SECRET=$(cat .env.CCLOUD_SCHEMA_REGISTRY_API.json | jq -r .secret)