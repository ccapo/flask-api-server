DROP TABLE IF EXISTS registration;

CREATE TABLE registration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uuid TEXT NOT NULL,
    token TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_customer_token UNIQUE(customer_uuid, token)
);

DROP TABLE IF EXISTS authorization;

CREATE TABLE authorization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uuid TEXT NOT NULL,
    client_uuid TEXT NOT NULL,
    token TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_customer_client_jwt UNIQUE(customer_uuid, client_uuid)
);

DROP TABLE IF EXISTS client;

CREATE TABLE client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uuid TEXT NOT NULL,
    client_uuid TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'registered',
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_customer_client UNIQUE(customer_uuid, client_uuid)
);

DROP TABLE IF EXISTS scan_group;

CREATE TABLE scan_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_customer_name UNIQUE(customer_uuid, name)
);

DROP TABLE IF EXISTS group_client;

CREATE TABLE group_client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    client_uuid TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS audit_data;

CREATE TABLE audit_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uuid TEXT NOT NULL,
    client_uuid TEXT NOT NULL,
    type TEXT NOT NULL,
    data TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS scan_data;

CREATE TABLE scan_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uuid TEXT NOT NULL,
    client_uuid TEXT NOT NULL,
    type TEXT NOT NULL,
    passed INTEGER NOT NULL,
    failed INTEGER NOT NULL,
    errored INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO registration (customer_uuid, token) VALUES ('96326e2a-6487-4cfd-a859-2881b330c30d', 'sMCGzni0dWm7WCH2XNDSqxMcrpmpFwIJ9sqQeik/WbEY671uiArn23V3SViNkiDUta9UtThHkAgQhToAMxPFzL0aJVhw3q8lBWkh9dFGNLYLIz7bI7hqXlZawwJX9qewIeLaqngonV6Xkp5kGOsje9pE2M21ejuTd+VzNhJaWSE=');
INSERT INTO client (customer_uuid, client_uuid, status) VALUES ('96326e2a-6487-4cfd-a859-2881b330c30d', '1a5d154b-8fb6-40fb-89e6-6b2bdba6973a', 'registered');
INSERT INTO scan_group (customer_uuid, name) VALUES ('96326e2a-6487-4cfd-a859-2881b330c30d', 'Server Scan Group');
INSERT INTO scan_group (customer_uuid, name) VALUES ('96326e2a-6487-4cfd-a859-2881b330c30d', 'Desktop Scan Group');
INSERT INTO group_client (group_id, client_uuid) VALUES (1, '1a5d154b-8fb6-40fb-89e6-6b2bdba6973a');