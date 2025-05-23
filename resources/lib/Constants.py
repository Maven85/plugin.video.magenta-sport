# -*- coding: utf-8 -*-
# Module: Constants
# Author: asciidisco
# Created on: 24.07.2017
# License: MIT https://goo.gl/WA1kby

"""Static links & list of sports"""

from __future__ import unicode_literals

# KODI addon id
ADDON_ID = 'plugin.video.magenta-sport'

# urls for login & data retrival
PRL = 'https://'
BASE_URL = '{0}www.magentasport.de'.format(PRL)
LOGIN_LINK = '{0}/service/auth/web/login?headto={0}'.format(BASE_URL)
LOGIN_ENDPOINT = '{0}accounts.login.idm.telekom.com/factorx'.format(PRL)
API_URL = '{0}/api/v3'.format(BASE_URL)
API_NAVIGATION_PATH = '/navigation'
API_SALT = '55!#r%Rn3%xn?U?PX*k'
STREAM_ROUTE = '/service/player/v2/streamAccess'
STREAM_PARAMS = 'videoId=%VIDEO_ID%&label=2780_hls&cdn=telekom_cdn'
STREAM_DEFINITON_URL = '{0}{1}?{2}'.format(BASE_URL, STREAM_ROUTE, STREAM_PARAMS)
LICENSE_URL = 'https://multidrm.core.verimatrixcloud.net/widevine?authorization=%DRM_TOKEN%'
DAY_NAMES = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

# core event types
SPORTS_ADDITIONAL_INFOS = {
    31: {
        'prefix': 'Basketball - {0}'
    },
    6941: {
        'prefix': 'Basketball - {0}'
    },
    37: {
        'prefix': 'Basketball - {0}'
    },
    281: {
        'prefix': 'Basketball - {0}'
    },
    40: {
        'prefix': 'Basketball - {0}'
    },
    52: {
        'prefix': 'Eishockey - {0}'
    },
    9144: {
        'prefix': 'Eishockey - {0}'
    },
    13: {
        'prefix': 'Fußball - {0}'
    },
    64: {
        'prefix': 'Fußball - {0}'
    },
    67: {
        'prefix': 'Fußball - {0}'
    },
    106: {
        'prefix': 'Sky Sport Kompakt - {0}'
    },
    103: {
        'prefix': 'Sky Sport Kompakt - {0}'
    },
    109: {
        'prefix': 'Sky Sport Kompakt - {0}'
    }
}

# static menu items for various lists
STATICS = {
    'liga3': {
        'categories': [
            {
                'name': 'Alle Spieltage',
                'id': 'spieltage',
            }, {
                'name': 'Suche nach Datum',
                'id': 'bydate',
            }
        ]
    }
}


class Constants(object):
    """Access methods for static links & list of sports"""


    @classmethod
    def get_base_url(cls):
        """
        Returns the Magenta Sport base HTTP address

        :returns:  string -- Base address
        """
        return BASE_URL


    @classmethod
    def get_login_link(cls):
        """
        Returns the Magenta Sport login HTTP route

        :returns:  string -- Login route
        """
        return LOGIN_LINK


    @classmethod
    def get_login_endpoint(cls):
        """
        Returns the Magenta Sport login SSO endpoint

        :returns:  string -- SSO login endpoint
        """
        return LOGIN_ENDPOINT


    @classmethod
    def get_api_url(cls):
        """
        Returns the API URL

        :returns:  string -- API URL
        """
        return API_URL


    @classmethod
    def get_api_salt(cls):
        """
        Returns the API salt

        :returns:  string -- API salt
        """
        return API_SALT


    @classmethod
    def get_stream_definition_url(cls):
        """
        Returns the stream defintion URL,
        used to get the final stream URL.
        It contains a `%VIDEO_ID%` placeholder,
        that needs to be replaced in order to
        fetch the streams

        :returns:  string -- STREAM DEFINITION URL
        """
        return STREAM_DEFINITON_URL


    @classmethod
    def get_api_navigation_path(cls):
        """
        Returns the navigation path

        :returns:  string -- navigation path
        """
        return API_NAVIGATION_PATH


    @classmethod
    def get_sports_additional_infos(cls):
        """
        Returns dict of static sports additional informations

        :returns:  dict -- dict of static sports additional informations
        """
        return SPORTS_ADDITIONAL_INFOS


    @classmethod
    def get_statics_list(cls):
        """
        Returns list of static menu items for various categories

        :returns:  dict -- List of static menu items for various categories
        """
        return STATICS


    @classmethod
    def get_addon_id(cls):
        """
        Returns the addon id

        :returns:  string -- Addon ID
        """
        return ADDON_ID


    @classmethod
    def get_day_names(cls):
        """
        Returns the list of german day names

        :returns:  dict -- List of german day names
        """
        return DAY_NAMES


    @classmethod
    def get_license_url(cls):
        """
        Returns the license URL,
        used to get a valid license key.
        It contains a `%DRM_TOKEN%` placeholder,
        that needs to be replaced

        :returns:  string -- LICENSE URL
        """
        return LICENSE_URL
