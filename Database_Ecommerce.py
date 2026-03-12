# let's set up a more professional e-commerce platform

# Initial configuration
import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Activation of foreign keys
# Creation of tables (customer, category, product, orders, order_item, payment)
cursor.executescript("""
PRAGMA foreign_keys = ON; 


CREATE TABLE IF NOT EXISTS customer (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS category (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS product (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  price REAL NOT NULL CHECK(price >= 0),
  stock INTEGER NOT NULL CHECK(stock >= 0),
  created_at TEXT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS "orders" (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
  FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE IF NOT EXISTS order_item (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL CHECK(quantity > 0),
  unit_price REAL NOT NULL CHECK(unit_price >= 0),
  FOREIGN KEY (order_id) REFERENCES "orders"(id),
  FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS payment (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL UNIQUE,
  payment_date TEXT,
  amount REAL NOT NULL CHECK(amount >= 0),
  method TEXT NOT NULL CHECK(method IN ('credit_card', 'debit_card', 'pix', 'ticket', 'cash')),
  status TEXT NOT NULL CHECK(status IN ('pending', 'paid', 'failed', 'refunded')),
  FOREIGN KEY (order_id) REFERENCES "orders"(id)
);

INSERT OR IGNORE INTO category (id, name) VALUES
(1, 'Electronics'),
(2, 'Computer'),
(3, 'Home'),
(4, 'Books'),
(5, 'Office');

INSERT OR IGNORE INTO customer (id, name, email, city, state, created_at) VALUES
(1, 'Ana Souza', 'ana@email.com', 'São Paulo', 'SP', '2025-01-10'),
(2, 'Bruno Lima', 'bruno@email.com', 'Rio de Janeiro', 'RJ', '2025-01-15'),
(3, 'Carla Mendes', 'carla@email.com', 'Belo Horizonte', 'MG', '2025-02-01'),
(4, 'Daniel Rocha', 'daniel@email.com', 'Curitiba', 'PR', '2025-02-10'),
(5, 'Eduarda Alves', 'eduarda@email.com', 'Salvador', 'BA', '2025-02-20'),
(6, 'Felipe Costa', 'felipe@email.com', 'Fortaleza', 'CE', '2025-03-01'),
(7, 'Gabriela Pinto', 'gabriela@email.com', 'Recife', 'PE', '2025-03-05'),
(8, 'Henrique Dias', 'henrique@email.com', 'Porto Alegre', 'RS', '2025-03-10');

INSERT OR IGNORE INTO product (id, name, category_id, price, stock, created_at) VALUES
(1, 'Smartphone Galaxy', 1, 2500.00, 15, '2025-01-05'),
(2, 'Notebook Dell', 2, 4500.00, 8, '2025-01-06'),
(3, 'Mouse Logitech', 2, 120.00, 40, '2025-01-07'),
(4, 'Mechanic Keyboard', 2, 350.00, 25, '2025-01-08'),
(5, 'Air Fryer', 3, 500.00, 12, '2025-01-09'),
(6, 'Coffee maker', 3, 280.00, 10, '2025-01-10'),
(7, 'SQL book for beginners', 4, 90.00, 30, '2025-01-11'),
(8, 'Python book for professionals', 4, 120.00, 20, '2025-01-12'),
(9, 'Offiche chair', 5, 900.00, 7, '2025-01-13'),
(10, 'Monitor 24"', 2, 1100.00, 14, '2025-01-14');

INSERT OR IGNORE INTO "orders" (id, customer_id, order_date, status) VALUES
(1, 1, '2025-03-01', 'paid'),
(2, 2, '2025-03-02', 'delivered'),
(3, 1, '2025-03-05', 'shipped'),
(4, 3, '2025-03-08', 'paid'),
(5, 4, '2025-03-10', 'cancelled'),
(6, 5, '2025-03-11', 'delivered'),
(7, 6, '2025-03-12', 'paid'),
(8, 2, '2025-03-15', 'shipped'),
(9, 7, '2025-03-16', 'pending'),
(10, 8, '2025-03-18', 'paid');

INSERT OR IGNORE INTO order_item (id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 2500.00),
(2, 1, 3, 2, 120.00),
(3, 2, 2, 1, 4500.00),
(4, 3, 7, 1, 90.00),
(5, 3, 8, 1, 120.00),
(6, 3, 3, 1, 120.00),
(7, 4, 5, 1, 500.00),
(8, 4, 6, 1, 280.00),
(9, 5, 9, 1, 900.00),
(10, 6, 10, 2, 1100.00),
(11, 7, 4, 1, 350.00),
(12, 7, 3, 1, 120.00),
(13, 8, 1, 1, 2500.00),
(14, 8, 10, 1, 1100.00),
(15, 9, 7, 2, 90.00),
(16, 10, 6, 1, 280.00),
(17, 10, 5, 1, 500.00);

INSERT OR IGNORE INTO payment (id, order_id, payment_date, amount, method, status) VALUES
(1, 1, '2025-03-01', 2740.00, 'credit_card', 'paid'),
(2, 2, '2025-03-02', 4500.00, 'pix', 'paid'),
(3, 3, '2025-03-05', 330.00, 'ticket', 'paid'),
(4, 4, '2025-03-08', 780.00, 'credit_card', 'paid'),
(5, 5, '2025-03-10', 900.00, 'credit_card', 'refunded'),
(6, 6, '2025-03-11', 2200.00, 'debit_card', 'paid'),
(7, 7, '2025-03-12', 470.00, 'pix', 'paid'),
(8, 8, '2025-03-15', 3600.00, 'credit_card', 'paid'),
(9, 9, NULL, 180.00, 'boleto', 'pending'),
(10, 10, '2025-03-18', 780.00, 'cash', 'paid');
""")

# Confirmation and closing
conn.commit()
conn.close()

# Confirmation message
print("Bank ecommerce.db successfully created!")




