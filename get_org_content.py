# generates a list of itemIds for all content in ArcGIS Online or Portal organization

# import modules
import sys
from arcgis.gis import GIS

def get_items(url, username, password):
    """Generate list of all content in ArcGIS Online organization
    url = ArcGIS Online organization url
    username = username for admin account in ArcGIS Online
    password = password for admin account in ArcGIS Online
    """
    try:
        # list to store itemId of all items
        org_items = []
        # login to ArcGIS Online
        gis = GIS(url, username, password)
        # add message
        print(f'logged into {gis}')
        print('generating list of users...')
        # generate list of users in ArcGIS Online organization
        # update max_users parameter if needed
        org_users = gis.users.search(query=None, sort_field='username', sort_order='asc', max_users=500, outside_org=False, exclude_system=True)

        # add message
        print('generated list of users')
        print('gathering up all itemids for organization items...')

        # loop over users in organization
        for user in org_users:
            # get items in user's root directory
            user_root_items = user.items()
            # user's folders
            user_folders = user.folders
            # get items in user's root directory
            for item in user_root_items:
                # add itemid to list
                org_items.append(item.itemid)
            # end user's root directory
            # loop over user's oflders
            for folder in user_folders:
                # get items in folder
                folder_items = user.items(folder=folder['title'])
                # get items
                for item in folder_items:
                    # add item id's to list
                    org_items.append(item.itemid)
            # end user's folders
        # add message
        print('completed generating list of itemIds for items in organization')
    except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        # update to use code to get name of file
        print(f'error at Line {tbE.tb_lineno} in "get_org_content.py')
        # Write the error print( to the log file
        print(f'error: {str(e)}')
    finally:
        # return list of itemid's for web maps
        return org_items