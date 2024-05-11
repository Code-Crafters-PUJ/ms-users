-- CREATE TABLE IF NOT EXISTS clients (
--   id SERIAL PRIMARY KEY,
--   company_name VARCHAR(45) NOT NULL,
--   contact_name VARCHAR(45) NOT NULL,
--   email VARCHAR(45) NOT NULL UNIQUE,
--   telephone BIGINT NOT NULL,
--   NIT BIGINT NOT NULL UNIQUE,
--   client_status SMALLINT NOT NULL DEFAULT 1
-- );

-- CREATE TABLE IF NOT EXISTS coupons (
--   code VARCHAR(45) PRIMARY KEY,
--   duration TIME NOT NULL,
--   discount DOUBLE PRECISION NOT NULL,
--   expiration_date DATE NOT NULL,
--   coupon_status SMALLINT NOT NULL DEFAULT 1,

--   client_id INT NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS billings (
--   id SERIAL PRIMARY KEY,
--   initial_date DATE NOT NULL,
--   final_date DATE NOT NULL,
--   usage TIME NOT NULL,
--   payment_date DATE NOT NULL,
--   amount DOUBLE PRECISION NOT NULL,
--   billing_status SMALLINT NOT NULL DEFAULT 1,

--   plan_id INT NOT NULL,
--   client_id INT NOT NULL,
--   payment_id INT NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS payments (
--   id SERIAL PRIMARY KEY,
--   method VARCHAR(45) NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS plans (
--   id SERIAL PRIMARY KEY,
--   plan_type VARCHAR(45) NOT NULL,
--   price DOUBLE PRECISION NOT NULL,
--   plan_description VARCHAR(100) NOT NULL,
--   duration INT NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS services (
--   id SERIAL PRIMARY KEY,
--   name VARCHAR(45) NOT NULL,
--   service_status SMALLINT NOT NULL DEFAULT 1
-- );


-- CREATE TABLE IF NOT EXISTS plans_has_services (
--   plan_id INT NOT NULL,
--   service_id INT NOT NULL,
--   PRIMARY KEY (plan_id, service_id)
-- );

-- -- indexes
-- CREATE INDEX idx_client_email
-- ON clients(email);

-- CREATE INDEX idx_client_NIT 
-- ON clients(NIT);

-- -- Client - Billing
-- ALTER TABLE billings
-- ADD CONSTRAINT fk_billing_client_idx
-- FOREIGN KEY (client_id)
-- REFERENCES clients (id);

-- -- Billing - Plan
-- ALTER TABLE billings
-- ADD CONSTRAINT fk_billing_plan_idx
-- FOREIGN KEY (plan_id)
-- REFERENCES plans (id);

-- -- Billing - Payment
-- ALTER TABLE billings
-- ADD CONSTRAINT fk_billing_payment_idx
-- FOREIGN KEY (payment_id)
-- REFERENCES payments (id);

-- -- Coupon - Client
-- ALTER TABLE coupons
-- ADD CONSTRAINT fk_coupon_client_idx
-- FOREIGN KEY (client_id)
-- REFERENCES clients (id);

-- -- Plan - Service
-- ALTER TABLE plans_has_services
-- ADD CONSTRAINT fk_plans_service_idx
-- FOREIGN KEY (service_id)
-- REFERENCES services (id);

-- ALTER TABLE plans_has_services
-- ADD CONSTRAINT fk_plan_services_idx
-- FOREIGN KEY (plan_id)
-- REFERENCES plans (id);



-- -- Insert clients
-- INSERT INTO clients (company_name, contact_name, email, telephone, NIT)
-- VALUES ('Tech Inc.', 'John Doe', 'john.doe@techinc.com', 1234567890, 123456789);

-- INSERT INTO clients (company_name, contact_name, email, telephone, NIT)
-- VALUES ('Marketing Solutions', 'Jane Smith', 'jane.smith@marketingsolutions.com', 9876543210, 987654321);

-- -- Insert plans
-- INSERT INTO plans (plan_type, price, plan_description, duration)
-- VALUES ('Silver', 100.00, 'Limited features, ideal for small businesses', 12);

-- INSERT INTO plans (plan_type, price, plan_description, duration)
-- VALUES ('Gold', 200.00, 'Full features, suitable for growing businesses', 6);

-- -- Insert payments
-- INSERT INTO payments (method)
-- VALUES ('Credit Card');

-- INSERT INTO payments (method)
-- VALUES ('Bank Transfer');

-- -- Insert billings
-- INSERT INTO billings (initial_date, final_date, billing_status, usage, plan_id, client_id, payment_id, amount, payment_date)
-- VALUES ('2024-03-29', '2024-04-28', 1, '00:30:45', 1, 1, 1, 100.00, '2024-03-29');  -- Silver plan for Tech Inc.

-- INSERT INTO billings (initial_date, final_date, billing_status, usage, plan_id, client_id, payment_id, amount, payment_date)
-- VALUES ('2024-03-29', '2025-03-28', 1, '12:30:45', 2, 2, 2, 200.00, '2024-03-29');  -- Gold plan for Marketing Solutions


