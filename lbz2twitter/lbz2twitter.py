#!/usr/bin/env python3

import datetime
import dateutil.relativedelta
import locale
import os

import libs.lb_mb_data as lb_mb_data
import libs.cons as cons
import libs.download as download
import libs.twitter as twitter


# Functions
#=======================================================================================================================
def _filter_unverified_releases(plo_releases):
    """
    Function to remove unverified releases (releases without a proper MusicBrainz Id) from a list.
    :param plo_releases:
    :type plo_releases: List[libs.lb_mb_data.Release]

    :return:
    :rtype List[libs.lb_mb_data.Release]
    """
    lo_verified_releases = [o_release for o_release in plo_releases if o_release.u_release_mbid]
    return lo_verified_releases


def _build_tweet_text(plo_releases):
    """
    Function to build the text of the tweet with the top albums.

    :param plo_releases:
    :type plo_releases: List[Str]

    :return: The text with the top albums
    :rtype Str
    """
    u_msg = ''

    # Dictionary with heading and album line in different locales
    #------------------------------------------------------------
    du_heading = {
        'en_GB.UTF-8': 'Top %s albums in %s\n',
        'es_ES.UTF-8': 'Top %s discos de %s\n',
    }
    du_album_line = {
        'en_GB.UTF-8': '%s. %s (by %s)\n',
        'es_ES.UTF-8': '%s. %s (por %s)\n'
    }

    # Setting the locale and using en_GB.UTF-8 when the chosen option is not valid
    #-----------------------------------------------------------------------------
    if (cons.u_LOCALE in du_heading) and (cons.u_LOCALE in du_album_line):
        u_locale = cons.u_LOCALE
    else:
        print('WARNING: Locale "%s" not found, using "en_GB.UTF-8" instead' % cons.u_LOCALE)
        u_locale = 'en_GB.UTF-8'

    locale.setlocale(locale.LC_TIME, cons.u_LOCALE)

    if plo_releases:
        u_heading_tpl = du_heading[u_locale]
        u_album_tpl = du_album_line[u_locale]

        # Getting the name of the last month
        #-----------------------------------
        o_last_month = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)
        u_last_month = o_last_month.strftime('%B')

        # Building the heading message
        #-----------------------------
        u_msg += u_heading_tpl % (cons.i_LB_VERIFIED, u_last_month)

        for i_release, o_release in enumerate(plo_releases, start=1):
            u_msg += u_album_tpl % (i_release,
                                    o_release.u_release_name,
                                    o_release.u_artist_name)

    return u_msg.strip()


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
        u_msg += 'u_LOCALE:                 %s\n' % cons.u_LOCALE
        u_msg += '\n'
        u_msg += 'u_LB_USER:                %s\n' % cons.u_LB_USER
        u_msg += 'i_LB_FETCH:               %s\n' % cons.i_LB_FETCH
        u_msg += 'i_LB_VERIFIED:            %s\n' % cons.i_LB_VERIFIED
        u_msg += '\n'
        u_msg += 'u_TW_CONSUMER_KEY:        %s\n' % cons.u_TW_CONSUMER_KEY
        u_msg += 'u_TW_CONSUMER_SECRET:     %s\n' % cons.u_TW_CONSUMER_SECRET
        u_msg += 'u_TW_ACCESS_TOKEN:        %s\n' % cons.u_TW_ACCESS_TOKEN
        u_msg += 'u_TW_ACCESS_TOKEN_SECRET: %s\n' % cons.u_TW_ACCESS_TOKEN_SECRET
        u_msg += '~~~~~~~~~~~~~~~~~'
        print(u_msg)


# Main code
#=======================================================================================================================
if __name__ == '__main__':
    u_prg = '%s - %s' % (cons.u_PRG, cons.u_VER)
    u_msg = '%s\n%s' % (u_prg, '='*cons.i_WIDTH)
    print(u_msg)

    _print_debug_msg()

    # Getting a high enough number of albums, so later we can keep enough verified ones
    #----------------------------------------------------------------------------------
    u_msg = 'Fetching top %s releases from ListenBrainz...' % cons.i_LB_FETCH
    u_msg = u_msg.ljust(cons.i_WIDTH, '.')
    print(u_msg, end='')
    lo_releases = lb_mb_data.get_lb_releases(pu_user=cons.u_LB_USER,
                                             pi_count=cons.i_LB_FETCH,
                                             pi_offset=0,
                                             pu_time_range='month')
    print(' DONE!')

    # Filtering out unverified albums (totally wanted side effect: Podcasts won't be taken into account)
    #---------------------------------------------------------------------------------------------------
    u_msg = 'Filtering top %s verified releases...' % cons.i_LB_VERIFIED
    u_msg = u_msg.ljust(cons.i_WIDTH, '.')
    print(u_msg, end='')
    lo_releases = _filter_unverified_releases(lo_releases)[:cons.i_LB_VERIFIED]
    print(' DONE!')

    # Showing the text (only the text, not the covers) of the tweet about to be sent
    #-------------------------------------------------------------------------------
    print('-' * cons.i_WIDTH)
    u_tweet = _build_tweet_text(lo_releases)
    if u_tweet:
        u_msg = u_tweet
    else:
        u_msg = '(Sorry, empty list of albums, so empty tweet)'
    print(u_msg)
    print('-' * cons.i_WIDTH)

    # Sending the tweet
    #------------------
    u_msg = 'Sending tweet (%s characters)...' % len(u_tweet)
    u_msg = u_msg.ljust(cons.i_WIDTH, '.')
    print(u_msg, end='')
    if lo_releases:
        _tweet_releases(lo_releases)
        u_result = ' DONE!'
    else:
        u_result = ' SKIPPED!'
    print(u_result)
