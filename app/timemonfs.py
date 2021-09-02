import threading
import time
import psutil
import config1 as cfg

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
        mi4 = psutil.disk_io_counters(perdisk=True, nowrap = True)['vda2'] #path to part all body

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
        for dp in psutil.disk_partitions(' '):
            try:
               if (dp.device=='rootfs' or (dp.device=='tmpfs' and dp.mountpoint=='/dev') or (dp.device=='tmpfs' and dp.mountpoint=='/run/.containerenv')):
                du = psutil.disk_usage(dp.mountpoint)
                di.append(du.percent)
                disk_usage.append(di)
            except:
                continue

        mem_info.append([mi.available / 1024 / 1024])
        cpu_time.append([(round(mi2.user))/1000/60])
        cpu_percent.append([mi3.user,mi3.system])

        if rr>0:
            rr1 = mi4.read_bytes - rr
        rr = mi4.read_bytes


        if ttrr > 0 and ttrr <= mi4.write_bytes:
            ttrr1 = mi4.write_bytes - ttrr
        if ttrr >mi4.write_bytes:ttrr = 0
        ttrr = mi4.write_bytes


        if (rr1 > 0) and (ttrr1 <= 0):
            time_disk.append([((rr1 / 1024)) / 1024 / cfg.time_step, (write)])
        if (rr1 <= 0) and (ttrr1 > 0):
            time_disk.append([read, ((ttrr1 / 1024)) / 1024 / cfg.time_step])
        if (rr1 <= 0) and (ttrr1 <= 0):
            time_disk.append([read, write])
        if (rr1 > 0) and (ttrr1 > 0):
            time_disk.append([((rr1 / 1024)) / 1024 / cfg.time_step, ((ttrr1 / 1024) / 1024 )/ cfg.time_step])
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

        if (ccc1+wcc1)>0 and (ccc1+wcc1)<10^100:time_disk1.append(cfg.time_step/round(ccc1+wcc1))
        else: time_disk1.append(0)


def start():
    print('start fn')
    t = threading.Thread(target=timer_thread,
                         name="Monitor",
                         args=(),
                         daemon=True)
    print (t)
    t.start()

