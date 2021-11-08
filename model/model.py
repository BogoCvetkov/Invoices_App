import sqlite3
from pathlib import Path

cur_dir = Path.cwd()
db_dir = cur_dir.parent.joinpath("model", "database.db")


class Model:

    """
    This class is used for all CRUD operations on the database
    It includes only class methods, because there is no need for separate instances here
    """
    db = db_dir

    # Private method used internally in the other class methods
    @classmethod
    def _create_accounts_table(cls):
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY,"
                                  "account_name TEXT, account_id INTEGER type UNIQUE )")
            conn.commit()

    @classmethod
    def _create_user_table(cls):
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY,"
                                  "username TEXT, password TEXT )")
            conn.commit()

    @classmethod
    def _create_secret_table(cls):
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS secret (id INTEGER PRIMARY KEY,"
                                  "secret_key TEXT)")
            conn.commit()

    @classmethod
    def _create_billing_table(cls):
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS billing (id INTEGER PRIMARY KEY,"
                                  "info TEXT)")
            conn.commit()

    @classmethod
    def insert_user(cls, username, password):
        cls._create_user_table()
        ## DB holds only one record for the user. So we delete it everytime a new record is put
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("DELETE FROM user")
            conn.commit()
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("INSERT INTO user(username,password) VALUES(?,?)", (username, password))
            conn.commit()

    @classmethod
    def get_user(cls):
        with sqlite3.connect(cls.db) as conn:
            result = conn.cursor().execute("SELECT * FROM user")
            res = result.fetchone()
            if len(res) > 0:
                return res
            else:
                return None

    @classmethod
    def insert_account(cls, account_name,account_id):
        cls._create_accounts_table()
        account_name = str(account_name)
        account_id = int(account_id)
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("INSERT INTO accounts(account_name,account_id) VALUES(?,?)", (account_name, account_id))
            conn.commit()

    @classmethod
    def get_account(cls, account_name=None, account_id=None):
        cls._create_accounts_table()
        if account_id:
            with sqlite3.connect(cls.db) as conn:
                result = conn.cursor().execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
                return result.fetchone()
        if account_name:
            account_name = str(account_name).lower()
            with sqlite3.connect(cls.db) as conn:
                result = conn.cursor().execute("SELECT * FROM accounts WHERE account_name LIKE ? ", (account_name[:6] + "%",))
                return result.fetchall()
        else:
            return cls._get_all()

    @classmethod
    def insert_secret(cls,secret):
        cls._create_secret_table()
        ## DB holds only one record. So we delete it everytime a new record is put
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("DELETE FROM secret")
            conn.commit()
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("INSERT INTO secret(secret_key) VALUES(?)", (secret,))
            conn.commit()

    @classmethod
    def get_secret(cls):
        with sqlite3.connect(cls.db) as conn:
            result = conn.cursor().execute("SELECT * FROM secret")
            res = result.fetchone()
            if len(res) > 0:
                return res[-1]
            else:
                return None

    @classmethod
    def insert_billing_info(cls, info):
        cls._create_billing_table()
        ## DB holds only one record for the user. So we delete it everytime a new record is put
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("DELETE FROM billing")
            conn.commit()
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("INSERT INTO billing(info) VALUES(?)", (info,))
            conn.commit()

    @classmethod
    def get_billing_info(cls):
        with sqlite3.connect(cls.db) as conn:
            result = conn.cursor().execute("SELECT * FROM billing")
            res = result.fetchone()
            if len(res) > 0:
                return res[-1]
            else:
                return None

    @classmethod
    def _get_all(cls):
        with sqlite3.connect(cls.db) as conn:
            result = conn.cursor().execute("SELECT * FROM accounts")
            return result.fetchall()

    @classmethod
    def delete_account(cls, account_id):
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
            conn.commit()
            return "Account Deleted"

    @classmethod
    def delete_all_accounts(cls):
        with sqlite3.connect(cls.db) as conn:
            conn.cursor().execute("DELETE FROM accounts")
            conn.commit()
            return 'All Account Deleted'