import sqlite3
import json

class Database:
  def __init__(self, filepath):
    self.db = sqlite3.connect(filepath, detect_types = sqlite3.PARSE_DECLTYPES, check_same_thread = False)
    self.db.row_factory = sqlite3.Row

  def close(self):
    self.db.close()

  def get_registration(self, customer_uuid):
    registration = self.db.execute("SELECT * FROM registration WHERE customer_uuid = ? AND enabled = 'true';", (customer_uuid,)).fetchone()
    return registration

  def get_client(self, customer_uuid, client_uuid):
    client = self.db.execute("SELECT * FROM client WHERE customer_uuid = ? AND client_uuid = ?;", (customer_uuid, client_uuid,)).fetchone()
    return client

  def upsert_client(self, customer_uuid, client_uuid):
    self.db.execute("BEGIN TRANSACTION;")
    self.db.execute("INSERT OR IGNORE INTO client (customer_uuid, client_uuid) VALUES (?,?);", (customer_uuid, client_uuid,))
    self.db.execute("COMMIT TRANSACTION;")

  def get_scan_group_ids(self, customer_uuid, client_uuid):
    rows = self.db.execute("SELECT sg.id FROM scan_group sg LEFT JOIN group_client gc ON sg.id = gc.group_id WHERE sg.customer_uuid = ? AND gc.client_uuid = ? AND sg.enabled = 'true';", (customer_uuid, client_uuid,)).fetchall()
    scan_groups = [row[0] for row in rows]
    return scan_groups

  def get_authorization(self, customer_uuid, client_uuid):
    token = self.db.execute("SELECT * FROM authorization WHERE customer_uuid = ? AND client_uuid = ? AND enabled = 'true';", (customer_uuid, client_uuid,)).fetchone()
    return token

  def upsert_authorization(self, customer_uuid, client_uuid, token):
    updated = -1
    self.db.execute("BEGIN TRANSACTION;")
    self.db.execute("INSERT OR IGNORE INTO authorization (customer_uuid, client_uuid, token) VALUES (?,?,?);", (customer_uuid, client_uuid, token,))
    updated = self.db.execute("UPDATE authorization SET token = ? WHERE customer_uuid = ? AND client_uuid = ? AND enabled = 'true';", (token, customer_uuid, client_uuid,)).rowcount
    self.db.execute("COMMIT TRANSACTION;")
    return updated >= 1

  def set_scan_data(self, customer_uuid, client_uuid, data_map):
    scan_type = data_map['type']
    passed = data_map['passed']
    failed = data_map['failed']
    errored = data_map['errored']
    self.db.execute("BEGIN TRANSACTION;")
    self.db.execute("INSERT INTO scan_data (customer_uuid, client_uuid, type, passed, failed, errored) VALUES (?,?,?,?,?,?);", (customer_uuid, client_uuid, scan_type, passed, failed, errored,))
    self.db.execute("COMMIT TRANSACTION;")

  def set_audit_data(self, customer_uuid, client_uuid, data_map):
    audit_type = data_map['type']
    data = json.dumps(data_map[audit_type])
    self.db.execute("BEGIN TRANSACTION;")
    self.db.execute("INSERT INTO audit_data (customer_uuid, client_uuid, type, data) VALUES (?,?,?,?);", (customer_uuid, client_uuid, audit_type, data,))
    self.db.execute("COMMIT TRANSACTION;")