from jinja2 import Markup
import config1 as cfg
from app import timemon
import psutil
import matplotlib
matplotlib.use('agg')
matplotlib.axes.Axes.pie
matplotlib.pyplot.pie
import matplotlib.pyplot as plt
import os
matplotlib.use('agg')
from matplotlib import pyplot as plt, pyplot, pylab
from operator import itemgetter

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) #инициализация демона только в инит.пу

def get_blocks():
    blocks = list()
    time_disk(blocks)
    time_disk1(blocks)
    cpu_percent(blocks)
    get_mem_info(blocks)
    get_disks_usage(blocks)##
    cpu_time(blocks)
    #print(blocks)
    return blocks

def get_mem_info(blocks):
    target = os.path.join(APP_ROOT, 'static/')
    fig= plt.figure(figsize=(2 * cfg.fig_hw, cfg.fig_hw))#2*4
    fig.set_facecolor('#F1F1F2')
    plt.subplot(1, 2, 1)
    labels = ['Available', 'Used', 'Free']
    mem = psutil.virtual_memory()
    fracs = [mem.available, mem.used, mem.free]

    lines = list()
    lines.append(str.format('Avaliable memory: {0} MB', round(mem.available/1024/1024,2)))
    lines.append(str.format('Used memory: {0} MB', round(mem.used/1024/1024,2)))
    lines.append(str.format('Free memory: {0} MB', round(mem.free/1024/1024,2)))

    plt.pie(fracs, labels=labels, shadow=True, autopct='%1.1f%%')

    plt.subplot(122, facecolor=(.95, .95, .95))
    plt.plot(timemon.mem_info,'xkcd:crimson')
    plt.ylabel('MB')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('Avaliable memory')
    plt.tight_layout()
    plt.grid(True, which='both')
    plt.ylim(-1,(round(mem.total/1024)/1024))
    fig.savefig('static/stickers_proxy.png', facecolor=fig.get_facecolor(), edgecolor='none')
    f = ("static/stickers_proxy.png")
    blocks.append({
        'title': 'Memory info',
        'graph': Markup (f),
        'data':
            {
                'primary': str.format("Total memory: {0} MB", round(mem.total/1024/1024,2)),
                'lines': lines
            }
            })
    pylab.close(fig)
    pyplot.clf()
    #print(blocks)

def get_disks_usage(blocks):
    num = 0
    fig = plt.figure(figsize=(2 * cfg.fig_hw, cfg.fig_hw))
    fig.set_facecolor('#F1F1F2')
    plt.subplot(121)
    if (cfg.type_container_VM == 'docker_podman_FS'):
        for dp in psutil.disk_partitions(' '):
            try:
                if (dp.device == 'rootfs' or (dp.device == 'tmpfs' and dp.mountpoint == '/dev') or (
                        dp.device == 'tmpfs' and dp.mountpoint == '/run/.containerenv')):
                    razv(dp,num,fig,blocks)
            except:
                continue
            pylab.close('all')  #######
            pyplot.clf()
            print(blocks)
    else:
        for dp in psutil.disk_partitions():
            try:
                razv(dp,num,fig,blocks)
            except:
                continue
            pylab.close('all')  #######
            pyplot.clf()
            print(blocks)

def razv(dp, num,fig,blocks):
    di = psutil.disk_usage(dp.mountpoint)
    labels = ['Free', 'Used', ]
    fracs = [di.free, di.used]
    plt.pie(fracs, labels=labels, shadow=True, autopct='%1.1f%%')
    plt.subplot(122, facecolor=(.95, .95, .95))
    plt.plot(list(map(itemgetter(num), timemon.disk_usage)))
    plt.ylabel('"%" MB')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('Disk available space')
    plt.tight_layout()
    plt.grid(True, which='both')
    plt.ylim(0)
    fig.savefig('static/' + str.format('stickers_proxy5 {0} .png', num), facecolor=fig.get_facecolor(),
                edgecolor='none')
    f = ('static/' + str.format('stickers_proxy5 {0} .png', num))
    # print(dp.device)
    # print(dp.mountpoint)
    blocks.append({
        'title': str.format('Disk razdel: {0} mountpont: {1}', dp.device, dp.mountpoint),
        'graph': Markup(f),
        'data':
            {
                'primary': '',
                'lines': [str.format('Free memory: {0} MB', round(di.free / 1024 / 1024, 2)),
                            str.format('Used memory: {0} MB', round(di.used / 1024 / 1024, 2))]
            }
    })
    num = num + 1
    return num,fig,blocks

def cpu_time(blocks):
    target = os.path.join(APP_ROOT, 'static/')
    fig = plt.figure(figsize=(2 * cfg.fig_hw, cfg.fig_hw))  # 2*4
    fig.set_facecolor('#F1F1F2')
    plt.subplot(1, 2, 1)
    cpu_time = psutil.cpu_times()
    fracs = [ cpu_time.system, cpu_time.user]
    lines = list()
    labels = [ 'system', 'user']

    #lines.append(str.format('колличество_потоков_CPU: %s' % psutil.NUM_CPUS))
    # lines.append(str.format('nice: %s' % cpu_time.nice))
    lines.append(str.format('system: %s' % round(cpu_time.system/1000,3)+ "s"))
    lines.append(str.format('idle: %s' % round(cpu_time.idle/1000,3)+ "s"))
    lines.append(str.format('user: %s' % round(cpu_time.user/1000,3)+ "s"))
    # lines.append(str.format('iowait: %s' % cpu_time.iowait))
    # lines.append(str.format('irq: %s' % cpu_time.irq))
    # lines.append(str.format('softirq: %s' % cpu_time.softirq))
    plt.bar(labels, fracs,0.40)

    plt.subplot(122, facecolor=(.95, .95, .95))
    plt.plot(timemon.cpu_time,alpha=2.5)

    plt.ylabel('min')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('                      user_process')
    plt.tight_layout()
    plt.grid(True, which='both')
    fig.savefig('static/stickers_proxy3.png', facecolor=fig.get_facecolor(), edgecolor='none')
    f = ('static/stickers_proxy3.png')

    blocks.append({
        'title': 'Time\nprocess',
        'graph': Markup(f),
        'data':
            {
                'primary': str.format("cpu_time_user: %s" % round(cpu_time.user/1000,3)+ "s"),
                'lines': lines
            }
    })
    pylab.close(fig)
    pyplot.clf()
    #print(blocks)

def cpu_percent(blocks):
    target = os.path.join(APP_ROOT, 'static/')
    fig = plt.figure(figsize=(2* cfg.fig_hw, cfg.fig_hw))  # 2*4
    fig.set_facecolor('#F1F1F2')
    plt.subplot(1,2,1)

    labels = ['user', 'system', 'idle']
    cpu_percent = psutil.cpu_times_percent(interval=1)

    fracs = [cpu_percent.user, cpu_percent.system, cpu_percent.idle]
    lines = list()

    lines.append(str.format('blue:user: %s' % cpu_percent.user + "%"))
    #lines.append(str.format('nice_time_to_prioryty': %s' % cpu_percent.nice))
    lines.append(str.format('orange:system: %s' % cpu_percent.system + "%"))
    lines.append(str.format('green:бездействия: %s' % cpu_percent.idle + "%"))
    # stats.append('iowait: %s' % cpu_percent.iowait)
    # stats.append('irq: %s' % cpu_percent.irq)
    # stats.append('softirq: %s' % cpu_percent.softirq)
    # stats.append('steal: %s' % cpu_percent.steal)
    # stats.append('guest: %s' % cpu_percent.guest)
    # stats.append('guest_nice: %s' % cpu_percent.guest_nice)
    plt.pie(fracs, labels=labels, shadow=True, autopct='%1.1f%%')

    plt.subplot(122)
    plt.rcParams['axes.facecolor']=(.95, .95, .95)
    plt.plot(timemon.cpu_percent,alpha=2.5)
    plt.ylabel('%')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('Состояния_работы_цпу')
    plt.tight_layout()
    plt.grid(True, which='both')
    plt.ylim(-1)
    fig.savefig('static/stickers_proxy2.png', facecolor=fig.get_facecolor(), edgecolor='none')
    f = ('static/stickers_proxy2.png')

    blocks.append({
        'title': 'CPU info',
        'graph': Markup(f),
        'data':
                     {
            'primary': str.format("status"),
            'lines': lines
                     }
                   })
    pylab.close(fig)
    pyplot.clf()
    #print(blocks)

def time_disk(blocks):
    target = os.path.join(APP_ROOT, 'static/')
    fig = plt.figure(figsize=(2* cfg.fig_hw, cfg.fig_hw))  # 2*4
    fig.set_facecolor('#F1F1F2')

    mi4 = psutil.disk_io_counters(perdisk=False, nowrap=True)
    if ((mi4 != None) and (cfg.type_container_VM == 'lxc')) or (cfg.type_container_VM == 'docker_podman_FS') or (
            (cfg.type_container_VM == 'linux') or (cfg.type_container_VM == 'windows')):
        razv2(fig,blocks)
    pylab.close(fig)
    pyplot.clf()
    #print(blocks)

def razv2(fig,blocks):
    lines = list()
    lines.append(str.format('blue: read_mb: %s' % round(timemon.rr1/1024/1024,3) + 'mb/s'))
    lines.append(str.format('write_mb: %s' % round(timemon.ttrr1/1024/1024,3) + 'mb/s'))

    plt.plot(timemon.time_disk,alpha=2.5)
    plt.rcParams['axes.facecolor']=(.95, .95, .95)
    plt.ylabel('MB')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('time READ/WRITE')
    #plt.tight_layout()
    plt.grid(True, which='both')
    plt.ylim(0)
    fig.savefig('static/stickers_proxy6.png', facecolor=fig.get_facecolor(), edgecolor='none')
    f = ('static/stickers_proxy6.png')
    #f = mpld3.display_d3(fig)

    blocks.append({
        'title': 'READ/WRITE',
        'graph': Markup(f),
        'data':
                     {
            'lines': lines
                     }
                   })
    return fig,blocks

def time_disk1(blocks):
    target = os.path.join(APP_ROOT, 'static/')
    fig = plt.figure(figsize=(2* cfg.fig_hw, cfg.fig_hw))  # 2*4
    fig.set_facecolor('#F1F1F2')

    time_disk1 = psutil.disk_io_counters(perdisk = False , nowrap = False )
    if (time_disk1 != None):
        lines = list()
        lines.append(str.format('read_count: %s' % round(time_disk1.write_count,3) + 'unit'))
        lines.append(str.format('write_count: %s' % round(time_disk1.read_count,3) + 'unit'))
        if (cfg.type_container_VM != 'docker_podman_FS'):
            lines.append(str.format('time_avg_otverta: %s' % round(timemon.time_disk1[-1],3) + 's'))
            p = timemon.time_disk1[-1] +( (timemon.time_disk1[-1]*0.25))
            plt.ylim(0, p)
        if (cfg.type_container_VM == 'docker_podman_FS'):
            plt.ylim(0)
        plt.plot(timemon.time_disk1,alpha=2.5)
        plt.rcParams['axes.facecolor'] = (.95, .95, .95)
        plt.ylabel('units')
        plt.xlabel(str.format('Interval {0} s', cfg.time_step))
        plt.title('time_avg_otverta')
        plt.grid(True, which='both')
        plt.autoscale(tight=False)
        fig.savefig('static/stickers_proxy7.png', facecolor=fig.get_facecolor(), edgecolor='none')
        f = ('static/stickers_proxy7.png')
        blocks.append({
            'title': 'Колличество чтений и записей в шаг (time_avg_otverta)',
            'graph': Markup(f),
            'data':
                         {
                'lines': lines
                         }
                       })
    pylab.close(fig)
    pyplot.clf()
    #print(blocks)





