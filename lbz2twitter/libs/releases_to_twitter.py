"""
Library with functions to build tweets with information about releases listened.
"""
import datetime
import locale

import dateutil.relativedelta

from . import cons


def build_tweet_text(plo_releases, ps_period='month'):
    """
    Function to build a tweet about listened releases; it'll automatically try to reduce the length of the tweet so it
    fits into the maximum allowed spaced of 280 characters.
    """
    for s_format in ('normal', 'short', 'shorter'):
        s_tweet_candidate = _build_tweet_text(plo_releases=plo_releases, ps_period=ps_period, ps_format=s_format)
        if len(s_tweet_candidate) <= 280:
            s_tweet = s_tweet_candidate
            break

    else:
        s_tweet = _build_tweet_text(plo_releases=plo_releases, ps_period=ps_period, ps_format='shorter')[:280]

    return s_tweet


def _build_tweet_text(plo_releases, ps_period='month', ps_format='normal'):
    """
    Function to build the text of the tweet with the top albums.

    :param plo_releases:
    :type plo_releases: List[Str]

    :param ps_format: Format of the tweet. Allowed values are 'normal', 'short', 'shorter'. Twitter only accepts 256
                     characters, so we'll try to fit all the information in them.
    :type ps_format: Str

    :return: The text with the top albums
    :rtype Str
    """
    s_msg = ''

    # Dictionary with heading and album line in different locales
    #------------------------------------------------------------
    dds_heading = {'normal': {'en_GB.UTF-8': '#TopAlbums in %s\n',
                              'es_ES.UTF-8': '#TopDiscos de %s\n'},
                   'short': {'en_GB.UTF-8': '#TopAlbums in %s\n',
                             'es_ES.UTF-8': '#TopDiscos de %s\n'},
                   'shorter': {'en_GB.UTF-8': '#TopAlbums in %s\n',
                               'es_ES.UTF-8': '#TopDiscos de %s\n'}
                   }
    dds_album_line = {'normal': {'en_GB.UTF-8': '%s. %s (by %s)\n',
                                 'es_ES.UTF-8': '%s. %s (por %s)\n'},
                      'short': {'en_GB.UTF-8': '%s %s (by %s)\n',
                                'es_ES.UTF-8': '%s %s (por %s)\n'},
                      'shorter': {'en_GB.UTF-8': '%s %s (%s)\n',
                                  'es_ES.UTF-8': '%s %s (%s)\n'}
                      }

    # Setting the locale and using en_GB.UTF-8 when the chosen option is not valid
    #-----------------------------------------------------------------------------
    if (cons.s_LOCALE in dds_heading[ps_format]) and (cons.s_LOCALE in dds_album_line[ps_format]):
        s_locale = cons.s_LOCALE
    else:
        print('WARNING: Locale "%s" not found, using "en_GB.UTF-8" instead' % cons.s_LOCALE)
        s_locale = 'en_GB.UTF-8'

    locale.setlocale(locale.LC_TIME, cons.s_LOCALE)

    if plo_releases:
        s_heading_tpl = dds_heading[ps_format][s_locale]
        s_album_tpl = dds_album_line[ps_format][s_locale]

        # Getting the name of the last time interval
        #-------------------------------------------
        if ps_period == 'month':
            o_last_month = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)
            s_last_interval = o_last_month.strftime('%B')
        elif ps_period == 'year':
            o_last_year = datetime.datetime.now() - dateutil.relativedelta.relativedelta(years=1)
            s_last_interval = o_last_year.strftime('%Y')
        else:
            raise ValueError('Invalid interval name, allowed values are "month", and "year"')

        # Building the heading message
        #-----------------------------
        try:
            s_msg += s_heading_tpl % (cons.i_LB_VERIFIED, s_last_interval)
        except TypeError:
            s_msg += s_heading_tpl % s_last_interval

        for i_release, o_release in enumerate(plo_releases, start=1):
            s_msg += s_album_tpl % (i_release,
                                    o_release.u_release_name,
                                    o_release.u_artist_name)

    return s_msg.strip()
