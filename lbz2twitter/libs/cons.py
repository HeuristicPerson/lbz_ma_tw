"""
File with constant definitions and also a bit of code to read the constants from environment variables.
"""

import os


# Constants
#=======================================================================================================================
# Program name and version
u_PRG = 'ListenBrainz to Twitter'
u_VER = 'v1.0.2022-10-04.dev'

# Number of chars for fixed-width elements
i_WIDTH = 45

# Tuple with values than can be interpreted as a True
_tu_ON_VALUES = ('1', 'true', 'on', 'yes', 'y')

# Debug mode
_u_debug = os.getenv('DEBUG', 'False')
b_DEBUG = False
if _u_debug.lower() in _tu_ON_VALUES:
    b_DEBUG = True

# Language configuration, used in the creation of the tweet.
u_LOCALE = os.getenv('LOCALE', 'en_GB.UTF-8')


# ListenBrainz constants
#-----------------------
# ListenBrainz user to get most popular albums from
u_LB_USER = os.getenv('LB_USER', '')

# Number of albums to get from that user
i_LB_FETCH = int(os.getenv('LB_FETCH', '10'))

# Number of verified albums. When fetching most popular albums from ListBrainz website, some of them won't be verified
# e.g. they don't have any valid associated album ID in MusicBrainz website. So after getting all albums from,
# ListenBrainz, just the number below will be kept. Since at the moment I'm verifying my entire collection of music (and
# mostly listening to the recently updated material (so, VERIFIED), a ratio of 3:1 between FETCH albums, and KEPT albums
# seems reasonable
i_LB_VERIFIED = int(os.getenv('LB_VERIFIED', '3'))


# Cover download options
#-----------------------
# Number of retries when downloading materials from ListBrainz and MusicBrainz
i_DL_RETRIES = int(os.getenv('DL_RETRIES', '5'))

# Number of seconds between download retries
i_DL_DELAY = int(os.getenv('DL_DELAY', '5'))


# Twitter constants
#------------------
# The constants below are used to identify yourself in Twitter and being able to submit tweets. Check the page located
# at https://dev.twitter.com/apps (under "OAuth settings"). The access tokens can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "Your access token")
# # "Your access token")
u_TW_CONSUMER_KEY = os.getenv('TW_CONSUMER_KEY', '')
u_TW_CONSUMER_SECRET = os.getenv('TW_CONSUMER_SECRET', '')
u_TW_ACCESS_TOKEN = os.getenv('TW_ACCESS_TOKEN', '')
u_TW_ACCESS_TOKEN_SECRET = os.getenv('TW_ACCESS_TOKEN_SECRET', '')

# Number of retries when submitting a tweet
i_TW_RETRIES = int(os.getenv('TW_RETRIES', '5'))

# Number of seconds to wait between tweet retries
i_TW_DELAY = int(os.getenv('TW_DELAY', '5'))
