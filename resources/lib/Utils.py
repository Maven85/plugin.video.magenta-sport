# -*- coding: utf-8 -*-
# Module: Utils
# Author: asciidisco
# Created on: 24.07.2017
# License: MIT https://goo.gl/WA1kby

"""General plugin utils"""

from __future__ import unicode_literals
from kodi_six.utils import PY2
from datetime import datetime
from hashlib import sha224, sha256
from json import dumps, loads
from re import search
import xbmc
import xbmcaddon

if PY2:
    from urllib import urlencode
    from xbmc import translatePath
else:
    from urllib.parse import urlencode
    from xbmcvfs import translatePath


class Utils(object):
    """General plugin utils"""


    def __init__(self, kodi_base_url, constants):
        """
        Injects instances & the plugin handle

        :param kodi_base_url: Plugin base url
        :type kodi_base_url: string
        :param constants: Constants instance
        :type constants: resources.lib.Constants
        """
        self.constants = constants
        self.kodi_base_url = kodi_base_url


    def get_addon_data(self):
        """
        Returns the relevant addon data for the plugin,
        e.g. name, version, default fanart, base data path & cookie pathname

        :returns:  dict - Addon data
        """
        addon = self.get_addon()
        base_data_path = translatePath(addon.getAddonInfo('profile'))
        return dict(
            plugin=addon.getAddonInfo('name'),
            version=addon.getAddonInfo('version'),
            fanart=addon.getAddonInfo('fanart'),
            base_data_path=base_data_path,
            cookie_path='{0}COOKIE'.format(base_data_path))


    def log(self, msg, level=xbmc.LOGINFO):
        """
        Logs a message to the Kodi log (default debug)

        :param msg: Message to be logged
        :type msg: mixed
        :param level: Log level
        :type level: int
        """
        addon_data = self.get_addon_data()
        xbmc.log('[{0}] {1}'.format(addon_data.get('plugin'), msg), level)


    def get_local_string(self, string_id):
        """
        Fetches a translated string from the po files

        :param string_id: Id of the string to be translated
        :type string_id: int
        :returns:  string - Translated string
        """
        src = xbmc if string_id < 30000 else self.get_addon()
        return src.getLocalizedString(string_id)


    def build_url(self, query):
        """
        Generates an URL for internal plugin navigation

        :param query: Map of request params
        :type query: dict
        :returns:  string - Url
        """
        return '{0}?{1}'.format(self.kodi_base_url, urlencode(query))


    def get_addon(self):
        """
        Returns an Kodi addon instance

        :returns:  xbmcaddon.Addon - Addon instance
        """
        return xbmcaddon.Addon(self.constants.get_addon_id())


    def build_api_url(self, url, query=dict()):
        """
        Generates an URL for api usage

        :param path: api path
        :type query: string
        :param query: Map of request params
        :type query: dict
        :returns:  string - Url
        """
        match = search('.*?(\/api\/v3\/[^?]*)', url)
        if match:
            path = match.group(1)
            query.update(dict(token=self.generate_api_token(path)))
        if query:
            return '{0}?{1}'.format(url, urlencode(query))
        else:
            return url


    def generate_api_token(self, path):
        """
        Generates an api token

        :param url: path for which the token is generated
        :type path: string
        :returns:  string - token
        """
        salt = self.constants.get_api_salt()
        utc = int((datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime(1970, 1, 1)).total_seconds())
        return self.generate_hash256('{0}{1}{2}'.format(salt, utc, path))


    def get_api_url(self):
        """
        Returns the API URL

        :returns:  string -- API URL
        """
        return self.constants.get_api_base_url().format(self.get_addon().getSetting('api_version').lower())


    @classmethod
    def generate_hash224(cls, text):
        """
        Returns an hash for a given text

        :param text: String to be hashed
        :type text: string
        :returns:  string - Hash
        """
        return sha224(text.encode('utf-8')).hexdigest()


    @classmethod
    def generate_hash256(cls, text):
        """
        Returns an hash for a given text

        :param text: String to be hashed
        :type text: string
        :returns:  string - Hash
        """
        return sha256(text.encode('utf-8')).hexdigest()


    @classmethod
    def capitalize(cls, sentence):
        """
        Capitalizes a sentence

        :param sentence: String to be capitalized
        :type sentence: string
        :returns:  string - Capitalized sentence
        """
        cap = ''
        words = sentence.split(' ')
        i = 0
        for word in words:
            if i > 0:
                cap = '{0} '.format(cap)
            cap = '{0}{1}{2}'.format(cap, word[:1].upper(), word[1:].lower())
            i += 1
        return cap


    @classmethod
    def get_kodi_version(cls):
        """
        Retrieves the Kodi version (Defaults to 18)

        :returns:  string - Kodi version
        """
        version = 18
        payload = {
            'jsonrpc': '2.0',
            'method': 'Application.GetProperties',
            'params': {
                'properties': ['version', 'name']
            },
            'id': 1
        }
        response = xbmc.executeJSONRPC(dumps(payload))
        response_serialized = loads(response)
        if 'error' not in response_serialized.keys():
            result = response_serialized.get('result', {})
            version_raw = result.get('version', {})
            version = version_raw.get('major', 18)
        return version


    @classmethod
    def get_inputstream_version(cls):
        """
        Retrieves the Inputsteam version (Defaults to 1.0.0)

        :returns:  string - Inputsteam version
        """
        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'Addons.GetAddonDetails',
            'params': {
                'addonid': 'inputstream.adaptive',
                'properties': ['enabled', 'version']
            }
        }
        # execute the request
        response = xbmc.executeJSONRPC(dumps(payload))
        response_serialized = loads(response)
        if 'error' not in response_serialized.keys():
            result = response_serialized.get('result', {})
            addon = result.get('addon', {})
            if addon.get('enabled', False) is True:
                return addon.get('version', '1.0.0')
        return '1.0.0'


    @classmethod
    def get_user_agent(cls):
        """Determines the user agent string for the current platform

        :returns:  str -- User agent string
        """
        base = 'Mozilla/5.0 {0} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        platform_str = cls.get_platform()
        # Mac OSX
        if platform_str == 'MacOSX':
            return base.format('(Macintosh; Intel Mac OS X 10_10_1)')
        # Windows
        if platform_str == 'Windows':
            return base.format('(Windows NT 10.0; Win64; x64)')
        # x86 Linux
        return base.format('(X11; Linux x86_64)')


    @classmethod
    def get_platform(cls):
        platform = 'Unknown'

        if xbmc.getCondVisibility('system.platform.osx'):
            platform = 'MacOSX'
        if xbmc.getCondVisibility('system.platform.atv2'):
            platform = 'AppleTV2'
        if xbmc.getCondVisibility('system.platform.tvos'):
            platform = 'tvOS'
        if xbmc.getCondVisibility('system.platform.ios'):
            platform = 'iOS'
        if xbmc.getCondVisibility('system.platform.windows'):
            platform = 'Windows'
        if xbmc.getCondVisibility('system.platform.raspberrypi'):
            platform = 'RaspberryPi'
        if xbmc.getCondVisibility('system.platform.linux'):
            platform = 'Linux'
        if xbmc.getCondVisibility('system.platform.android'):
            platform = 'Android'

        return platform
