from DB.DB_connect import DBConnect
from DB.DB_List import DBList
from Account.Account import Account
from DB.DB_Table_List import AccountTable
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import ProgrammingError, DataError, DatabaseError
from Logger.Logger import Logger


class AccountManager(object):

    @staticmethod
    def create_test_account(name='test'):
        account = AccountManager.get_account(name)

        if account is None:
            account = Account(name, name)
            AccountManager.create_account(account)
            return account
        else:
            return account

    ''' DB METHODS '''
    @staticmethod
    @DBConnect(DBList.LOGIN_DB_NAME.value)
    def get_account(cursor: MySQLCursor, account_name: str):
        account_table_name = AccountTable.ACCOUNT_LIST.value

        try:
            get_account_query = 'SELECT name, salt, verifier FROM ' + account_table_name + ' WHERE name = %s'
            get_account_data = (account_name.upper(),)
            cursor.execute(get_account_query, get_account_data)
            values = cursor.fetchone()

            if values is None:
                result = None
            else:
                # need for save data by field name
                field_name = [field[0] for field in cursor.description]
                result = dict(zip(field_name, values))

        except ProgrammingError as e:
            Logger.error('[Account Manager]: (get_account) programming error {}'.format(e))

        else:
            if result is not None:
                return Account(name=result['name'], salt=result['salt'], verifier=result['verifier'])

    @staticmethod
    @DBConnect(DBList.LOGIN_DB_NAME.value)
    def create_account(cursor: MySQLCursor, account: Account):
        account_table_name = AccountTable.ACCOUNT_LIST.value

        try:
            create_account_query = ('INSERT INTO ' + account_table_name + 
                                    '(name, salt, verifier) VALUES (%s, %s, %s)')
            create_account_data = (account.name.upper(), account.salt, account.verifier)
            cursor.execute(create_account_query, create_account_data)

        except (DataError, ProgrammingError, DatabaseError) as e:
            Logger.error('[Account Manager]: (create_account) error {}'.format(e))

    @staticmethod
    @DBConnect(DBList.LOGIN_DB_NAME.value)
    def update_account(cursor: MySQLCursor, account: Account):
        account_table_name = AccountTable.ACCOUNT_LIST.value

        try:
            update_account_query = ('UPDATE ' + account_table_name +
                                    ' SET ip = %s, timezone = %s, os = %s, platform = %s, locale = %s' +
                                    ' WHERE name = %s'
                                    )
            update_account_data = (
                account.ip_addr, account.timezone, account.os, account.platform, account.locale, account.name.upper()
            )

            cursor.execute(update_account_query, update_account_data)
        except (DataError, ProgrammingError, DatabaseError) as e:
            Logger.error('[Account Manager]: (update_account) error {}'.format(e))

    ''' END OF DB METHODS '''
