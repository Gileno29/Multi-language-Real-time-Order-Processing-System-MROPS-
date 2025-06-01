#!/bin/bash



for ((i=1; i<=100; i++)); do
  product_id=$((i + 10))

  json=$(printf '{"order_id":"%d","user_id":"%d","product_id":"%d","quantity":1,"price":150.0}' "$i" "$i" "$product_id")
  curl -X POST http://localhost:5000/order \
     -H "Content-Type: application/json" \
     -d "$json"

 
done