import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import datetime
from flask import Flask, jsonify, request, redirect, render_template
import time
from multiprocessing import Process, Value
import multiprocessing
# from flask_cors import CORS
import pymysql
app = Flask(__name__)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'

box1_value, box1_value, box1_value, box4_value = [0, 0, 0, 0, 0, 0, True, False], [
    0, 0, 0, 0, 0, 0, True, False], [0, 0, 0, 0, 0, 0, True, False], [0, 0, 0, 0, 0, 0, True, False]
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='mygp',
    charset='utf8',
)
cur = conn.cursor()


@app.route('/', methods=['POST', 'GET'])
def index_0():
    return render_template('index.html')


@app.route('/user', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data['name'], data['pwd'])
        falg = fun_user(data['name'], data['pwd'])
        if(falg):
            return str(falg)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')


def fun_user(name, pwd):
    sql = "select name,pwd from user where name='{}' and pwd={}".format(
        name, pwd)
    num = cur.execute(sql)
    print(num == 1)
    return (num == 1)


@app.route('/ad', methods=['POST', 'GET'])
def ad_login():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        # print(data)
        print(data['name'], data['pwd'])
        falg = fun_ad(data['name'], data['pwd'])
        if(falg):
            return str(falg)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')


def fun_ad(name, pwd):
    sql = "select name,pwd from ad where name='{}' and pwd={}".format(
        name, pwd)
    num = cur.execute(sql)
    print(num == 1)
    return (num == 1)


@app.route('/Box1_table', methods=['POST', 'GET'])
def Box1_table():
    return render_template('Box1_table.html')


@app.route('/Box1_line', methods=['POST', 'GET'])
def Box1_line():
    return render_template('Box1_line.html')


@app.route('/Box1_chart', methods=['POST', 'GET'])
def Box1_chart():
    return render_template('Box1_chart.html')


@app.route('/Box1_operation', methods=['POST', 'GET'])
def Box1_operation():
    return render_template('Box1_operation.html')


@app.route('/Box1')
def Box1_table1():
    object_dict = {'id': 0, 'PH': 0,
                   'pressure': 0, 'CO2': 0, 'time': '', 'O2': 0, 'CH3CH2OH': 0, 'CH3CH2COOH': 0}
    sql = "select * from box1 order by id desc"
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    desc = cur.description
    rows = cur.fetchall()
    object_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in rows
    ]
    strs = str(object_dict)
    strs = strs.replace('[', '').replace(']', '')
    object_dict = eval(strs)
    # print(box1_value)
    return jsonify(object_dict)


@app.route('/Box1_write', methods=['POST', 'GET'])
def Box1_write():
    data = request.get_json(silent=True)
    box1_value[0] = int(data['pressure'])
    box1_value[1] = int(data['CO2'])
    box1_value[2] = int(data['O2'])
    box1_value[3] = int(data['CH3CH2OH'])
    box1_value[4] = int(data['CH3CH2COOH'])
    box1_value[5] = int(data['PH'])
    box1_value[7] = True
    # print(box1_value)
    return render_template('Box1_operation.html')


@app.route('/Box1_switch', methods=['POST', 'GET'])
def Box1_switch():
    data = request.get_json(silent=True)
    box1_value[6] = data['flag']
    return render_template('Box1_operation.html')


@app.route('/Box2_table', methods=['POST', 'GET'])
def Box2_table():
    return render_template('Box2_table.html')


@app.route('/Box2_line', methods=['POST', 'GET'])
def Box2_line():
    return render_template('Box2_line.html')


@app.route('/Box2_chart', methods=['POST', 'GET'])
def Box2_chart():
    return render_template('Box2_chart.html')


@app.route('/Box2_operation', methods=['POST', 'GET'])
def Box2_operation():
    return render_template('Box2_operation.html')


@app.route('/Box2')
def Box2_table1():
    object_dict = {'id': 0, 'PH': 0,
                   'pressure': 0, 'CO2': 0, 'time': '', 'O2': 0, 'CH3CH2OH': 0, 'CH3CH2COOH': 0}
    sql = "select * from box2 order by id desc"
    conn.ping(reconnect=True)
    nums = cur.execute(sql)
    conn.commit()
    desc = cur.description
    rows = cur.fetchall()
    object_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in rows
    ]
    if(nums):
        strs = str(object_dict).replace('[', '').replace(']', '')
        object_dict = eval(strs)
        # print(box1_value)
        return jsonify(object_dict)
    else:
        object_dict = {'a': 1, 'b': 2}
        return jsonify(object_dict)


@app.route('/Box2_write', methods=['POST', 'GET'])
def Box2_write():
    data = request.get_json(silent=True)
    box2_value[0] = int(data['pressure'])
    box2_value[1] = int(data['CO2'])
    box2_value[2] = int(data['O2'])
    box2_value[3] = int(data['CH3CH2OH'])
    box2_value[4] = int(data['CH3CH2COOH'])
    box2_value[5] = int(data['PH'])
    box2_value[7] = True
    # print(box2_value)
    return render_template('Box2_operation.html')


@app.route('/Box2_switch', methods=['POST', 'GET'])
def Box2_switch():
    data = request.get_json(silent=True)
    box2_value[6] = data['flag']
    return render_template('Box2_operation.html')


@app.route('/Box3_table', methods=['POST', 'GET'])
def Box3_table():
    return render_template('Box3_table.html')


@app.route('/Box3_chart', methods=['POST', 'GET'])
def Box3_chart():
    return render_template('Box3_chart.html')


@app.route('/Box3_line', methods=['POST', 'GET'])
def Box3_line():
    return render_template('Box3_line.html')


@app.route('/Box3_operation', methods=['POST', 'GET'])
def Box3_operation():
    return render_template('Box3_operation.html')


@app.route('/Box3')
def Box3_table1():
    object_dict = {'id': 0, 'PH': 0,
                   'pressure': 0, 'CO2': 0, 'time': '', 'O2': 0, 'CH3CH2OH': 0, 'CH3CH2COOH': 0}
    sql = "select * from box3 order by id desc"
    conn.ping(reconnect=True)
    nums = cur.execute(sql)
    conn.commit()

    desc = cur.description
    rows = cur.fetchall()
    object_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in rows
    ]
    if(nums):
        strs = str(object_dict).replace('[', '').replace(']', '')
        object_dict = eval(strs)
        # print(box1_value)
        return jsonify(object_dict)
    else:
        object_dict = {'a': 1, 'b': 2}
        return jsonify(object_dict)


@app.route('/Box3_write', methods=['POST', 'GET'])
def Box3_write():
    data = request.get_json(silent=True)
    box3_value[0] = int(data['pressure'])
    box3_value[1] = int(data['CO2'])
    box3_value[2] = int(data['O2'])
    box3_value[3] = int(data['CH3CH2OH'])
    box3_value[4] = int(data['CH3CH2COOH'])
    box3_value[5] = int(data['PH'])
    box3_value[7] = True
    # print(box3_value)
    return render_template('Box3_operation.html')


@app.route('/Box3_switch', methods=['POST', 'GET'])
def Box3_switch():
    data = request.get_json(silent=True)
    box3_value[6] = data['flag']
    return render_template('Box3_operation.html')


@app.route('/Box4_table', methods=['POST', 'GET'])
def Box4_table():
    return render_template('Box4_table.html')


@app.route('/Box4_line', methods=['POST', 'GET'])
def Box4_line():
    return render_template('Box4_line.html')


@app.route('/Box4_chart', methods=['POST', 'GET'])
def Box4_chart():
    return render_template('Box4_chart.html')


@app.route('/Box4_operation', methods=['POST', 'GET'])
def Box4_operation():
    return render_template('Box4_operation.html')


@app.route('/Box4')
def Box4_table1():
    object_dict = {'id': 0, 'PH': 0,
                   'pressure': 0, 'CO2': 0, 'time': '', 'O2': 0, 'CH3CH2OH': 0, 'CH3CH2COOH': 0}
    sql = "select * from box4 order by id desc"
    conn.ping(reconnect=True)
    nums = cur.execute(sql)
    conn.commit()
    desc = cur.description
    rows = cur.fetchall()
    object_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in rows
    ]
    if(nums):
        strs = str(object_dict).replace('[', '').replace(']', '')
        object_dict = eval(strs)
        # print(box1_value)
        return jsonify(object_dict)
    else:

        object_dict = {'a': 1, 'b': 2}
        return jsonify(object_dict)


@app.route('/Box4_write', methods=['POST', 'GET'])
def Box4_write():
    data = request.get_json(silent=True)
    box4_value[0] = int(data['pressure'])
    box4_value[1] = int(data['CO2'])
    box4_value[2] = int(data['O2'])
    box4_value[3] = int(data['CH3CH2OH'])
    box4_value[4] = int(data['CH3CH2COOH'])
    box4_value[5] = int(data['PH'])
    box4_value[7] = True
    # print(box4_value)
    return render_template('Box4_operation.html')


@app.route('/Box4_switch', methods=['POST', 'GET'])
def Box4_switch():
    data = request.get_json(silent=True)
    box4_value[6] = data['flag']
    return render_template('Box4_operation.html')


@app.route('/switch', methods=['POST', 'GET'])
def Box_switch():
    desc = ['box1_switch', 'box2_switch', 'box3_switch', 'box4_switch']
    rows = []
    rows.append(box1_value[6])
    rows.append(box2_value[6])
    rows.append(box3_value[6])
    rows.append(box4_value[6])
    # print(rows)
    object_dict = [
        dict(zip(desc, rows))

    ]
    object_dict = str(object_dict).replace('[', '').replace(']', '')
    object_dict = eval(object_dict)
    # print(object_dict)
    return jsonify(object_dict)


@app.route('/user_admin', methods=['POST', 'GET'])
def user_admin():
    return render_template('user_table.html')


@app.route('/user_table', methods=['POST', 'GET'])
def user_table():
    sql = "select * from user"
    conn.ping(reconnect=True)
    nums = cur.execute(sql)
    conn.commit()
    desc = cur.description
    rows = cur.fetchall()
    object_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in rows
    ]
    if(nums):
        strs = str(object_dict).replace('[', '').replace(']', '')+',1'
        object_dict = eval(strs)
        print(object_dict)
        return jsonify(object_dict)
    else:
        object_dict = {'a': 1, 'b': 2}
        return jsonify(object_dict)


@app.route('/user_add', methods=['POST', 'GET'])
def user_add():
    data = request.get_json(silent=True)
    sql = "insert into user(id,name, pwd) values(0,'{}','{}')".format(
        data['name'], data['pwd'])
    print(sql)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    return redirect('/user_admin')


@app.route('/user_del', methods=['POST', 'GET'])
def user_del():
    data = request.get_json(silent=True)
    print(data)
    sql = "delete from user where id='{}'".format(
        data['id'])
    print(sql)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    return redirect('/user_admin')


@app.route('/user_update', methods=['POST', 'GET'])
def user_update():
    data = request.get_json(silent=True)
    if(data['name'] == ''):
        data['name'] = data['NAME']
    if(data['pwd'] == ''):
        sql = "update user set name='{}' where name='{}'".format(
            data['name'], data['NAME'])
    else:
        sql = "update user set name='{}',pwd='{}' where name='{}'".format(
            data['name'], data['pwd'], data['NAME'])
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    return redirect('/user_admin')


@app.route('/User_Box1_table', methods=['POST', 'GET'])
def User_Box1_table():
    return render_template('User_Box1_table.html')


@app.route('/User_Box1_line', methods=['POST', 'GET'])
def User_Box1_line():
    return render_template('User_Box1_line.html')


@app.route('/User_Box1_chart', methods=['POST', 'GET'])
def User_Box1_chart():
    return render_template('User_Box1_chart.html')


@app.route('/User_Box2_table', methods=['POST', 'GET'])
def User_Box2_table():
    return render_template('User_Box2_table.html')


@app.route('/User_Box2_line', methods=['POST', 'GET'])
def User_Box2_line():
    return render_template('User_Box2_line.html')


@app.route('/User_Box2_chart', methods=['POST', 'GET'])
def User_Box2_chart():
    return render_template('User_Box2_chart.html')


@app.route('/User_Box3_table', methods=['POST', 'GET'])
def User_Box3_table():
    return render_template('User_Box3_table.html')


@app.route('/User_Box3_line', methods=['POST', 'GET'])
def User_Box3_line():
    return render_template('User_Box3_line.html')


@app.route('/User_Box3_chart', methods=['POST', 'GET'])
def User_Box3_chart():
    return render_template('User_Box3_chart.html')


@app.route('/User_Box4_table', methods=['POST', 'GET'])
def User_Box4_table():
    return render_template('User_Box4_table.html')


@app.route('/User_Box4_line', methods=['POST', 'GET'])
def User_Box4_line():
    return render_template('User_Box4_line.html')


@app.route('/User_Box4_chart', methods=['POST', 'GET'])
def User_Box4_chart():
    return render_template('User_Box4_chart.html')


def box1_mod(box1_value):
    red = []
    alarm = ""
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port="com2",
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        red = master.execute(1, cst.READ_HOLDING_REGISTERS,
                             0, 9)
        alarm = "正常"
        if(box1_value[7]):
            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0,
                           output_value=tuple(box1_value[0:6]))
            box1_value[7] = False
        return list(red), alarm
    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))
    return red, alarm


def box2_mod(box2_value):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port="com4",
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        red = master.execute(1, cst.READ_HOLDING_REGISTERS,
                             0, 9)  # 这里可以修改需要读取的功能码
        alarm = "正常"
        # print(output_value, output_value)
        # print(box2_value)
        if(box2_value[7]):
            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0,
                           output_value=tuple(box2_value))  # READ_HOLDING_REGISTERS 功能码对上可使用
            box2_value[7] = False

        return list(red), alarm

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


def box3_mod(box3_value):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port="com6",
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        red = master.execute(1, cst.READ_HOLDING_REGISTERS,
                             0, 9)  # 这里可以修改需要读取的功能码
        alarm = "正常"
        # print(output_value, output_value)
        # print(box3_value)
        if(box3_value[7]):
            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0,
                           output_value=tuple(box3_value))  # READ_HOLDING_REGISTERS 功能码对上可使用
            box3_value[7] = False

        return list(red), alarm

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


def box4_mod(box4_value):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port="com8",
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        red = master.execute(1, cst.READ_HOLDING_REGISTERS,
                             0, 9)  # 这里可以修改需要读取的功能码
        alarm = "正常"
        # print(output_value, output_value)
        # print(box4_value)
        if(box4_value[7]):
            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0,
                           output_value=tuple(box4_value))
            box4_value[7] = False

        return list(red), alarm

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


def Box_1(loop_on, box1_value):
    while True:

        if loop_on.value == True:
            if(box1_value[6]):
                red, alarm1 = box1_mod(box1_value)
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = "insert into box1(id,time,pressure,CO2,O2,CH3CH2OH,CH3CH2COOH,PH) VALUES (0,'{}','{}','{}','{}','{}','{}','{}')".format(
                    t, red[0], red[1], red[2], red[3], red[4], red[5])
                conn.ping(reconnect=True)
                cur.execute(sql)
                conn.commit()
        time.sleep(5)


def Box_2(loop_on, box1_value):
    while True:
        if loop_on.value == True:
            red, alarm1 = box2_mod(box1_value)
            # print(red1, red2, red3, red4)
            t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = "insert into box2(id,time,pressure,CO2,O2,CH3CH2OH,CH3CH2COOH,PH) VALUES (0,'{}','{}','{}','{}','{}','{}','{}')".format(
                t, red[0], red[1], red[2], red[3], red[4], red[5])

            # print(t, red, sql1, box1_value)
            conn.ping(reconnect=True)
            cur.execute(sql)
            conn.commit()
        time.sleep(5)


def Box_3(loop_on, box1_value):
    while True:
        if loop_on.value == True:
            red, alarm1 = box3_mod(box1_value)
            # print(red1, red2, red3, red4)
            t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = "insert into box3(id,time,pressure,CO2,O2,CH3CH2OH,CH3CH2COOH,PH) VALUES (0,'{}','{}','{}','{}','{}','{}','{}')".format(
                t, red[0], red[1], red[2], red[3], red[4], red[5])
            conn.ping(reconnect=True)

            # print(t, red, sql1, box1_value)
            cur.execute(sql)
            conn.commit()
        time.sleep(5)


def Box_4(loop_on, box1_value):
    while True:
        if loop_on.value == True:
            red, alarm1 = box4_mod(box1_value)
            # print(red1, red2, red3, red4)
            t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = "insert into box4(id,time,pressure,CO2,O2,CH3CH2OH,CH3CH2COOH,PH) VALUES (0,'{}','{}','{}','{}','{}','{}','{}')".format(
                t, red[0], red[1], red[2], red[3], red[4], red[5])
            conn.ping(reconnect=True)

            # print(t, red, sql1, box1_value)
            cur.execute(sql)
            conn.commit()
        time.sleep(5)


if __name__ == '__main__':
    box1_value, box2_value, box3_value, box4_value = multiprocessing.Manager().list(
        [0, 0, 0, 0, 0, 0, True, False]), multiprocessing.Manager().list([0, 0, 0, 0, 0, 0, True, False]), multiprocessing.Manager().list([0, 0, 0, 0, 0, 0, True, False]), multiprocessing.Manager().list([0, 0, 0, 0, 0, 0, True, False])
    recording_on = [Value('b', True), Value('b', True),
                    Value('b', True), Value('b', True)]
    # print(recording_on)
    p1 = Process(target=Box_1, args=(
        recording_on[0], box1_value))
    p2 = Process(target=Box_2, args=(
        recording_on[1], box2_value))
    p3 = Process(target=Box_3, args=(
        recording_on[2], box3_value))
    p4 = Process(target=Box_4, args=(
        recording_on[3], box4_value))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    app.run(host='0.0.0.0',  # 任何ip都可以访问
            port=5000,  # 端口
            debug=True,
            use_reloader=False
            )
    p1.join()
    p2.join()
    p3.join()
    p4.join()
