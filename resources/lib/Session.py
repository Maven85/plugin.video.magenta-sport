# -*- coding: utf-8 -*-
# Module: Session
# Author: asciidisco
# Created on: 24.07.2017
# License: MIT https://goo.gl/WA1kby

"""Stores, loads & builds up a request session object. Provides login"""

from __future__ import unicode_literals
from kodi_six.utils import PY2
from bs4 import BeautifulSoup
from os import path, remove
from requests import session, utils
from time import time
import xbmcvfs

if PY2:
    from cPickle import dump, load, UnpicklingError
else:
    from pickle import dump, load, UnpicklingError


class Session(object):
    """Stores, loads & builds up a request session object. Provides login"""


    def __init__(self, constants, util, settings):
        """
        Injects instances, sets session file & loads initial session

        :param constants: Constants instance
        :type constants: resources.lib.Constants
        :param util: Utils instance
        :type util: resources.lib.Utils
        :param settings: Settings instance
        :type settings: resources.lib.Settings
        """
        self.constants = constants
        self.utils = util
        self.settings = settings
        addon = self.utils.get_addon()
        self.session_file = self.utils.get_addon_data().get('cookie_path')
        self._session = self.load_session()
        self.load_session_cookies()


    def get_session(self):
        """
        Returns the build up session object

        :returns:  requests.session -- Session object
        """
        return self._session


    def clear_session(self):
        """Clears the session, e.g. removes Cookie file"""
        if path.isfile(self.session_file):
            remove(self.session_file)
            self.get_session().cookies.clear_session_cookies()


    def save_session(self):
        """Persists the session, e.g. generates Cookie file"""
        with open(self.session_file, 'wb') as handle:
            dump(
                utils.dict_from_cookiejar(self._session.cookies),
                handle)


    def load_session(self):
        """
        Generates the build up session object,
        loads & deserializes Cookie file if exists

        :returns:  requests.session -- Session object
        """
        _session = session()
        _session.headers.update({
            'User-Agent': self.utils.get_user_agent(),
            'Accept-Encoding': 'gzip'
        })

        return _session


    def load_session_cookies(self):
        """
        loads & deserializes Cookie file if exists
        """
        if path.isfile(self.session_file):
            _cookies = None
            try:
                with open(self.session_file, 'rb') as handle:
                    _cookies = utils.cookiejar_from_dict(load(handle))
            except EOFError:
                _cookies = utils.cookiejar_from_dict({})
            except (ValueError, UnpicklingError):
                if self.settings.has_credentials():
                    USER, PASSWORD = self.settings.get_credentials()
                else:
                    USER, PASSWORD = self.settings.set_credentials()
                self.login(USER, PASSWORD, forceLogin=True)
            if _cookies:
                self._session.cookies = _cookies


    def login(self, user, password, forceLogin=False):
        """
        Logs in to the platform, fetches cookie headers and checks
        if the login succeeded

        :param user: Username/E-Mail
        :type user: string
        :param password: Password
        :type password: string
        :returns:  bool -- Login succeeded
        """
        # check if the suer is already logged in
        if forceLogin is False and path.isfile(self.session_file):
            file_time = xbmcvfs.Stat(self.session_file).st_mtime()
            if (time() - file_time) / 3600 < 24 and self.get_session().cookies.get('displayname'):
                return True
            else:
                self.clear_session()

        # get contents of login page
        res = self.get_session().get(self.constants.get_login_link())

        for i in [0, 1]:
            soup = BeautifulSoup(res.text, 'html.parser')
            # find all <input/> items in the login form & grep their data
            payload = {}
            for item in soup.find(id='login').find_all('input'):
                if item.attrs.get('name') and (item.attrs.get('name').startswith('xsrf') or item.attrs.get('name') == 'tid'):
                    payload[item.attrs.get('name')] = item.attrs.get('value', '')
            # overwrite user & password fields with our settings data
            if i == 0:
                payload['pw_usr'] = user
                payload['hidden_pwd'] = ''
            else:
                payload['hidden_usr'] = user
                payload['pw_pwd'] = password

            # persist the session
            # payload['persist_session'] = 1
            # add empyt sumbit field (it is the value of the button in the page...)
            payload['pw_submit'] = ''
            # do the login & read the incoming html <title/>
            # attribute to determine of the login was successfull
            res = self.get_session().post(
                self.constants.get_login_endpoint(),
                data=payload)

        success = self._session.cookies.get_dict().get('displayname')
        if success:
            self.save_session()
            return True
        return False


    def logout(self):
        """Clears the session"""
        self.clear_session()
        return self.settings.clear_credentials()


    def switch_account(self):
        """Clears the session & opens up credentials dialogs"""
        self.clear_session()
        return self.settings.set_credentials()
