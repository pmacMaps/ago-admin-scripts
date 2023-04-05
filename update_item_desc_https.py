# script generates list of all items in ArcGIS Online organization.  Then, it checks if 'http:' text is within the item description.  If it is, it replaces 'http' with 'https' text.  However, the validity of the updated url as https is not tested. You may want to add logic to test that

# import modules
import sys
from os import environ
from arcgis.gis import GIS
from get_org_content import get_items

# Run geoprocessing tool.
# If there is an error with the tool, it will break and run the code within the except statement
try:
    # arcgis online url
    ago_url = 'https://{ago-org-slug}.maps.arcgis.com/'
    # arcgis online username
    username = environ.get('your_ago_username_variable')
    # arcgis online password
    password = environ.get('your_ago_password_variable')
    # get list of public content in ArcGIS Online
    org_content = get_items(ago_url, username, password)
    # login into AGO
    gis = GIS(ago_url, username, password)
    print('checking if item descriptions contain "http:"')
    # iterate over content
    for item in org_content:
        # get item properties
        the_item = gis.content.get(item)
        # test if 'description' key exists
        if 'description' in the_item.keys():
            # description property
            item_desc = the_item['description']
            # test for not being None type
            if item_desc is not None:
                # check for 'http:' string
                if 'http:' in item_desc:
                    # update http: to https:
                    item_desc.replace('http:', 'https:')
                    print(f'updated item "{item}"')
except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        print(f'error at Line {tbE.tb_lineno}')
        # Write the error print( to the log file
        print(f'error: {str(e)}')