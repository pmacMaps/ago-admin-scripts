# Creates a CSV file with publicly shared content from ArcGIS Online or Portal organization

# import modules
import sys
from os import environ
from get_org_public_content import get_content
from write_csv_file import write_data

# Run geoprocessing tool.
# If there is an error with the tool, it will break and run the code within the except statement
try:
    # arcgis online url
    # update url to match your organization
    ago_url = 'https://{your org slug}.maps.arcgis.com/'
    # arcgis online username
    # method uses environment variables on machine running script
    username = environ.get('username_for_ago')
    # arcgis online password
     # method uses environment variables on machine running script
    password = environ.get('password_for_ago')
    # csv file to write data to
    # update to path where you want csv file created
    csv_file = r'C:\gis\logs\Public_Content_Report.csv'
    # get list of public content in ArcGIS Online
    public_content = get_content(ago_url, username, password)
    # print message
    print(f'writing data to csv file "{csv_file}"')
    # write content to csv file
    write_data(csv_file, public_content)
except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        print(f'error at Line {tbE.tb_lineno}')
        # Write the error print( to the log file
        print(f'error: {str(e)}')