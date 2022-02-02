# Returns list of itemid's and type for public-shared content in ArcGIS Online or Portal organization

# import modules
import sys
from arcgis.gis import GIS

def get_content(url, username, password):
    """Generate list of all publicly-shared content in ArcGIS Online organization
       url = ArcGIS Online or Portal URL
       username = username for administrator account for ArcGIS Online or Portal
       password = password for administrator account for ArcGIS Online or Portal"""
    try:
        # list to store items
        org_public_content = []
        # login to ArcGIS Online
        gis = GIS(url, username, password)
        # add message
        print('logged into {}'.format(gis))
        print('generating list of users...')

        # generate list of users in ArcGIS Online organization
        # update 'max_users' to account for number of users in your organization
        org_users = gis.users.search(query=None, sort_field='username', sort_order='asc', max_users=500, outside_org=False, exclude_system=True)
        # add message
        print('generated list of users')        
        print('generating list of public content in organization...')
        # loop over users in organization
        for user in org_users:
            # get items in user's root directory
            user_root_items = user.items()
            # user's folders
            user_folders = user.folders
            # get content in user's root directory
            for item in user_root_items:
                # focus on public items
                if item.access == 'public':
                    # add item's itemid and type to list
                    org_public_content.append([item.itemid, item.type])
            # end user's root directory
            # loop over user's oflders
            for folder in user_folders:
                # get items in folder
                folder_items = user.items(folder=folder['title'])
                # get items in each user's folder
                for item in folder_items:
                     # focus on public items
                    if item['access'] == 'public':
                        # add item's itemid and type to list
                        org_public_content.append([item.itemid, item.type])
            # end user's folders
        # add message
        print('completed generating list of public content in organization')
    except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        # TODO: generate file name through code logic
        print('error at Line {} in "get_org_public_content.py"'.format(tbE.tb_lineno))
        # Write the error print( to the log file
        print('error: {}'.format(str(e)))
    finally:
        # return list of public shared content in organization
        return org_public_content