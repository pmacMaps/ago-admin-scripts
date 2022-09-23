# get's itemIds for all items in ArcGIS Online organization.  Iterates over items and checks if delete protection is enabled.  If not, it enables delete protection

# import modules
import sys
from os import environ
from os import path
from datetime import date
from arcgis.gis import GIS
from get_org_content import get_items

# Run geoprocessing tool.
# If there is an error with the tool, it will break and run the code within the except statement
try:
    # Date the script is being run
    date_today = date.today()
    # Date formatted as month-day-year (1-1-2020)
    formatted_date_today = date_today.strftime("%m-%d-%Y")
    # log file to write messages to
    log_file = path.join(r'C:\GIS\logs', f'AGO-Enable-Delete-Protection-{formatted_date_today}.txt')
    # container for messages to write to log file
    log_msg = ''
    # arcgis online url
    ago_url = 'https://{your org slug}.maps.arcgis.com/'
    # arcgis online username
    username = environ.get('username_for_ago')
    # arcgis online password
    password = environ.get('password_for_ago')
    # add message
    log_msg += 'Generating itemIds for content in ArcGIS Online...\n'
    # get list of content (itemsIds) in ArcGIS Online
    org_content = get_items(ago_url, username, password)
    # add message
    log_msg += '\nCompleted getting content itemIds\n'
    # login into AGO
    gis = GIS(ago_url, username, password)
    # add message
    log_msg += f'\nLogged into GIS: {gis}\n'
    # add message
    log_msg += '\nEnabling "delete protection" on content...\n'
    # iterate over content
    for item in org_content:
        # get item by id
        the_item = gis.content.get(item)
        # check if delete protection is not enabled
        if the_item.can_delete:
            # enable delete protection
            result = the_item.protect(enable=True)
            # expect 'success' key to exist
            if 'success' in result.keys():
                # check if value of "success" is False
                if result['success'] is False:
                    # print message
                    log_msg += f'\n\tFailed to enable delete protection for item "{item}"\n'
            # unexpected issue arose
            else:
                log_msg += f'\n\tCheck item "{item}" for delete protection status\n'
        # end if the_item.can_delete
    # end iteration
    # add message
    log_msg += '\nCompleted enabling delete protection for items\n'
except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        log_msg += f'\nError at Line {tbE.tb_lineno}\n'
        # Write the error print( to the log file
        log_msg += f'\nError: {str(e)}'
finally:
    # write message to log file
    try:
        with open(log_file, 'w') as f:
            f.write(str(log_msg))
    except:
        pass