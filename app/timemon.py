import threading
import time
import psutil
import config1 as cfg
import socket
import requests

from pyzabbix import ZabbixMetric, ZabbixSender

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((cfg.zabbserv,80))
print(s.getsockname()[0])
lhip=(s.getsockname()[0])
s.close()
diskinfo_info_a =[]
metrics = []
a = bool
# Create name
namehost = '%s_%s - %s' % (cfg.type_container_VM, 'test', lhip)
servz ='%s%s/%s' % ('http://',cfg.zabbserv,"zabbix")

def f():
    try:
        print('check_connect_to_zabbx')
    #    socket.gethostbyaddr(cfg.zabbserv)
        r = requests.get(servz)

    #except socket.gaierror:
    #    print('false_connect_gaierror')
    #    return False
    #    print('false_connect')
    #except socket.herror:
    #    print('false_connect_herror')
    #    return False
    #except socket.timeout:
    #    print('false_connect_timeout')
    #    return False
    except requests.ConnectionError:  # ловит
        print('false_connect_herror')
        return False
    print('true_connect')
    return True
if f() == True:
    a = True
else:
    a = False
print (a)

s.close()

rr = 0
rr1 = 0
ww = 0
ww1 = 0
ttrr = 0
ttrr1 = 0
ttww = 0
ttww1 = 0
read = 0
write = 0
ccc = 0
wcc = 0
ccc1 = 0
wcc1 = 0

mem_info = list()
disk_usage = list()
cpu_time = list()
cpu_percent = list()
time_disk = list()
time_disk1 = list()

def timer_thread():
    while True:
        global rr
        global ww
        global ttrr
        global ttww
        global rr1
        global ww1
        global ttrr1
        global ttww1
        global read
        global write
        global ccc
        global ccc1
        global wcc
        global wcc1

        time.sleep(cfg.time_step)
        mi = psutil.virtual_memory()
        mi2 = psutil.cpu_times()
        mi3 = psutil.cpu_times_percent()
        mi4 = psutil.disk_io_counters(perdisk=False, nowrap = True)
        #['PhysicalDrive4'] #vda for unix(fs), overlay fs use timemonfs.py, win PhysicalDrive

        metrics = []

        if mem_info.__len__() >= cfg.max_items_count:
            mem_info.pop(0)

        if cpu_time.__len__() >= cfg.max_items_count:
            cpu_time.pop(0)

        if cpu_percent.__len__() >= cfg.max_items_count:
            cpu_percent.pop(0)

        if disk_usage.__len__() >= cfg.max_items_count:
            disk_usage.pop(0)

        if time_disk.__len__() >= cfg.max_items_count:
                time_disk.pop(0)

        if time_disk1.__len__() >= cfg.max_items_count:
                time_disk1.pop(0)

        di = list()

        if (cfg.type_container_VM == 'docker_podman_FS'):
            for dp in psutil.disk_partitions(' '):
                try:
                    if (dp.device == 'rootfs' or (dp.device == 'tmpfs' and dp.mountpoint == '/dev') or (
                            dp.device == 'tmpfs' and dp.mountpoint == '/run/.containerenv')):
                        du = psutil.disk_usage(dp.mountpoint)
                        di.append(du.percent)
                        disk_usage.append(di)

                        disk_send_zabx(dp, du, metrics)
                except:
                    continue
        else:
            for dp in psutil.disk_partitions():
                try:
                    du = psutil.disk_usage(dp.mountpoint)
                    di.append(du.percent)
                    disk_usage.append(di)

                    disk_send_zabx(dp,du,metrics)

                except:
                    continue

        mem_info.append([mi.available / 1024 / 1024])
        cpu_time.append([(round(mi2.user))/1000/60])
        cpu_percent.append([mi3.user,mi3.system])

        data_temlates_send_zabx1(mi, mi2, mi3, metrics)

        if ((mi4 != None) and (cfg.type_container_VM == 'lxc')) or (cfg.type_container_VM == 'docker_podman_FS') or (
                (cfg.type_container_VM == 'linux') or (cfg.type_container_VM == 'windows')):
            if rr>0:
                rr1 = mi4.read_bytes - rr
            rr = mi4.read_bytes

            if ttrr > 0 and ttrr <= mi4.write_bytes:
                ttrr1 = mi4.write_bytes - ttrr
            if ttrr >mi4.write_bytes:ttrr = 0
            ttrr = mi4.write_bytes

            if (rr1 > 0) and (ttrr1 <= 0):
                time_disk.append([((rr1 / 1024)) / 1024 / cfg.time_step, (write)])

                readr = ZabbixMetric(namehost, 'trap', ((rr1 / 1024)) / 1024 / cfg.time_step)
                metrics.append(readr)
                writer = ZabbixMetric(namehost, 'trap2', (write))
                metrics.append(writer)


            if (rr1 <= 0) and (ttrr1 > 0):
                time_disk.append([read, ((ttrr1 / 1024)) / 1024 / cfg.time_step])

                readr = ZabbixMetric(namehost, 'trap', read)
                metrics.append(readr)
                writer = ZabbixMetric(namehost, 'trap2', ((ttrr1 / 1024)) / 1024 / cfg.time_step)
                metrics.append(writer)



            if (rr1 <= 0) and (ttrr1 <= 0):
                time_disk.append([read, write])

                readr = ZabbixMetric(namehost, 'trap', read)
                metrics.append(readr)
                writer = ZabbixMetric(namehost, 'trap2', (write))
                metrics.append(writer)



            if (rr1 > 0) and (ttrr1 > 0):
                time_disk.append([((rr1 / 1024)) / 1024 / cfg.time_step, ((ttrr1 / 1024) / 1024 )/ cfg.time_step])

                readr = ZabbixMetric(namehost, 'trap', ((rr1 / 1024)) / 1024 / cfg.time_step)
                metrics.append(readr)
                writer = ZabbixMetric(namehost, 'trap2', ((ttrr1 / 1024) / 1024 )/ cfg.time_step)
                metrics.append(writer)

            if (read < 0): read = 0
            else:read = ((rr1 / 1024)) / 1024 / cfg.time_step
            if (write < 0): write = 0
            else:write = ((ttrr1 / 1024)) / 1024 / cfg.time_step

            if ccc>=0 and ccc<=mi4.read_count:
                ccc1 = mi4.read_count - ccc
                ccc = mi4.read_count
            if (ccc > mi4.read_count or ccc < 0): ccc = 0

            if wcc >= 0 and wcc <= mi4.write_count:
                wcc1 = mi4.write_count - wcc
                wcc = mi4.write_count
            if (wcc > mi4.write_count or wcc < 0):
                wcc = 0

            if (ccc1+wcc1)>0 and (ccc1+wcc1)<10^100:
                time_disk1.append(cfg.time_step/round(ccc1+wcc1))
                taor = ZabbixMetric(namehost, 'tao', cfg.time_step/round(ccc1+wcc1))
                metrics.append(taor)
            else:
                time_disk1.append(0)
                taor = ZabbixMetric(namehost, 'tao', 0)
                metrics.append(taor)
            #print(time_disk1)
            #print (metrics)

        if a != False:
            zbx = ZabbixSender(cfg.zabbserv)
            zbx.send(metrics)

def start():
    print('start fn')
    t = threading.Thread(target=timer_thread,
                         name="Monitor",
                         args=(),
                         daemon=True)
    print (t)
    t.start()

def data_temlates_send_zabx1(mi,mi2,mi3,metrics):

    rua = ZabbixMetric(namehost, 'rua', round(mi.available / 1024 / 1024, 2))
    ruu = ZabbixMetric(namehost, 'ruu', round(mi.used / 1024 / 1024, 2))
    ruf = ZabbixMetric(namehost, 'ruf', round(mi.free / 1024 / 1024, 2))
    metrics.append(rua)
    metrics.append(ruu)
    metrics.append(ruf)

    ctu = ZabbixMetric(namehost, 'ctu', round(mi2.user / 1000, 3))
    cts = ZabbixMetric(namehost, 'cts', round(mi2.system / 1000, 3))
    cti = ZabbixMetric(namehost, 'cti', round(mi2.idle / 1000, 3))
    metrics.append(ctu)
    metrics.append(cts)
    metrics.append(cti)

    cuu = ZabbixMetric(namehost, 'cuu', mi3.user)
    cus = ZabbixMetric(namehost, 'cus', mi3.system)
    cui = ZabbixMetric(namehost, 'cui', mi3.idle)
    metrics.append(cuu)
    metrics.append(cus)
    metrics.append(cui)

    return metrics

def disk_send_zabx(dp,du,metrics):
    diskinfo_info = '%s_%s - %s' % (dp.device, dp.mountpoint, dp.fstype)

    diskinfo_data = '%s' % (du.percent)
    diskinfo_info_data = '%s - %s' % (diskinfo_info, 'data')
    diskinfo_info_data = diskinfo_info_data.replace("\\", '_')
    diskinfo_info_data = diskinfo_info_data.replace("/", '_')
    diskinfo_info_data = diskinfo_info_data.replace(":", '_')
    diskinfo_info_data = diskinfo_info_data.replace(" ", '_')
    diskinfo_info_data = diskinfo_info_data.replace(",", '_')
    diskinfo_info_a.append(diskinfo_info_data)

    diskinfo_used = '%s' % (round(du.used / 1024 / 1024, 2))
    diskinfo_info_used = '%s - %s' % (diskinfo_info, 'used')
    diskinfo_info_used = diskinfo_info_used.replace("\\", '_')
    diskinfo_info_used = diskinfo_info_used.replace("/", '_')
    diskinfo_info_used = diskinfo_info_used.replace(":", '_')
    diskinfo_info_used = diskinfo_info_used.replace(" ", '_')
    diskinfo_info_used = diskinfo_info_used.replace(",", '_')
    diskinfo_info_a.append(diskinfo_info_used)

    diskinfo_free = '%s' % (round(du.free / 1024 / 1024, 2))
    diskinfo_info_free = '%s - %s' % (diskinfo_info, 'free')
    diskinfo_info_free = diskinfo_info_free.replace("\\", '_')
    diskinfo_info_free = diskinfo_info_free.replace("/", '_')
    diskinfo_info_free = diskinfo_info_free.replace(":", '_')
    diskinfo_info_free = diskinfo_info_free.replace(" ", '_')
    diskinfo_info_free = diskinfo_info_free.replace(",", '_')
    diskinfo_info_a.append(diskinfo_info_free)

    diskinfo_total = '%s' % (round(du.total / 1024 / 1024, 2))
    diskinfo_info_total = '%s - %s' % (diskinfo_info, 'total')
    diskinfo_info_total = diskinfo_info_total.replace("\\", '_')
    diskinfo_info_total = diskinfo_info_total.replace("/", '_')
    diskinfo_info_total = diskinfo_info_total.replace(":", '_')
    diskinfo_info_total = diskinfo_info_total.replace(" ", '_')
    diskinfo_info_total = diskinfo_info_total.replace(",", '_')
    diskinfo_info_a.append(diskinfo_info_total)

    send_disk_usage_data = ZabbixMetric(namehost, diskinfo_info_data, diskinfo_data)
    send_disk_usage_used = ZabbixMetric(namehost, diskinfo_info_used, diskinfo_used)
    send_disk_usage_free = ZabbixMetric(namehost, diskinfo_info_free, diskinfo_free)
    send_disk_usage_total = ZabbixMetric(namehost, diskinfo_info_total, diskinfo_total)
    metrics.append(send_disk_usage_data)
    metrics.append(send_disk_usage_used)
    metrics.append(send_disk_usage_free)
    metrics.append(send_disk_usage_total)
    # print(dp.mountpoint,diskinfo_data,diskinfo_used,diskinfo_free,diskinfo_total)

    return diskinfo_info_a, metrics

