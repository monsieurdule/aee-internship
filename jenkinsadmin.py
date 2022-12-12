#from sys import exit
from api4jenkins import Jenkins
import configparser
import os
config_obj = configparser.ConfigParser()
config_obj.read("/remote_homes/djovanovic/djovanovic_lab/pythonscripts/configfile.ini")

JenkinsParameters = config_obj["Jenkins"]

jenkins_url = JenkinsParameters["url"]
jenkins_username = JenkinsParameters["username"]
jenkins_password = JenkinsParameters["password"]
jenkins_job_name = JenkinsParameters["job_name"]
jenkins_backup_dir = JenkinsParameters["backup_dir"]
jenkins_container_name = JenkinsParameters["container_name"]
jenkins_workdir = JenkinsParameters["workdir"]
jenkins_backup_folder = JenkinsParameters["backup_folder"]

client = Jenkins(jenkins_url, auth=(jenkins_username, jenkins_password))

print(client.version)
#if (item.exists()):
	#print('item exists')
option = input('Opcije:\n1 za stop sistema\n2 za start\n3 za backup\n4 start job\n')

#match option:
	#case "1":
if (option=='1'):
	client.system.quiet_down()
#case '2':
if (option=='2'):
	client.system.cancel_quiet_down()
#case '3':
if (option=='3'):
	os.system(f'docker cp {jenkins_container_name}:{jenkins_workdir} {jenkins_backup_dir}{jenkins_backup_folder}')
	#os.system('docker cp jenkins_compose_jenkins-master_1:/var/jenkins_home ~/djovanovic_lab/jenkins_backup')
	os.system(f'tar -czvf {jenkins_backup_dir}/jenkins_backup.tar.gz {jenkins_backup_dir}')
	#os.system('tar -czvf jenkins_backup.tar.gz ~/djovanovic_lab/jenkins_backup')
	os.system(f'rm -rf {jenkins_backup_dir}/{jenkins_backup_folder}')
#case '4':
if (option=='4'):
	job = client.get_job(jenkins_job_name)
	print(job)
	item = client.build_job(jenkins_job_name)
	build = item.get_build()
	print(build)
	s = input('Press any key to stop it\n')
	if (s):
		job = client.get_job(jenkins_job_name)
		last_build = job.get_last_build()
		last_build.stop()
#exit()