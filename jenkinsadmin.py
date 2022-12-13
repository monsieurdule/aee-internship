from api4jenkins import Jenkins
import configparser
import subprocess

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

option = input('Opcije:\n1 za stop sistema\n2 za start\n3 za backup\n4 start job\n')

if (option=='1'):
	client.system.quiet_down() #sleep jenkins

if (option=='2'):
	client.system.cancel_quiet_down() #wake jenkins

if (option=='3'):
	subprocess.run(['rm', f"{jenkins_backup_dir}jenkins_backup.tar.gz"]) #remove previous archive file
	subprocess.run(['docker', 'cp', f'{jenkins_container_name}:{jenkins_workdir}', f'{jenkins_backup_dir}/{jenkins_backup_folder}']) #copy jenkins workdir to backup folder
	subprocess.run(['tar', '-czvf', f'{jenkins_backup_dir}/jenkins_backup.tar.gz', f'{jenkins_backup_dir}/{jenkins_backup_folder}']) #tar the backup folder
	subprocess.run(['rm', '-rf', f'{jenkins_backup_dir}/{jenkins_backup_folder}']) #remove folder, leave only .tar

if (option=='4'):
	job = client.get_job(jenkins_job_name) #job name is predefined in config file
	#print(job)
	item = client.build_job(jenkins_job_name) #build job and save it as "item"
	build = item.get_build() #save the build as variable so we can use later
	print(build)
	s = input('Press any key to stop it\n')
	if (s): #if any key is entered job will stop
		#job = client.get_job(jenkins_job_name)
		last_build = job.get_last_build() #get the last build
		last_build.stop() #stop it