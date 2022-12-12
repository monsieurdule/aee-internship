from flask import Flask, request, abort
import gitlab
from api4jenkins import Jenkins
from jira import JIRA
import configparser
import os

config_obj = configparser.ConfigParser()
config_obj.read("/remote_homes/djovanovic/djovanovic_lab/pythonscripts/configfile.ini")

GitLabParameters = config_obj["GitLab"]
JenkinsParameters = config_obj["Jenkins"]
JiraParameters = config_obj["Jira"]

gl_url = GitLabParameters["url"]
gl_token = GitLabParameters["token"]

# gl = gitlab.Gitlab(url='http://192.168.10.200:8083/', private_token='glpat-Bk-DoGks9yW1fsBhgMP6')
gl = gitlab.Gitlab(url=gl_url, private_token=gl_token)

jenkins_url = JenkinsParameters["url"]
jenkins_username = JenkinsParameters["username"]
jenkins_password = JenkinsParameters["password"]
jenkins_job_name = JenkinsParameters["job_name"]

jenkins_client = Jenkins(jenkins_url, auth=(jenkins_username, jenkins_password))

jira_url = JiraParameters["url"]
jira_username = JiraParameters["username"]
jira_password = JiraParameters["password"]
jira_project_number = int(JiraParameters["project_number"])

jira = JIRA(server=jira_url, auth=(jira_username, jira_password))
issue_key = jira.projects()[jira_project_number].key
# projects = gl.projects.list(iterator=True)
# for project in projects:
#    print(project)
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        data = request.get_json()
        if "event_name" in data:
            print('there is event_name')
            if data['before'] == '0000000000000000000000000000000000000000' and data['event_name'] == 'push':
                tempdata = data['project']
                #proj_name = tempdata["name"]
                print(f'Starting merge request on  {tempdata["name"]}')
                proj_id = tempdata["id"]
                branch_name = data['ref'].split("/")
                project = gl.projects.get(proj_id)
                # print(type(branch_name)
                branch_name = branch_name[len(branch_name) - 1]
                print(branch_name)
                # commits = data['commits']
                # total_commits = data['total_commits_count']
                # before_commit = data['before']
                project.mergerequests.create({
                    'source_branch': branch_name,
                    'target_branch': 'main',
                    'title': f'merge {branch_name} into main',
                    'labels': ['label1', 'label2']})
                # gl.proj_name.mr.merge()
                return 'success', 200
                # starting a target job because push event is triggered
                job = jenkins_client.get_job(jenkins_job_name)
                item = jenkins_client.build_job(jenkins_job_name)
                build = item.get_build()
                return 'success', 200
    if "event_type" in data:
        if data['event_type'] == 'merge_request':
            print('merge request is going on')
            tempdata = data['project']
            print(type(tempdata))
            print(type(data))
            # source_proj = tempsrc["name"]
            # source_id = tempsrc["id"]
            # summary_tmp = source_id + source_proj
            # global issue_key
            # issue_key = jira.projects()[0].key
            print(issue_key)
            global new_issue
            oa = data['object_attributes']
            #sb = pa['source_branch']
            #tb = pa['target_branch']
            print(oa["source_branch"])
            print(oa["target_branch"])
            new_issue = jira.create_issue(project=issue_key,
                                          summary=f'On project {tempdata["name"]}, merging {oa["source_branch"]} into {oa["target_branch"]} branch',
                                          description='test', issuetype={'name': 'Bug'})
            return 'success', 200
    else:
        abort(400)


@app.route('/jenkinshook', methods=['POST'])
def jenkinshook():
    if request.method == 'POST':
        print(request.json)
        data = request.get_json()
        if "result" in data:
            if data['result'] == 'build success':
                print('Build successful')
                # fields = {'description': 'Jenkins build successful'}
                # issue_key = jira.projects()
                # update_issue = jira.issue_update(project=jira.projects()[0].key, description='edited')
                jira.add_comment(new_issue, "Successful build on Jenkins")
                print(issue_key)
                # jira.add_comment(issue_key, 'edited')
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='192.168.10.200', port=5001)

