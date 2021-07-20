# -*- coding: utf-8 -*-
# Module: ContentLoader
# Author: asciidisco
# Created on: 24.07.2017
# License: MIT https://goo.gl/WA1kby

"""Fetches and parses content from the Magenta Sport API & website"""

from __future__ import unicode_literals
from kodi_six.utils import py2_decode
from datetime import datetime
from json import loads
from re import search
from xml.etree.ElementTree import fromstring
import xbmcgui, xbmc
import xbmcplugin


class ContentLoader(object):
    """Fetches and parses content from the Magenta Sport API & website"""


    def __init__(self, cache, session, item_helper, dialogs, handle):
        """
        Injects instances & the plugin handle

        :param cache: Cache instance
        :type cache: resources.lib.Cache
        :param session: Session instance
        :type session: resources.lib.Session
        :param item_helper: ItemHelper instance
        :type item_helper: resources.lib.ItemHelper
        :param handle: Kodis plugin handle
        :type handle: int
        """
        self.constants = session.constants
        self.utils = session.utils
        self.cache = cache
        self.session = session
        self.item_helper = item_helper
        self.dialogs = dialogs
        self.plugin_handle = handle
        addon = self.utils.get_addon()


    def get_epg(self, sport):
        """
        Loads EPG either from cache or starts fetching it

        :param sport: Cache instance
        :type sport: resources.lib.Cache
        :returns:  dict - Parsed EPG
        """
        _session = self.session.get_session()
        # check for cached epg data
        cached_epg = self.cache.get_cached_item('epg{0}'.format(sport))
        if cached_epg is not None:
            return cached_epg
        return self.load_epg(sport=sport, _session=_session)


    def load_epg(self, sport, _session):
        """
        Fetches EPG & appends it to the cache

        :param sport: Chosen sport
        :type sport: string
        :param _session: Requests session instance
        :type _session: requests.session
        :returns:  dict - EPG
        """
        epg = self.fetch_epg(sport=sport, _session=_session)
        if epg.get('status') == 'success':
            page_tree = self.parse_epg(epg=epg)
            self.cache.add_cached_item('epg{0}'.format(sport), page_tree)
        return page_tree


    def parse_epg(self, epg):
        """
        Parses the raw EPG

        :param epg: Raw epg
        :type epg: dict
        :returns:  dict - Parsed EPG
        """
        page_tree = {}
        data = epg.get('data', {})
        elements = data.get('elements') or data.get('data')
        use_slots = self.__use_slots(data=data)
        # iterate over every match in the epg
        for element in elements:
            # get details & metadata for the current event
            metadata = element.get('metadata', {})
            details = metadata.get('details', {})
            # get matchtime
            match_date, match_time, match_weekday = self.item_helper.datetime_from_utc(
                metadata=metadata,
                element=element)
            # check if we have already matches scheduled for that date
            if page_tree.get(match_date) is None:
                page_tree[match_date] = []

            matches = self.__parse_epg_element(
                use_slots=use_slots,
                element=element,
                details=details,
                match_time=match_time)

            for match in matches:
                page_tree.get(match_date).append(match)

            return page_tree


    def fetch_epg(self, sport, _session):
        """
        Builds the EPG URL & fetches the EPG

        :param sport: Chosen sport
        :type sport: string
        :param _session: Requests session instance
        :type _session: requests.session
        :returns:  dict - Parsed EPG
        """
        url = '{0}{1}'.format(self.utils.get_api_url(), self.constants.get_sports_additional_infos().get(sport, {}).get('epg', ''))
        url = self.utils.build_api_url(url)
        return loads(_session.get(url).text)


    def get_stream_urls(self, video_id):
        """
        Fetches the stream urls document & parses them as well

        :param video_id: Id of the video to fetch stream urls for
        :type video_id: string
        :returns:  dict - Stream urls
        """
        stream_urls = {}
        _session = self.session.get_session()
        stream_access = loads(_session.post(
            self.constants.get_stream_definition_url().replace(
                '%VIDEO_ID%',
                str(video_id))
            ).text)
        if stream_access.get('status') == 'success':
            stream_urls['Live'] = 'https:{0}'.format(stream_access.get('data', {}).get('stream-access', [None, None])[1])
        elif stream_access.get('status') == 'error':
            self.dialogs.show_ok_dialog(stream_access.get('message'))
        return stream_urls


    def get_m3u_url(self, stream_url):
        """
        Fetches the m3u description XML, parses the attributes & builds
        the m3u url

        :param stream_url: Url to fetch the m3u description XML from
        :type stream_url: string
        :returns:  string - m3u url
        """
        m3u_url = ''
        _session = self.session.get_session()
        xml_content = _session.get(stream_url)
        root = fromstring(xml_content.text)
        for child in root:
            m3u_url = '{0}?hdnea={1}'.format(child.attrib.get('url', ''), child.attrib.get('auth', ''))
        return m3u_url


    def show_sport_selection(self):
        """Creates the KODI list items for the sport selection"""
        self.utils.log('Sport selection')
        _session = self.session.get_session()
        url = '{0}{1}'.format(self.utils.get_api_url(), self.constants.get_api_navigation_path())
        url = self.utils.build_api_url(url)
        nav_data = loads(_session.get(url).text)

        # get live matches
        url = '{0}{1}'.format(self.utils.get_api_url(), nav_data.get('data').get('header')[0].get('target'))
        url = self.utils.build_api_url(url)
        live_data = loads(_session.get(url).text)
        for content in live_data.get('data').get('content'):
            for group_element in content.get('group_elements'):
                if group_element.get('type') == 'programm':
                    live_counter = 0
                    for data in group_element.get('data'):
                        for slot in data.get('slots'):
                            if slot.get('is_live'):
                                live_counter += 1
                    group_element.update(dict(data=None))
                    url = self.utils.build_url({'for': group_element, 'lane': group_element.get('data_url')})
                    list_item = xbmcgui.ListItem(label='[B]Live ({0})[/B]'.format(live_counter))
                    list_item.setArt({'thumb': '{0}{1}'.format(self.constants.get_base_url(), live_data.get('data').get('metadata').get('web').get('image').replace(' ', '%20'))})
                    xbmcplugin.addDirectoryItem(
                        handle=self.plugin_handle,
                        url=url,
                        listitem=list_item,
                        isFolder=True)

        sports = nav_data.get('data').get('league_filter')
        for sport in sports:
            url = self.utils.build_url({'for': sport})
            label = py2_decode(self.constants.get_sports_additional_infos().get(sport.get('id'), {}).get('prefix', '{0}')).format(sport.get('title'))
            list_item = xbmcgui.ListItem(label=label)
            list_item = self.item_helper.set_art(
                list_item=list_item,
                sport=sport)
            xbmcplugin.addDirectoryItem(
                handle=self.plugin_handle,
                url=url,
                listitem=list_item,
                isFolder=True)
        xbmcplugin.addSortMethod(
            handle=self.plugin_handle,
            sortMethod=xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(self.plugin_handle)


    def show_sport_categories(self, sport):
        """
        Creates the KODI list items for the contents of a sport selection.
        It loads the sport html page & parses the event lanes given

        :param sport: Chosen sport
        :type sport: string
        """
        self.utils.log('({0}) Main Menu'.format(sport))
        _session = self.session.get_session()

        # load sport page from Magenta Sport
        url = '{0}{1}'.format(self.utils.get_api_url(), sport.get('target'))
        url = self.utils.build_api_url(url)
        raw_data = _session.get(url).text

        # parse data
        data = loads(raw_data)
        data = data.get('data', dict())

        lanes = list()
        content = data.get('content', list())
        if content:
            for lane in content:
                if lane.get('group_elements', list()):
                    lane_type = lane.get('group_elements')[0].get('type').lower()
                    if lane_type.find('lane') > -1:
                        lanes.append(lane)
                    elif lane_type == 'teasergrid':
                        url = self.utils.build_url({'for': sport, 'lane': '/epg/content/{0}'.format(lane.get('group_elements')[0].get('content_id'))})
                        title = 'Programm'
                        list_item = xbmcgui.ListItem(label=title)
                        list_item = self.item_helper.set_art(
                            list_item=list_item,
                            sport=sport)
                        xbmcplugin.addDirectoryItem(
                            handle=self.plugin_handle,
                            url=url,
                            listitem=list_item,
                            isFolder=True)

        # add directory item for each event
        for lane in lanes:
            url = self.utils.build_url({'for': sport, 'lane': lane.get('group_elements')[0].get('data_url')})
            title = lane.get('title') if lane.get('title') and lane.get('title') != '' else lane.get('group_elements')[0].get('title')
            list_item = xbmcgui.ListItem(label=title)
            list_item = self.item_helper.set_art(
                list_item=list_item,
                sport=sport)
            xbmcplugin.addDirectoryItem(
                handle=self.plugin_handle,
                url=url,
                listitem=list_item,
                isFolder=True)

        # Add static folder items (if available)
        # self.__add_static_folders()
        # xbmcplugin.addSortMethod(
        #    handle=self.plugin_handle,
        #    sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.endOfDirectory(self.plugin_handle)


    def show_date_list(self, _for):
        """
        Creates the KODI list items for a list of dates with contents
        based on the current date & syndication.

        :param _for: Chosen sport
        :type _for: string
        """
        self.utils.log('Main menu')
        plugin_handle = self.plugin_handle
        addon_data = self.utils.get_addon_data()
        epg = self.get_epg(_for)
        for _date in epg.keys():
            title = ''
            items = epg.get(_date)
            for item in items:
                title = '{0}{1}\n\n'.format(title, ' '.join(item.get('title').replace('Uhr', '').split(' ')[:-2]))
            url = self.utils.build_url({'date': date, 'for': _for})
            list_item = xbmcgui.ListItem(label=_date)
            list_item.setProperty('fanart_image', addon_data.get('fanart'))
            list_item.setInfo('video', {
                'date': date,
                'title': title,
                'plot': title,
            })
            xbmcplugin.addDirectoryItem(
                handle=plugin_handle,
                url=url,
                listitem=list_item,
                isFolder=True)
            xbmcplugin.addSortMethod(
                handle=plugin_handle,
                sortMethod=xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(plugin_handle)


    def show_event_lane(self, sport, lane):
        """
        Creates the KODI list items with the contents of an event-lanes
        for a selected sport & lane

        :param sport: Chosen sport
        :type sport: string
        :param lane: Chosen event-lane
        :type lane: string
        """
        _session = self.session.get_session()
        plugin_handle = self.plugin_handle

        # load sport page from Magenta Sport
        url = '{0}{1}'.format(self.utils.get_api_url(), lane)
        url = self.utils.build_api_url(url)
        raw_data = _session.get(url).text

        # parse data
        data_json = loads(raw_data)
        datalist = [data_json.get('data', dict())]

        if self.utils.get_addon().getSetting('show_program_fcbayerntv') == 'true':
            url = self.utils.build_api_url(url, query=dict(page=1, eventTreeId=1577))
            raw_data = _session.get(url).text
            data_json = loads(raw_data)
            datalist.append(data_json.get('data', dict()))

        # generate entries
        events = list()
        if datalist:
            for data in datalist:
                if data.get('data'):
                    for item in data.get('data'):
                        if item.get('slots'):
                            for slot in item.get('slots'):
                                for event in slot.get('events'):
                                    events.append(event)
                        else:
                            self.add_event_lane_item(sport, lane , item)
                elif data.get('content'):
                    for content in data.get('content'):
                        for group_element in content.get('group_elements'):
                            for group_element_data in group_element.get('data'):
                                for slot in group_element_data.get('slots'):
                                    for event in slot.get('events'):
                                        events.append(event)
                elif data.get('elements'):
                    for element in data.get('elements'):
                        for slot in element.get('slots'):
                            for event in slot.get('events'):
                                events.append(event)

        if events:
            events = sorted(events, key=lambda k: k.get('metadata').get('scheduled_start').get('utc_timestamp'))
            now = datetime.now()
            eventday = None;
            mt = None
            added_events_url = list()
            for event in events:
                if event.get('metadata').get('state') != 'post' and event.get('metadata').get('scheduled_start').get('utc_timestamp') and event.get('target') not in added_events_url:
                    sdt = datetime.fromtimestamp(float(event.get('metadata').get('scheduled_start').get('utc_timestamp')))
                    mt = self.item_helper.datetime_from_utc(event.get('metadata'), event)
                    if eventday is None or eventday < sdt.date():
                        eventday = sdt.date()
                        list_item = xbmcgui.ListItem('[COLOR gold]{0}, {1}[/COLOR]'.format(mt[2], mt[0]))
                        list_item.setArt(dict(thumb='DefaultYear.png'))
                        xbmcplugin.addDirectoryItem(
                            handle=plugin_handle,
                            url=None,
                            listitem=list_item,
                            isFolder=False)

                    self.add_event_lane_item(sport, lane, event, mt, isFolder=not (event.get('metadata').get('state') == 'pre' and sdt > now))
                    mt = None
                    added_events_url.append(event.get('target'))

        xbmcplugin.endOfDirectory(plugin_handle)


    def add_event_lane_item(self, sport, lane, _for, match_time=None, isFolder=True):
        """
        Adds a KODI list items with the contents of an event-lanes
        for a selected sport & lane

        :param sport: Chosen sport
        :type sport: string
        :param lane: Chosen event-lane
        :type lane: string
        :param _for: Item that will be added
        :type lane: string
        :param match_time: Match time of the item
        :type lane: string
        :param isFolder: Whether the item is a folder
        :type lane: bool
        """
        url = self.utils.build_url({'for': _for, 'lane': lane, 'target': _for.get('target'), 'sport': sport})
        label = self.item_helper.build_title(_for)
        if match_time:
            label = '[COLOR red]{0}[/COLOR] {1} [COLOR blue]{2}[/COLOR]'.format(match_time[1], label, self.item_helper.build_description(_for, show_title=False))
        list_item = xbmcgui.ListItem(label=label)
        list_item = self.item_helper.set_art(list_item, sport, _for)
        info = dict(plot=self.item_helper.build_description(_for))
        list_item.setInfo('video', info)

        xbmcplugin.addDirectoryItem(
            handle=self.plugin_handle,
            url=url,
            listitem=list_item,
            isFolder=isFolder)


    def show_matches_list(self, game_date, _for):
        """
        Creates the KODI list items with the contents of available matches
        for a given date

        :param game_date: Chosen event-lane
        :type game_date: string
        :param _for: Chosen sport
        :type _for: string
        """
        self.utils.log('Matches list: {0}'.format(_for))
        addon_data = self.utils.get_addon_data()
        plugin_handle = self.plugin_handle
        epg = self.get_epg(_for)
        items = epg.get(game_date)
        for item in items:
            url = self.utils.build_url(
                {'hash': item.get('hash'), 'date': game_date, 'for': _for})
            list_item = xbmcgui.ListItem(label=item.get('title'))
            list_item.setProperty('fanart_image', addon_data.get('fanart'))
            xbmcplugin.addDirectoryItem(
                handle=plugin_handle,
                url=url,
                listitem=list_item,
                isFolder=True)
            xbmcplugin.addSortMethod(
                handle=plugin_handle,
                sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(plugin_handle)


    def show_match_details(self, target, lane, _for, sport):
        """
        Creates the KODI list items with the contents of a matche
        (Gamereport, Interviews, Rematch, etc.)

        :param target: Chosen match
        :type target: string
        :param lane: Chosen event-lane
        :type lane: string
        :param _for: Chosen item
        :type _for: string
        :param sport: Chosen sport
        :type sport: string
        """
        self.utils.log('Matches details')

        # check if content is available
        if _for.get('metadata').get('state') == 'pre' and _for.get('metadata', {}).get('scheduled_start', {}).get('utc_timestamp'):
            sdt = datetime.fromtimestamp(float(_for.get('metadata', {}).get('scheduled_start', {}).get('utc_timestamp')))
            if sdt > datetime.now():
                self.dialogs.show_not_available_dialog()
                return None

        _session = self.session.get_session()

        # load sport page from Magenta Sport
        url = '{0}{1}'.format(self.utils.get_api_url(), target)
        url = self.utils.build_api_url(url)
        raw_data = _session.get(url).text

        # parse data
        data = loads(raw_data)
        data = data.get('data', dict())

        # check if content is available
        if data.get('content') is None:
            xbmcplugin.endOfDirectory(self.plugin_handle)
            return None

        added_vids = list()
        for videos in data.get('content', []):
            vids = videos.get('group_elements', [{}])[0].get('data')
            for video in vids:
                if self.__is_playable_video_item(video=video) \
                        and self.__add_video_item(video=video, video_types=_for.get('metadata').get('video_types')) \
                        and video.get('videoID') not in added_vids:
                    added_vids.append(video.get('videoID'))
                    title = video.get('title', '')
                    list_item = xbmcgui.ListItem(
                        label=title)
                    list_item = self.item_helper.set_art(
                        list_item=list_item,
                        sport=sport,
                        item=video)
                    list_item = self.__set_item_playable(
                        list_item=list_item,
                        title=title)
                    url = self.utils.build_url({
                        'for': sport,
                        'lane': lane,
                        'target': target,
                        'video_id': str(video.get('videoID'))})
                    xbmcplugin.addDirectoryItem(
                        handle=self.plugin_handle,
                        url=url,
                        listitem=list_item,
                        isFolder=False)
        xbmcplugin.endOfDirectory(handle=self.plugin_handle)


    def play(self, video_id):
        """
        Plays a video by Video ID

        :param target: Video ID
        :type target: string
        """
        self.utils.log('Play video: {0}'.format(video_id))
        streams = self.get_stream_urls(video_id)
        for stream in streams:
            play_item = xbmcgui.ListItem(
                path=self.get_m3u_url(streams.get(stream)))

            import inputstreamhelper
            is_helper = inputstreamhelper.Helper('hls')
            if is_helper.check_inputstream():
                # pylint: disable=E1101
                play_item.setContentLookup(False)
                play_item.setMimeType('application/vnd.apple.mpegurl')
                play_item.setProperty('inputstream.adaptive.stream_headers',
                    'user-agent={0}'.format(self.utils.get_user_agent()))
                play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
                play_item.setProperty('inputstreamaddon' if self.utils.get_kodi_version() == 18 else 'inputstream', 'inputstream.adaptive')
            return xbmcplugin.setResolvedUrl(
                self.plugin_handle,
                True,
                play_item)
        return xbmcplugin.setResolvedUrl(
                self.plugin_handle,
                False,
                xbmcgui.ListItem())


    def __parse_regular_event(self, target_url, details, match_time):
        """
        Parses a regular event (one that´s not part of a slot)

        :param target_url: Events target url
        :type target_url: string
        :param details: Events details
        :type details: dict
        :param match_time: Events match time
        :type match_time: string
        :returns:  dict - Parsed event
        """
        return self.item_helper.build_page_leave(
            target_url=target_url,
            details=details,
            match_time=match_time)


    def __parse_slot_events(self, element, details, match_time):
        """
        Parses an event

        :param element: Raw element info
        :type element: dict
        :param details: Events details
        :type details: dict
        :param match_time: Events match time
        :type match_time: string
        :returns:  dict - Parsed event
        """
        events = []
        slots = element.get('slots')
        # get data for home and away teams
        home = details.get('home', {})
        away = details.get('away', {})
        for slot in slots:
            events = slot.get('events')
            for event in events:
                target_url = event.get('target_url', '')
                if details.get('home') is not None:
                    shorts = (
                        home.get('name_mini'),
                        away.get('name_mini'))
                    events.append(
                        self.item_helper.build_page_leave(
                            target_url=target_url,
                            details=details,
                            match_time=match_time,
                            shorts=shorts))
        return events


    def __add_static_folders(self, statics, sport):
        """
        Adds static folder items to Kodi (if available)

        :param statics: All static entries
        :type statics: dict
        :param sport: Chosen sport
        :type sport: string
        """
        if statics.get(sport):
            static_lanes = statics.get(sport)
            if static_lanes.get('categories'):
                lanes = static_lanes.get('categories')
                for lane in lanes:
                    url = self.utils.build_url({
                        'for': sport,
                        'static': True,
                        'lane': lane.get('id')})
                    list_item = xbmcgui.ListItem(label=lane.get('name'))
                    xbmcplugin.addDirectoryItem(
                        handle=self.plugin_handle,
                        url=url,
                        listitem=list_item,
                        isFolder=True)


    def __add_video_item(self, video, video_types):
        """
        Determines if a playable video item should be added to Kodi

        :param video: Video details
        :type video: dict
        :param video_types: Type of the video
        :type video_types: list
        :returns:  bool - Video should be added
        """
        if video.get('islivestream', True) is True or ('Magazin' in video_types):
            return True


    def __parse_epg_element(self, use_slots, element, details, match_time):
        """
        Parses an EPG element & returns a list of parsed elements

        :param use_slots: Slot item
        :type use_slots: bool
        :param element: Raw EPG element
        :type element: dict
        :param details: EPG element details
        :type details: dict
        :param match_time: Events match time
        :type match_time: string
        :returns:  list - EPG element list
        """
        elements = []

        # determine event type & parse
        if use_slots is True:
            slot_events = self.__parse_slot_events(
                element=element,
                details=details,
                match_time=match_time)
            for slot_event in slot_events:
                elements.append(slot_event)
        else:
            target_url = element.get('target_url', '')
            slot = self.__parse_regular_event(
                target_url=target_url,
                details=details,
                match_time=match_time)
            elements.append(slot)
        return elements


    @classmethod
    def get_player_ids(cls, src):
        """
        Parses the player id HTML & returns stream & customer ids

        :param src: Raw HTML
        :type src: string
        :returns:  tuple - Stream & customer id
        """
        stream_id_raw = search('stream-id=.*', src)
        if stream_id_raw is None:
            return (None, None)
        stream_id = search('stream-id=.*', src).group(0).split('"')[1]
        customer_id = search('customer-id=.*', src).group(0).split('"')[1]
        return (stream_id, customer_id)


    @classmethod
    def __set_item_playable(cls, list_item, title):
        """
        Sets an Kodi item playable

        :param list_item: Kodi list item
        :type list_item: xbmcgui.ListItem
        :param title: Title of the video
        :type title: string
        :returns:  bool - EPG has slot type elements
        """
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {
            'title': title,
            'genre': 'Sports'})
        return list_item


    @classmethod
    def __use_slots(cls, data):
        """
        Determines if the EPG uses slot type events

        :param data: Raw EPG data
        :type data: dict
        :returns:  bool - EPG has slot type elements
        """
        if data.get('elements') is None:
            return False
        return True


    @classmethod
    def __is_playable_video_item(cls, video):
        """
        Determines if the item is playable

        :param video: Raw video data
        :type data: dict
        :returns:  bool - Video is playable
        """
        if isinstance(video, dict):
            if 'videoID' in video.keys():
                return True
        return False
