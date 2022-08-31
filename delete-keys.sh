#!/bin/bash

confluent login --save 

for i in $(confluent api-key list -o json | jq -r '.[] | select(.description | contains("demo-10x-storage")) | .key'); do
    confluent api-key delete $i 
done