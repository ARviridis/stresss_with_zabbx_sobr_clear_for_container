from flask import render_template,request,json
from pyzabbix import ZabbixAPI
from app import app
from app.timemon import a, lhip, namehost,diskinfo_info_a, metrics, servz
import config1 as cfg

#инициализация демона только в инит.пу
@app.route('/zabbx', methods=['GET', 'POST'])
def zabb():
    metrics
    return render_template('zabbx.html', title='zabbx', metrics=metrics)
# ------------------------------------------------------------------------------------------------

iskl=0

if a != False:
    servz ='%s%s/%s' % ('http://',cfg.zabbserv,"zabbix")
    z = ZabbixAPI(servz, user='Admin', password='11')
    answer = z.do_request('apiinfo.version')
    print ("Version:",answer['result'])

    # Get all monitored hosts
    result1 = z.host.get(monitored_hosts=1, output='extend')
    result2 = z.item.get(output='extend')
    result3 = z.template.get(output='extend')
    # шаблон создаем зерез интерфейс
    print ('AAAAAAAAAAAA2')
    diskinfo_info_a_2 = []
    for i2 in diskinfo_info_a:
        if i2 not in diskinfo_info_a_2:
            diskinfo_info_a_2.append(i2)

    #diskinfo_info_a_2 = diskinfo_info_a.copy()

    hosts = z.do_request('host.get', {
                          'selectGroups': 'extend',
                           'filter': {'host': ''}
                          })
    hostnames = [host['host'] for host in hosts['result']]
    print ("Found hosts: {}".format(hostnames))
    find = 0


    for d in result1:
        if d.get('name') == namehost:
            print(d.get('name') == namehost)
            print("Find your host")
            print(d)
            find = 1
            hid = d.get('hostid')
            print(hid)
            z.do_request(method="host.update", params=
            {
                "hostid": hid,
                "host": namehost,

                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": lhip,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": "2"
                    }
                ],
                "templates": [
                    {
                        "templateid": "10358"
                    }
                ],
            }
                         )
            print("host.update.SUCCES")

            print(diskinfo_info_a_2)
            for q in result2:
                if q.get('hostid') == d.get('hostid'):
                    for qq2 in diskinfo_info_a_2:
                        if qq2 == (q.get('name')):
                           # print("s")
                           # print(qq2)
                            diskinfo_info_a_2.remove(q.get('name'))
                            z.do_request(method="item.update", params=
                            {
                                'itemid': q.get('itemid'),
                                'type': '2',
                                'hostid': d.get('hostid'),
                                'name': qq2,
                                'key_': qq2,
                                'delay': '0',
                                'history': '1d',
                                'trends': '1d',
                                'status': '0',
                                'value_type': '0',
                                'description': qq2,
                                'interfaceid': '0',
                            }
                                         )
                            iskl = q.get('name')
                            print("item.update.SUCCES")

            if diskinfo_info_a_2 != []:
                for q333 in diskinfo_info_a:
                    for qt3 in diskinfo_info_a_2:
                        if iskl != qt3:
                            print('ISKLLL_net')
                            if q333 == qt3:
                                print('_onea2nepusto')
                                z.do_request(method="item.create", params=
                                    {
                                        'type': '2',
                                        'hostid': d.get('hostid'),
                                        'name': qt3,
                                        'key_': qt3,
                                        'delay': '0',
                                        'history': '1d',

                                        'trends': '1d',
                                        'status': '0',
                                        'value_type': '0',
                                        'description': qt3,
                                        'interfaceid': '0',
                                    }

                                                 )
                                diskinfo_info_a_2.remove(qt3)
                                print("item.create_ost.SUCCES_pri_up")

    if find != 1:
        print("not find host in server list")
        print("create new info host on server")
        z.do_request(method="host.create",params=
        {
            "host": namehost,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": lhip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": "2"  # группу не будем создавать втавляем большую часть в по умолчанию линукс
                }
            ],
            "templates": [
                {
                    "templateid": "10358"
                }
            ],
        }
                    )
        print("host.create.SUCCES")

        result1 = z.host.get(monitored_hosts=1, output='extend')
        for d in result1:
            if d.get('name') == namehost:
                print(d.get('name') == namehost)
                print("Find your host")
                print(d.get('name'))
                find = 1
                hid = d.get('hostid')
                print(hid)
                if diskinfo_info_a_2 != []:
                    for q3 in diskinfo_info_a_2:
                        diskinfo_info_a.remove(q3)
                        print("create_stats")
                        # print (diskinfo_info_a_2)
                        z.do_request(method="item.create", params=
                            {
                                'type': '2',
                                'hostid': d.get('hostid'),
                                'name': q3,
                                'key_': q3,
                                'delay': '0',
                                'history': '1d',
                                'trends': '1d',
                                'status': '0',
                                'value_type': '0',
                                'description': q3,
                                'interfaceid': '0'
                            }
                                         )
                            #print (diskinfo_info_a)
                        print("item.create_new_host.SUCCES")
    print("logout")
    z.user.logout();




