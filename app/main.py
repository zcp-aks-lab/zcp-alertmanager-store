from flask import Flask, request, abort, jsonify
import json
import datetime
import pymysql.cursors

# Dev
# MARIA_SERVER = '127.0.0.1'
# MARIA_PORT = 3306
# MARIA_USER = 'root'
# MARIA_PWD = 'my-secret-pw'

# Production
# TODO : Extract to configmap or argument
MARIA_SERVER = 'alertmanager-store-mariadb'
MARIA_PORT = 3306
MARIA_DB_NAME = 'alertmanager'
MARIA_USER = 'root'
MARIA_PWD = 'admin'

app = Flask(__name__)


def _get_connection(db=None):
    conn = pymysql.connect(host=MARIA_SERVER,
                           port=MARIA_PORT,
                           user=MARIA_USER,
                           db=db,
                           password=MARIA_PWD,
                           charset='utf8')
    return conn


'''
DB Scheme infomation 
--------------------
'''

_SQL_CREATE_DB = 'CREATE DATABASE IF NOT EXISTS %s' % MARIA_DB_NAME
_SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS history(
    seq INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    alert JSON,
    datetime VARCHAR(30)
)'''
_SQL_SET_EVENT_SCHEDULER = '''SET GLOBAL event_scheduler = ON;
SET @@global.event_scheduler = ON;
SET GLOBAL event_scheduler = 1;
SET @@global.event_scheduler = 1;'''

_SQL_CREATE_EVENT = '''CREATE EVENT IF NOT EXISTS history
ON SCHEDULE
    EVERY 1 DAY
    STARTS CURRENT_TIMESTAMP
DO
    DELETE FROM history
    WHERE date_format(datetime, '%Y-%m-%d') <= date_sub(curdate(), INTERVAL 1 MONTH)
'''

_SQL_INSERT_HISTORY = "INSERT INTO history (alert, datetime) VALUES (%s, %s)"


@app.before_first_request
def _init_db():
    print '# Check db scheme...'
    conn = _get_connection()
    try:
        with conn.cursor() as cursor:
            # Create DB
            cursor.execute(_SQL_CREATE_DB)
            # Create table and event
            cursor.execute('USE %s' % MARIA_DB_NAME)
            cursor.execute(_SQL_CREATE_TABLE)
            for line in _SQL_SET_EVENT_SCHEDULER.splitlines():
                cursor.execute(line)
            cursor.execute(_SQL_CREATE_TABLE)
        conn.commit()
    finally:
        conn.close()


@app.route('/webhook', methods=['POST'])
def webhook_save():
    if request.method == 'POST':
        req_data = request.get_json()

        # TODO: Verify request data.
        ##

        json_str = json.dumps(req_data)

        now = datetime.datetime.now()
        now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        conn = _get_connection(MARIA_DB_NAME)

        try:
            with conn.cursor() as cursor:
                cursor.execute(_SQL_INSERT_HISTORY, (json_str, now_datetime))

            conn.commit()
        finally:
            conn.close()
    else:
        abort(400)

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
