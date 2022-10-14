import subprocess
import sys
import csv
from datetime import date
from os import environ
from os import path
from arcgis.gis import GIS
from time import sleep

try:
    # date when script is run
    date_today = date.today()
    # directory where ArcGIS Online Users Report and text file of "bad users" are saved
    # TODO: update this
    out_dir = r'C:\reports\arcgisonline\user-reports'
    # name of users report in ArcGIS Online
    users_report_name = 'ArcGIS Online Users Report {}'.format(date_today)
    # name of arcgis online users report downloaded to local drive
    users_report_local_name = '{} Export.csv'.format(users_report_name)
    # text file that will list potentially bad users from ArcGIS Online
    # users who may no longer work for organization
    bad_users_report_name = 'Potential-Bad-Users-for-ArcGIS-Online-{}.txt'.format(date_today)
    # directory for log file that reports on script processes
    # TODO: update directory
    script_report_dir = r'C:\logs\ago-user-reports'
    # text file containing messages of script processing
    script_report_name = 'Search AGO User in AD Report {}.txt'.format(date_today)
    # placeholder for messages added to report text file
    log_message = ''

    # list containing usernames from ArcGIS Online
    usernames_list = []
    # formatted list of user names to run 'net user' on
    # only required if usernames in ArcGIS Online are different than usernames
    # in Active Directory
    formatted_usernames_list = []
    # list of potential users no longer working for organization ('bad users')
    bad_users_list = []

    log_message += 'logging into ArcGIS Online...\n'
    # login into AGO
    # TODO: update parameters
    # assumes admin account credentials saved in operating system environment variable
    gis = GIS('https://[slug].maps.arcgis.com/', environ.get('username'), environ.get('password'))
    log_message += '\nGIS: {}\n'.format(gis)
    log_message += '\ngenerating report of ArcGIS Online users...\n'

    # generate ArcGIS Online Users Report
    users_report = gis.admin.usage_reports.generate_report('org', 'users', users_report_name, future=False)
    # delay searching for item; time needed for item to show up in ArcGIS Online
    sleep(120)

    # test that 'itemId' key exists
    if 'itemId' in users_report.keys():
        # convert to string format
        itemId = str(users_report['itemId'])
        # get generated user report
        users_report_item = gis.content.get(itemId)
        log_message += '\nUsers report itemID is "{}"\n'.format(itemId)
    # if 'itemId' key does not exist, user report does not likely exist
    else:
        log_message += '\nCould not find generated Users Report\n'
        log_message += '\nEnding script'
        # exit script
        sys.exit()

    log_message += '\ndownloading Users Report to "{}"\n'.format(out_dir)
    # download user report (csv) to local disk
    users_report_item.download(out_dir, users_report_local_name)
    log_message += '\ncompleted downloading Users Report\n'

    # delete generated report in ArcGIS Online
    try:
        users_report_item.delete()
        log_message += '\ncompleted deleteing Users Report in ArcGIS Online\n'
    except:
        log_message += '\failed to delete Users Report in ArcGIS Online\n'

    # reference downloaded CSV file (Users Report)
    with open(path.join(out_dir, users_report_local_name), 'r') as csvfile:
        datareader = csv.reader(csvfile)
        counter = 0
        for row in datareader:
            if counter > 0:
                # add username to list
                usernames_list.append(row[0])
            # increment counter
            counter += 1
    # end reading csv file
    log_message += '\nextracted usernames from Users Report\n'

    # format list of usernames to match active directory format
    # this step may not be needed for your organization
    """ for user in usernames_list:
        if '@' in user:
            formatted_usernames_list.append(user.split('@')[0].replace('_','-'))
        else:
            formatted_usernames_list.append(user.replace('_','-'))

    log_message += '\ncompleted reformatting usernames\n' """

    # iterate over list of users from ArcGIS Online
    # use either "usernames_list" or "formatted_usernames_list"
    #for user in formatted_usernames_list:
    for user in usernames_list:
        # if you have ArcGIS Online users who are not in Active Directory,
        # you can skip over checking them against Active Directory
        # skip over non-AD users
        if user == 'Headless-Account' or user == 'Taco_Tuesday':
            continue
        # run "net user" Windows command utility
        return_value = subprocess.run("net user {} /domain".format(user), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # convert returned data from "net user" to string format
        str_return_value = str(return_value)
        # format string to remove whitespace
        formatted_return_value = " ".join(str_return_value.split())
        # perform conditional test to extract bad users to list to write to text file
        if 'Account active Yes' not in formatted_return_value:
            # add user to list
            bad_users_list.append(user)

    # if there are no "bad users", no need to write text file report
    if len(bad_users_list) > 0:
        # write content to text file
        with open(path.join(out_dir, bad_users_report_name), 'w') as f:
            for user in bad_users_list:
                f.write('\n{}\n'.format(user))
        log_message += '\ncompleted adding bad users to report\n'
    else:
        log_message += '\nthere are no bad users in ArcGIS Online'
except (Exception, EnvironmentError) as e:
    # should I log old print statements to text file?
    tbE = sys.exc_info()[2]
    # Write the line number the error occured to the log file
    log_message += '\nerror at Line {}\n'.format(tbE.tb_lineno)
    # Write the error print to the log file
    log_message += '\nerror: {}\n'.format(str(e))
finally:
    try:
        with open(path.join(script_report_dir, script_report_name), 'w') as f:
            f.write(str(log_message))
    except:
        pass