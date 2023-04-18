# -*- encoding: utf-8 -*-
import pymysql


conn = pymysql.connect(
    host="124.220.3.231",
    port=3336,
    user="root",
    password="123456",
    database="fast_gms",
    charset="utf8"
)

cur = conn.cursor()

print(cur)


index = 1
while index < 10001:
    name = f"游戏服-{str(index)}"
    sql = f"""INSERT INTO server (id, client_ver, name,alias, game_addr, game_port, log_db_config, report_url, status, create_time, require_ver, remark, json_data, `order`, commend, is_ios, last_time, tabId, game_data, battleplan_id, season_group_id, real_number, expect_number, expect_time, switch_status, open_server_status) VALUES ({index}, '', '{name}', '开发服', '10.16.174.19', 12140, '', '', 2, '2022-05-17 15:40:20', 0, '', '', 14, 0, 0, '2022-05-19 18:28:12', 2, '', 10, 0, 0, -1, -1, 0, 0);"""
    print(sql)
    cur.execute(sql)
    conn.commit()
    index += 1
    print(sql)
cur.close()
conn.close()
