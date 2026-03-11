# Exercices - 10 queries in a row

# WHERE / ORDER BY / LIMIT (day to day basis)
# top 10 most expensive orders

SELECT id, customer_id, date, total
FROM "orders"
ORDER BY total DESC
LIMIT 10;

# ----

# Orders above a certain value (ex: 200)

SELECT id, customer_id, date, total
FROM "orders"
WHERE total > 200
ORDER BY total DESC;

# ----

# Customers in a city (change city)

SELECT id, name, city
FROM customer
WHERE city = 'São Paulo'
ORDER BY name;

# ----

# JOIN (link orders with customers)
# Orders with customer name and city

SELECT
  o.id AS order_id,
  c.name AS customer_name,
  c.city,
  o.date,
  o.total
FROM "orders" o
JOIN customer c ON c.id = o.customer_id
ORDER BY o.date DESC;

# ----

# Customer orders from a city (JOIN + WHERE)

SELECT
  o.id AS order_id,
  c.name,
  c.city,
  o.date,
  o.total
FROM "orders" o
JOIN customer c ON c.id = o.customer_id
WHERE c.city = 'São Paulo'
ORDER BY o.total DESC;

# ----

# GROUP BY + metrics (the heart of the “market”)
# Total spent and number of orders per customer (ranking)

SELECT
  c.id,
  c.name,
  c.city,
  COUNT(o.id) AS qtd_orders,
  ROUND(SUM(o.total), 2) AS total_spent,
  ROUND(AVG(o.total), 2) AS ticket_medium
FROM customer c
JOIN "orders" o ON o.customer_id = c.id
GROUP BY c.id, c.name, c.city
ORDER BY total_spent DESC;

# ----

# Filter out "good" customers (HAVING)
# Ex: customers with 3+ orders and total spend > 500

SELECT
  c.id,
  c.name,
  COUNT(*) AS qtd_orders,
  ROUND(SUM(o.total), 2) AS total_spent
FROM customer c
JOIN "orders" o ON o.customer_id = c.id
GROUP BY c.id, c.name
HAVING COUNT(*) >= 3 AND SUM(o.total) > 500
ORDER BY total_spent DESC;

# ----

# Metrics by city

SELECT
  c.city,
  COUNT(DISTINCT c.id) AS qtd_customer,
  COUNT(o.id) AS qtd_orders,
  ROUND(SUM(o.total), 2) AS invoicing
FROM customer c
JOIN "orders" o ON o.customer_id = c.id
GROUP BY c.city
ORDER BY invoicing DESC;

# ----

# Dates (since your date is TEXT)

SELECT
  substr(o.date, 1, 7) AS mounth,   -- YYYY-MM
  COUNT(*) AS qtd_orders,
  ROUND(SUM(o.total), 2) AS invoicing
FROM "orders" o
GROUP BY substr(o.date, 1, 7)
ORDER BY mounth;

# ----

# Data quality (highly valued)
# Check for "orphan" orders (without a customer)

SELECT o.*
FROM "orders" o
LEFT JOIN customer c ON c.id = o.customer_id
WHERE c.id IS NULL;

# ----

# Transforming queries into "reports" + performance + integrity

# General KPI

SELECT COUNT(*) AS qtd_orders, ROUND(SUM(total),2) AS invoicing_total, ROUND(AVG(total),2) AS ticket_medium FROM "orders";

# ----

# Top 5 clients by revenue

SELECT c.id, c.name, c.city, ROUND(SUM(o.total),2) AS total_spent FROM customer c JOIN "orders" o ON o.customer_id=c.id GROUP BY c.id, c.name, c.city ORDER BY total_spent DESC LIMIT 5;]

# ---- 

# "Who didn't buy?" (customers without orders) — LEFT JOIN

SELECT c.id, c.name, c.city FROM customer c LEFT JOIN "orders" o ON o.customer_id=c.id WHERE o.id IS NULL ORDER BY c.name;

# ----

# Performance (indices)

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON "orders"(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON "orders"(date);
EXPLAIN QUERY PLAN SELECT * FROM "orders" WHERE customer_id = 1;

# ----







