import psutil
import platform
import json

def secs2hours(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	return "%d:%02d:%02d" % (hh, mm, ss)
def bytes2gb(bytes, bsize=1024):
        r = float(bytes)
        r = r / (bsize*bsize*bsize)
        return(r)

lis={}
r=platform.system()
lis["System Information"]={}
lis["System Information"]["OS"]=r
lis["System Information"]["Release"]=platform.release()
lis["System Information"]["Version"]=platform.version()
lis["System Information"]["Platform"]=platform.platform()
lis["System Information"]["Machine"]=platform.machine()
lis["CPU Information"]={}
lis["CPU Information"]["CPU count"]=psutil.cpu_count(logical=False)
lis["CPU Information"]["CPU utilisation percent"]=psutil.cpu_times_percent(interval=None, percpu=False)
r=psutil.cpu_freq()
lis["CPU Information"]["Current CPU frequency"]=r.current
lis["CPU Information"]["Minimum CPU frequency"]=r.min
lis["CPU Information"]["Maximum CPU frequency"]=r.max
users=psutil.users()
lis["User Information"]={}
for user in users:
        lis["User Information"]["UserName"]=user.name
        lis["User Information"]["Terminal"]=user.terminal
        lis["User Information"]["Host"]=user.host
mem=psutil.virtual_memory()
lis["RAM"]={}
lis["RAM"]["Total"]=str(bytes2gb(mem.total))+'GB'
lis["RAM"]["Available"]=str(bytes2gb(mem.available))+'GB'
lis["RAM"]["Used"]=str(bytes2gb(mem.used))+'GB'
disks=psutil.disk_partitions()
lis["Disk Partitions"]={}
for disk in disks:
        lis["Disk Partitions"][disk.device]={}
        lis["Disk Partitions"][disk.device]["Name"]=disk.device
        lis["Disk Partitions"][disk.device]["Mount Point"]=disk.mountpoint
        lis["Disk Partitions"][disk.device]["Disk Type"]=disk.fstype
parts=psutil.disk_partitions()
for part in parts:
        temp=psutil.disk_usage(''+part.device)
        lis["Usage of "+part.device]={}
        lis["Usage of "+part.device]["Total"]=str(bytes2gb(temp.total))+'GB'
        lis["Usage of "+part.device]["Used"]=str(bytes2gb(temp.used))+'GB'
        lis["Usage of "+part.device]["Free"]=str(bytes2gb(temp.free))+'GB'
lis["Battery Information"]={}
battery = psutil.sensors_battery()
lis["Battery Information"]["Battery Percentage"]=battery.percent
lis["Battery Information"]["Battery Time Left"]=secs2hours(battery.secsleft)

#OrderedDict(sorted(lis.items(), key=lambda t: t[0]))

        
with open('systeminfo.json', 'w') as outfile:
        outfile.write(json.dumps(lis,sort_keys=True, ensure_ascii=False,indent = 4,))

