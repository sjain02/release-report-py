URL_base="http://jaisa05n198660:8080/datamanagement/a/api"
API_version="/v4"
API_method="/releases-reports"
REST_method="GET" #GET|POST
username='superuser'
password='suser'

import requests
import csv
import sys

default_resolver=lambda x,y: x if y=='default' else y

def rest_call_wrapper(invocation_url,rest_method='GET',user='default',passw='default',postdata=None,headers=None):
    global username
    global password
    us=default_resolver(username,user)
    pw=default_resolver(password,passw)
    try:
        if rest_method=='GET':
            r=requests.get(invocation_url,auth=(us,pw))
        elif rest_method=='POST':
            if headers==None:
                r=requests.post(invocation_url,data=postdata,auth=(us,pw))
            else:
                r=requests.post(invocation_url,data=postdata,auth=(us,pw),headers=headers)
        if r.status_code==200:
            result=(r.json(),r.status_code)
        else:
            result=("",r.status_code)
    except requests.exceptions.ConnectionError as e:
                print("Connection Error :" +str(e))
                sys.exit(1)
    
    return result
    
        
def write_csv_file_dict(headers,dict_list,file_path=None):
    if file_path==None:
        raise ValueError("Please specify the file name or full path eg. release_report.csv or c://release_report.csv")

def read_csv_file_dict(file_path=None):
    if file_path==None:
        raise ValueError("Please specify the file name or full path eg. release_report.csv or c://release_report.csv")
    results = []
    with open(file_path) as File:
        reader = csv.DictReader(File)
        for row in reader:
            results.append(row)
    return results

def get_invocation_URL(status="ALL"):
    result=""
    if status=='ALL':
        result=URL_base+API_version+API_method
    if status.upper()=='ACTIVE':
        result=URL_base+API_version+API_method+"?releaseStatus=active"
    if status.upper()=='FAILED':
        result=URL_base+API_version+API_method+"?releaseStatus=failed"
    if status.upper()=='SUCCEEDED':
        result=URL_base+API_version+API_method+"?releaseStatus=succeeded"
    if status.upper()=='CANCELED':
        result=URL_base+API_version+API_method+"?releaseStatus=canceled"
    return result

""" 
The REST API call for Release Automation
"""

def stop_releases(file_path=None,user='default',passw='default'):
    if file_path==None:
        raise ValueError("Please specify the file name or full path eg. release_report.csv or c://release_report.csv")
    results=read_csv_file_dict(file_path)
    headers={'Content-Type':'application/json'}
    invocation_url=URL_base+API_version+'/stop-release'
    postdata=""
    for i in results:
        postdata="{\"releaseId\":\""+str(i['id'])+"\"}"
        rest_call_wrapper(invocation_url,rest_method='POST',postdata=postdata,user=username,passw=password,headers=headers)


def get_release_report(rest_method='GET',user='default',passw='default',filename="release_report_all.csv",status="ALL"):
    result=rest_call_wrapper(get_invocation_URL(status),user=user,passw=passw)
    error_dict={};
    if result[1]==200:
        if len(result[0])>=1:
            with open(filename, 'w') as File:  
                try:
                    field_names=[k for k in result[0][0].keys()]
                    writer=csv.DictWriter(File,fieldnames=field_names)
                    writer.writeheader()
                    for i in result[0]:
                        try:
                            writer.writerow(i)
                        except ValueError:
                            error_dict=i.copy()
                except ValueError:
                    print("Error occurred")
        else:
            print("No Releases found with satus: " +str(status))
    else:
        print ("Exception occurred " + str(result[1]))
            
get_release_report(user="superuser",passw="suser",filename="Active_release.csv", status='active')
stop_releases('Active_release.csv')

#import releaseReportsChart as rc
#rc.getReports('all_release.csv')

