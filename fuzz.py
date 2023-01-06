import os
import subprocess
import random
test_img = "cirros-0.5.1-x86_64-disk.img"
strings = ['%s%p%x%d', '.1024d', '%.2049d', '%p%p%p%p', '%x%x%x%x',
                   '%d%d%d%d', '%s%s%s%s', '%99999999999s', '%08x', '%%20d',
                   '%%20n', '%%20x', '%%20s', '%s%s%s%s%s%s%s%s%s%s',
                   '%p%p%p%p%p%p%p%p%p%p',
                   '%#0123456x%08x%x%s%p%d%n%o%u%c%h%l%q%j%z%Z%t%i%e%g%f%a%C' +
                   '%S%08x%%', '%s x 129', '%x x 257']
save = []
#  rebase [--object objectdef] [--image-opts] [-U] [-q] [-f fmt] [-t cache] [-T src_cache] [-p] [-u] -b backing_file [-F backing_fmt] filename

for i in range(30):
	com=[['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'check', '-f', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'check', '-f', 'qcow2', '-r', 'leaks'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'check', '-f', 'qcow2', '-r', 'all'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'snapshot', '-c', 'new'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'info', '-f', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'convert', '-c', '-f', 'qcow2', '-O', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'amend', '-o', 'compat=0.10', '-f', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'amend', '-o', 'lazy_refcounts=on', '-f', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'amend', '-o', 'lazy_refcounts=off', '-f', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'rebase', "-u",
             'backing_file=' + random.choice(strings), '-f', 'qcow2'],
            ['/home/afl/qcow2/qemu-7.2.0/build/qemu-img', 'rebase', '-u' , '-F' + random.choice(strings),
             '-f', 'qcow2']]
	print(f"[+] GENERATING: {i}.img ")
	cmd = "radamsa "+test_img+f" > in/{i}.img"
	os.system(cmd)
	test = f"qemg check -f qcow2 {i}.img"
	print(f"[*] Testing {i}.img")
	for j in com:
		cmds = []
		print("[+] Executing: '",j,"'")
		for l in j:
			cmds.append(l)
		cmds.append(f"in/{i}.img")
		if "convert" in j:
			cmds.append("converted_image.qcow2")
			out = subprocess.run(cmds, capture_output=True) 
		else:
			out = subprocess.run(cmds, capture_output=True)
		print("##############################################\n")
		print(out, "\n", out.returncode)
		print("##############################################\n")
		if str(out.returncode) != "0":
			if f"{i}.img" in save:
				continue
			else:
				save.append(f"{i}.img")


import datetime

# get the current date and time
timed=str(datetime.datetime.now().day)+"_"+str(datetime.datetime.now().hour)+"_"+str(datetime.datetime.now().minute)+"_"+str(datetime.datetime.now().second)
os.system(f"mkdir {timed}")
print("[*] Saving:",save)
for f in save:
	print(f"Saving {f}")
	cmod=f"cp in/{f} {timed}/{f}"
	os.system(cmod)
