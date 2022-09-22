# Creates a CSV file with web maps that contain deprecated basemaps, based upon the standard ArcGIS Online basemaps group (https://www.arcgis.com/home/group.html?id=702026e41f6641fb85da88efe79dc166#overview)

# Import system modules
import sys
from os import environ
from get_deprecated_basemaps import get_urls
from get_org_webmaps import get_maps
from get_webmap_dep_data import get_data
from write_csv_file import write_data

# Run geoprocessing tool
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
    csv_file = r'C:\gis\logs\Webmaps_With_Deprecated_Basemaps_Report.csv'
    # get deprecated map service urls
    deprecated_urls = get_urls(ago_url, username, password)
    # get web maps in organization
    web_maps = get_maps(ago_url, username, password)
    # get webmaps with deprecated basemaps
    webmaps_with_deprecated_basemaps = get_data(ago_url, username, password, web_maps, deprecated_urls)
    # write data to csv file
    write_data(csv_file, webmaps_with_deprecated_basemaps)
# If an error occurs running geoprocessing tool(s) capture error and write message
except (Exception, EnvironmentError) as e:
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    print(f"Failed at Line {tbE.tb_lineno}")
    # add the error message to the log message
    print(f"Error: {str(e)}")
finally:
    print(f'completed documenting webmaps with deprecated basemaps in "{ago_url}"')