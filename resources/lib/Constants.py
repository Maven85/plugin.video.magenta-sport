# -*- coding: utf-8 -*-
# Module: Constants
# Author: asciidisco
# Created on: 24.07.2017
# License: MIT https://goo.gl/WA1kby

"""Static links & list of sports"""

# KODI addon id
ADDON_ID = 'plugin.video.magenta-sport'

# urls for login & data retrival
PRL = 'https://'
BASE_URL = PRL + 'www.magentasport.de'
LOGIN_LINK = BASE_URL + '/service/auth/web/login?headto=' + BASE_URL
LOGIN_ENDPOINT = PRL + 'accounts.login.idm.telekom.com/factorx'
EPG_URL = BASE_URL + '/api/v2/'
STREAM_ROUTE = '/service/player/streamAccess'
STREAM_PARAMS = 'videoId=%VIDEO_ID%&label=2780_hls'
STREAM_DEFINITON_URL = BASE_URL + STREAM_ROUTE + '?' + STREAM_PARAMS
FANART_URL = PRL + 'raw.githubusercontent.com/hubsif/kodi-telekomsport/master'
DAY_NAMES = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

# core event types
SPORTS = {
    'liga3': {
        'image': BASE_URL + '/images/editorial/Logos/Bewerb-Logos/3_liga.png',
        'fanart': FANART_URL + '/resources/fanart/3.liga.jpg',
        'name': 'Fußball - 3. Liga',
        'indicators': ['3. Liga'],
        'page': 'fussball/3-liga',
        'target': '/page/64',
        'epg': '',
    },
    'ffb': {
        'image': BASE_URL + '/images/packete/frauenbundesliga.png',
        'fanart': FANART_URL + '/resources/fanart/frauen-bundesliga.jpg',
        'name': 'Fußball -  Allianz Frauen-Bundesliga',
        'indicators': [''],
        'page': 'fussball/frauen-bundesliga',
        'target': '/page/67',
        'epg': '',
    },
    'bbl': {
        'image': BASE_URL + '/images/editorial/Logos/Bewerb-Logos/bbl.png',
        'fanart': FANART_URL + '/resources/fanart/bbl.jpg',
        'name': 'Basketball - easyCredit BBL',
        'indicators': [''],
        'page': 'basketball/bbl',
        'target': '/page/31',
        'epg': '',
    },
    'bblpokal': {
        'image': BASE_URL + '/images/infoNeu/logos/bbl-pokal-white.png',
        'fanart': '',
        'name': 'Basketball - BBL Pokal',
        'indicators': [''],
        'page': '/basketball/bbl_pokal',
        'target': '/page/6941',
        'epg': '',
    },
    'bel': {
        'image': BASE_URL + '/images/packete/euroleague.png',
        'fanart': FANART_URL + '/resources/fanart/euroleague.jpg',
        'name': 'Basketball - Turkish Airlines EuroLeague',
        'indicators': [''],
        'page': 'basketball/euroleague',
        'target': '/page/37',
        'epg': '',
    },
    'bec': {
        'image': BASE_URL + '/images/infoNeu/logos/EuroCup.png',
        'fanart': '',
        'name': 'Basketball - 7Days EuroCup',
        'indicators': [''],
        'page': '/basketball/eurocup',
        'target': '/page/281',
        'epg': '',
    },
    'bls': {
        'image': BASE_URL + '/images/editorial/Logos/Bewerb-Logos/bbl-laenderspiele.png',
        'fanart': '',
        'name': 'Basketball - Basketball-Länderspiele',
        'indicators': [''],
        'page': '/basketball/laenderspiele',
        'target': '/page/40',
        'epg': '',
    },
    'del': {
        'image': BASE_URL + '/images/editorial/Logos/Bewerb-Logos/del.png',
        'fanart': FANART_URL + '/resources/fanart/del.jpg',
        'name': 'Eishockey - Deutsche Eishockey Liga',
        'indicators': [''],
        'page': 'eishockey/del',
        'target': '/page/52',
        'epg': '',
    },
    'fcb': {
        'image': BASE_URL + '/images/packete/fcbayerntv.png',
        'fanart': FANART_URL + '/resources/fanart/fcbtv.jpg',
        'name': 'FC Bayern.tv live',
        'indicators': [''],
        'page': 'fc-bayern-tv-live',
        'target': '/page/13',
        'epg': '',
    },
    'boxen': {
        'image': BASE_URL + '/images/epg/ran-fighting.png',
        'fanart': '',
        'name': 'FIGHTING - Boxen',
        'indicators': [''],
        'page': 'fighting',
        'target': '/page/85',
        'epg': '',
    },
    'mma': {
        'image': BASE_URL + '/images/epg/ran-fighting.png',
        'fanart': '',
        'name': 'FIGHTING - MMA',
        'indicators': [''],
        'page': 'fighting/mma',
        'target': '/page/88',
        'epg': '',
    },
    'wrestling': {
        'image': BASE_URL + '/images/epg/ran-fighting.png',
        'fanart': '',
        'name': 'FIGHTING - Wrestling',
        'indicators': [''],
        'page': 'fighting/wrestling',
        'target': '/page/91',
        'epg': '',
    },
    'fbotr': {
        'image': BASE_URL + '/images/epg/ran-fighting.png',
        'fanart': '',
        'name': 'FIGHTING - Weitere Kampfsportarten',
        'indicators': [''],
        'page': 'fighting/bestoftherest',
        'target': '/page/296',
        'epg': '',
    },
    'skybuli': {
        'image': BASE_URL + '/images/editorial/Logos/Sky/bl_logo_SKY.png',
        'fanart': FANART_URL + '/resources/fanart/bundesliga.jpg',
        'name': 'Sky Sport Kompakt - Fußball-Bundesliga',
        'indicators': [''],
        'page': 'sky/bundesliga',
        'target': '/page/106',
        'epg': '',
    },
    'skychamp': {
        'image': BASE_URL + '/images/editorial/Logos/Bewerb-Logos/UCL_Sky_composite_Outline_new__003_.png',
        'fanart': FANART_URL + '/resources/fanart/uefa.jpg',
        'name': 'Sky Sport Kompakt - UEFA Champions League',
        'indicators': [''],
        'page': 'sky/champions-league',
        'target': '/page/103',
        'epg': '',
    },
    'skyhandball': {
        'image': BASE_URL + '/images/editorial/Logos/Bewerb-Logos/sky-dkb.png',
        'fanart': FANART_URL + '/resources/fanart/hbl.jpg',
        'name': 'Sky Sport Kompakt - DKB Handball-Bundesliga',
        'indicators': [''],
        'page': 'sky/handball-bundesliga',
        'target': '/page/109',
        'epg': '',
    },
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
        Returns the Telekom sport base HTTP address

        :returns:  string -- Base address
        """
        return BASE_URL

    @classmethod
    def get_login_link(cls):
        """
        Returns the Telekom Sport login HTTP route

        :returns:  string -- Login route
        """
        return LOGIN_LINK

    @classmethod
    def get_login_endpoint(cls):
        """
        Returns the Telekom login SSO endpoint

        :returns:  string -- SSO login endpoint
        """
        return LOGIN_ENDPOINT

    @classmethod
    def get_epg_url(cls):
        """
        Returns the EPG API URL

        :returns:  string -- EPG API URL
        """
        return EPG_URL

    @classmethod
    def get_stream_definition_url(cls):
        """
        Returns the stream defintion URL,
        used to get the final stream URL.
        It contains a `%VIDEO_ID%` placeholder,
        that needs to be replaced in order to
        fetch the streams

        :returns:  string -- EPG API URL
        """
        return STREAM_DEFINITON_URL

    @classmethod
    def get_sports_list(cls):
        """
        Returns the list of available sports

        :returns:  dict -- List of available sports
        """
        return SPORTS

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