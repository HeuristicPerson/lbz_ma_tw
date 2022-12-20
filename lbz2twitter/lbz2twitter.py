#!/usr/bin/env python3

import datetime
import dateutil.relativedelta
import locale
import os

# TODO: remove import and create my own exception in twitter.py library
import tweepy

import libs.lb_mb_data as lb_mb_data
import libs.cons as cons
import libs.download as download
import libs.twitter as twitter


# Functions
#=======================================================================================================================
def _filter_unverified_releases(plo_releases):
    """
    Function to remove unverified releases (releases without a proper MusicBrainz Id.) from a list.
    :param plo_releases:
    :type plo_releases: List[libs.lb_mb_data.Release]

    :return:
    :rtype: List[libs.lb_mb_data.Release]
    """
    lo_verified_releases = [o_release for o_release in plo_releases if o_release.u_release_mbid]
    return lo_verified_releases


def _filter_duplicated_releases(plo_releases):
    """
    Function to remove duplicated releases (same id) from a list of releases.

    :param plo_releases:
    :type plo_releases: List[libs.lb_mb_data.Release]

    :return:
    :rtype List[libs.lb_mb_data.Release]
    """
    # We need to keep the order, so mapping the objects to a dictionary where the unique key is the attribute we don't
    # want to have repeated is not an option. So I need to use "cheap" workaround.
    lu_used_keys = []
    lo_filtered_releases = []
    for o_release in plo_releases:
        if o_release.u_release_mbid not in lu_used_keys:
            lo_filtered_releases.append(o_release)
            lu_used_keys.append(o_release.u_release_mbid)

    return lo_filtered_releases


def _build_tweet_text(plo_releases, ps_interval='month'):
    """
    Function to build the text of the tweet with the top albums.

    :param plo_releases:
    :type plo_releases: List[Str]

    :return: The text with the top albums
    :rtype Str
    """
    s_msg = ''

    # Dictionary with heading and album line in different locales
    #------------------------------------------------------------
    ds_heading = {
        'en_GB.UTF-8': 'Top %s albums in %s\n',
        'es_ES.UTF-8': 'Top %s discos de %s\n',
    }
    ds_album_line = {
        'en_GB.UTF-8': '%s. %s (by %s)\n',
        'es_ES.UTF-8': '%s. %s (por %s)\n'
    }

    # Setting the locale and using en_GB.UTF-8 when the chosen option is not valid
    #-----------------------------------------------------------------------------
    if (cons.s_LOCALE in ds_heading) and (cons.s_LOCALE in ds_album_line):
        s_locale = cons.s_LOCALE
    else:
        print('WARNING: Locale "%s" not found, using "en_GB.UTF-8" instead' % cons.s_LOCALE)
        s_locale = 'en_GB.UTF-8'

    locale.setlocale(locale.LC_TIME, cons.s_LOCALE)

    if plo_releases:
        s_heading_tpl = ds_heading[s_locale]
        s_album_tpl = ds_album_line[s_locale]

        # Getting the name of the last time interval
        #-------------------------------------------
        if ps_interval == 'month':
            o_last_month = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)
            s_last_interval = o_last_month.strftime('%B')
        elif ps_interval == 'year':
            o_last_year = datetime.datetime.now() - dateutil.relativedelta.relativedelta(years=1)
            s_last_interval = o_last_year.strftime('%Y')
        else:
            raise ValueError('Invalid interval name, allowed values are "month", and "year"')

        # Building the heading message
        #-----------------------------
        s_msg += s_heading_tpl % (cons.i_LB_VERIFIED, s_last_interval)

        for i_release, o_release in enumerate(plo_releases, start=1):
            s_msg += s_album_tpl % (i_release,
                                    o_release.u_release_name,
                                    o_release.u_artist_name)

        # Adding an extra hashtag, so it's easier to track the entries
        #-------------------------------------------------------------
        s_msg += '\n#top_albums'

    return s_msg.strip()


def _tweet_releases(plo_releases):
    """
    Function to tweet the popular releases.
    :param plo_releases:
    :type plo_releases: List[lb_mb_data.Release]

    :return: True if the Tweet was sent, False otherwise
    :rtype Bool
    """

    # TODO: Find a way to indicate whether there were no releases found, so the empty tweet wasn't sent.
    b_tweet_sent = False

    if plo_releases:
        # Downloading the covers because tweepy can only post local files
        #----------------------------------------------------------------
        lu_cover_paths = []

        for i_release, o_release in enumerate(plo_releases, start=1):
            # Tweepy only allows posting local images, so we have to download the covers
            try:
                u_url = o_release.lo_covers[0].du_thumbnails['large']
                u_path = '/tmp/lb2twitter_cover_%s.jpg' % i_release
                download.dl_file(u_url, u_path)
                lu_cover_paths.append(u_path)

            except KeyError:
                pass

        u_msg = _build_tweet_text(plo_releases)
        b_tweet_sent = twitter.tweet(u_msg, plu_images=lu_cover_paths)

        # Deleting the files after sending the tweet
        for u_file in lu_cover_paths:
            os.remove(u_file)

    return b_tweet_sent


def _print_debug_msg():
    """
    Function to print debug information when needed.
    :return: Nothing
    """
    if cons.b_DEBUG:
        u_msg = 'DEBUG INFORMATION\n'
        u_msg += '~~~~~~~~~~~~~~~~~\n'
        u_msg += 'i_DL_RETRIES:             %s\n' % cons.i_DL_RETRIES
        u_msg += 'i_DL_DELAY:               %s\n' % cons.i_DL_DELAY
        u_msg += '\n'
        u_msg += 's_LOCALE:                 %s\n' % cons.s_LOCALE
        u_msg += '\n'
        u_msg += 's_LB_USER:                %s\n' % cons.s_LB_USER
        u_msg += 'i_LB_FETCH:               %s\n' % cons.i_LB_FETCH
        u_msg += 'i_LB_VERIFIED:            %s\n' % cons.i_LB_VERIFIED
        u_msg += '\n'
        u_msg += 's_TW_CONSUMER_KEY:        %s\n' % cons.s_TW_CONSUMER_KEY
        u_msg += 's_TW_CONSUMER_SECRET:     %s\n' % cons.s_TW_CONSUMER_SECRET
        u_msg += 's_TW_ACCESS_TOKEN:        %s\n' % cons.s_TW_ACCESS_TOKEN
        u_msg += 's_TW_ACCESS_TOKEN_SECRET: %s\n' % cons.s_TW_ACCESS_TOKEN_SECRET
        u_msg += '~~~~~~~~~~~~~~~~~'
        print(u_msg)


def _report(ps_period='month'):
    # Getting a high enough number of albums, so later we can keep enough verified ones
    #----------------------------------------------------------------------------------
    s_msg = 'Fetching top %s releases from ListenBrainz...' % cons.i_LB_FETCH
    s_msg = s_msg.ljust(cons.i_WIDTH, '.')
    print(s_msg, end='')
    lo_releases = lb_mb_data.get_lb_releases(pu_user=cons.s_LB_USER,
                                             pi_count=cons.i_LB_FETCH,
                                             pi_offset=0,
                                             pu_time_range=ps_period)
    print(' DONE!')

    # Filtering duplicated entries
    #-----------------------------
    # Somehow, listenbrainz sometimes points twice to the same release, so I filter out duplicated release URLs
    lo_releases = _filter_duplicated_releases(lo_releases)

    # Filtering out unverified albums (totally wanted side effect: Podcasts won't be taken into account)
    #---------------------------------------------------------------------------------------------------
    s_msg = 'Filtering top %s verified releases...' % cons.i_LB_VERIFIED
    s_msg = s_msg.ljust(cons.i_WIDTH, '.')
    print(s_msg, end='')
    lo_releases = _filter_unverified_releases(lo_releases)[:cons.i_LB_VERIFIED]
    print(' DONE!')

    # Showing the text (only the text, not the covers) of the tweet about to be sent
    # -------------------------------------------------------------------------------
    print('\nTweet:\n')
    s_tweet = _build_tweet_text(lo_releases)
    if s_tweet:
        s_msg = '\n'.join([f'  │ {s_line}' for s_line in s_tweet.splitlines(False)])
    else:
        s_msg = '(Sorry, empty list of albums, so empty tweet)'
    print(f'{s_msg}\n')

    # Sending the tweet
    # ------------------
    s_msg = 'Sending tweet (%s characters)...' % len(s_tweet)
    s_msg = s_msg.ljust(cons.i_WIDTH, '.')
    print(s_msg, end='')
    if lo_releases:
        try:
            _tweet_releases(lo_releases)
            u_result = ' DONE!'
        except tweepy.errors.BadRequest:
            u_result = ' ERROR! Wrong Twitter authentication keys.'
    else:
        u_result = ' SKIPPED!'
    print(u_result)


# Main code
#=======================================================================================================================
if __name__ == '__main__':
    s_prg = '%s - %s' % (cons.s_PRG, cons.s_VER)
    s_msg = '%s\n%s' % (s_prg, '=' * cons.i_WIDTH)
    print(s_msg)

    _print_debug_msg()

    print('\nLast month report\n%s' % ('-'*cons.i_WIDTH))
    _report(ps_period='month')

    # Only launch year report if we're in January
    if datetime.datetime.now().month == 0:
        print('\nLast year report\n%s' % ('-'*cons.i_WIDTH))
        _report(ps_period='year')
