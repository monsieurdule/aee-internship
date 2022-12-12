#from sys import exit
from api4jenkins import Jenkins
import os

#print('hello world')

#from jenkinsapi.jenkins import Jenkins

config_obj = configparser.ConfigParser()
config_obj.read("/remote_homes/djovanovic/djovanovic_lab/configfile.ini")

client = Jenkins('http://192.168.10.200:8085', auth=('admin', '8c26480cf3254192ae319a87a8218715'))
print(client.version)
#if (item.exists()):
	#print('item exists')
o=input('Opcije:\n1 za stop sistema\n2 za start\n3 za backup\n4 start job\n')
if (o=='1'):
	client.system.quiet_down()
if (o=='2'):
	client.system.cancel_quiet_down()
if (o=='3'):
	os.system('docker cp jenkins_compose_jenkins-master_1:/var/jenkins_home ~/djovanovic_lab/jenkins_backup')
	os.system('tar -czvf jenkins_backup.tar.gz ~/djovanovic_lab/jenkins_backup')
if (o=='4'):
	job = client.get_job('forkproj-jenkins-pipeline')
	print(job)
	item = client.build_job('forkproj-jenkins-pipeline')
	build = item.get_build()
	print(build)
	s = input('Press any key to stop it\n')
	if (s):
#if (o=='5'):
		job = client.get_job('forkproj-jenkins-pipeline')
		last_build = job.get_last_build()
		last_build.stop()
exit()
