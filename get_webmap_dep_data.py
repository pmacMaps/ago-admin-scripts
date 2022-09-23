# Returns list of web maps with a deprecated basemap in ArcGIS Online or Portal organization

# import modules
import sys
from arcgis.gis import GIS

def get_data(url, username, password, webmaps, deprecated_basemaps):
    """Checks webmaps properties to see if it is using a deprecated basemap
       url = ArcGIS Online or Portal URL
       username = username for administrator account for ArcGIS Online or Portal
       password = password for administrator account for ArcGIS Online or Portal
       webmaps = list containing itemid for webmaps
       deprecated_basemaps = list containing map service urls for deprecated basemaps"""
    try:
        # list for web map itemid and associated basemap property
        webmap_data = []
        # login to ArcGIS Online
        gis = GIS(url, username, password)
        # add message
        print(f'logged into {gis}')
        print('generating list of webmaps with deprecated basemaps...')
        # loop over web maps and get basemap property
        for item in webmaps:
            # web map item
            map_item = gis.content.get(item)
            # web map data
            map_data = map_item.get_data()
            # list for webmap's basemap urls
            basemap_list = []
            # in case item does not have 'baseMap' or 'baseMapLayers' keys
            # TODO: test for dict keys properties instead of try/except
            try:
                # loop over basemap data for item
                for basemap in map_data['baseMap']['baseMapLayers']:
                        # in case item does not have 'url' key
                        try:
                            # check if basemap url is in deprecated basemaps list
                            if basemap['url'] in deprecated_basemaps:
                                basemap_list.append(basemap['url'])
                        # handle error with missing key
                        except KeyError:
                            # move to next item iterable
                            # newer/vector basemaps don't have 'url' key
                            continue
            # handle error with missing key
            except KeyError:
                # skip to next record
                continue
            # add data to list if the basemap is deprecated
            if len(basemap_list) > 0:
                # add itemid to beginning of sub-list
                basemap_list.insert(0, item)
                # add data to list
                webmap_data.append(basemap_list)
        # add message
        print('completed identifying webmaps with deprecated basemaps')
    except (Exception, EnvironmentError) as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        # TODO: generate file name through code logic
        print(f'error at Line {tbE.tb_lineno} in "get_webmap_dep_data.py')
        # Write the error print( to the log file
        print(f'error: {str(e)}')
    finally:
        # return list of deprecated basemap REST urls
        return webmap_data