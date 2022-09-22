# Module returns a list of all deprecated basemaps from ArcGIS Online Basemaps group
# see https://www.arcgis.com/home/group.html?id=702026e41f6641fb85da88efe79dc166#overview

# import modules
import sys
from arcgis.gis import GIS

def get_urls(url, username, password):
    """Get list of map service url's for deprecated ArcGIS Online basemaps.
       url = ArcGIS Online or Portal URL
       username = username for administrator account for ArcGIS Online or Portal
       password = password for administrator account for ArcGIS Online or Portal"""
    try:
        # list to store URLs of deprecated basemap map service REST services
        basemap_service_urls = []
        # login to ArcGIS Online
        gis = GIS(url, username, password)
        # add message
        print(f'logged into {gis}')

        # arcgis online standard basemaps group
        basemaps_group = gis.groups.get('702026e41f6641fb85da88efe79dc166')
        # get content within group
        group_content = basemaps_group.content()
        # add message
        print('got items in basemaps group')
        print('storing url\'s for deprecated basemaps...')

        # loop over items in basemap group
        for item in group_content:
            # check if item has 'contentStatus' key
            if 'contentStatus' in item.keys():
                # check if contentStatus is 'deprecated'
                if item['contentStatus'] == 'deprecated':
                    # get data/properties for item
                    item_data = item.get_data()
                    # in case item does not have 'baseMap' or 'baseMapLayers' keys
                    # TODO: convert to stacked conditional to test for both keys
                    try:
                        # loop over basemaps
                        for basemap in item_data['baseMap']['baseMapLayers']:
                            # add 'url' property to list
                            basemap_service_urls.append(basemap['url'])
                    # handle error with missing key
                    except KeyError:
                        # move onto to next item in list
                        continue
            else:
                print(f'{item} does not have "contentStatus" key')
        # end loop over group content
        # add message
        print('completed storing url\'s for deprecated basemaps')
    except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        # TODO: generate file name through code logic
        print('error at Line {} in "get_deprecated_basemaps.py'.format(tbE.tb_lineno))
        # Write the error print( to the log file
        print('error: {}'.format(str(e)))
    finally:
        # return list of deprecated basemap REST urls
        return basemap_service_urls