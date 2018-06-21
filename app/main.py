from flask import Flask, request, abort, jsonify
import json
import datetime, time
import pymysql.cursors

# MARIA_SERVER = '169.56.100.62'
# MARIA_PORT = 30000
MARIA_SERVER = 'webhook-mariadb'
MARIA_PORT = 3306
MARIA_DB = 'alertmanager'
MARIA_USER = 'root'
MARIA_PWD = 'admin'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_save():
    if request.method == 'POST':
        req_data = request.get_json()
        # print(req_data)
        json_str = json.dumps(req_data)
        print(json_str)

        now = datetime.datetime.now()
        now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        # print(now_datetime)

        conn = pymysql.connect(host=MARIA_SERVER,
                               port=MARIA_PORT,
                               user=MARIA_USER,
                               password=MARIA_PWD,
                               db=MARIA_DB,
                               charset='utf8')
        try:
            with conn.cursor() as cursor:
                sql = 'INSERT INTO history (alert, datetime) VALUES (%s, %s)'
                cursor.execute(sql, (json_str, now_datetime))

                conn.commit()

            # with conn.cursor() as cursor:
            #     sql = 'SELECT * FROM history'
            #     cursor.execute(sql)
            #     result = cursor.fetchall()
            #     print(result)
        finally:
            conn.close()

    else:
        abort(400)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
