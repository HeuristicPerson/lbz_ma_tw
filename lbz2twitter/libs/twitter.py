"""
Library to submit messages to twitter.
"""

import time

import tweepy

from . import cons


def tweet(pu_text, plu_images=[]):
    """

    :param pu_text:

    :param plu_images: List of images to be attached to the post
    :type plu_images: List[Str[

    :return:
    """
    # [0/?] Initialization
    #---------------------
    b_tweeted = False

    # [2/?] Actual tweet posting
    #---------------------------
    if cons.b_DEBUG:
        b_tweeted = True

    else:
        # [1/?] Authentication
        #---------------------
        o_auth = tweepy.OAuthHandler(cons.s_TW_CONSUMER_KEY, cons.s_TW_CONSUMER_SECRET)
        o_auth.set_access_token(cons.s_TW_ACCESS_TOKEN, cons.s_TW_ACCESS_TOKEN_SECRET)
        o_twitter_account = tweepy.API(o_auth)

        if plu_images:
            for i_retry in range(cons.i_TW_RETRIES):
                try:
                    li_media_ids = []
                    for u_file in plu_images:
                        o_media_file = o_twitter_account.media_upload(filename=u_file)
                        li_media_ids.append(o_media_file.media_id)
                    o_twitter_account.update_status(status=pu_text, media_ids=li_media_ids)
                    b_tweeted = True
                    break
                except tweepy.errors.TwitterServerError:
                    time.sleep(cons.i_TW_DELAY)
                #except tweepy.errors.BadRequest:
                #    print('ERROR! Wrong Twitter authentication keys.')
                #    quit()

        else:
            for i_retry in range(cons.i_TW_RETRIES):
                try:
                    o_twitter_account.update_status(status=pu_text)
                    b_tweeted = True
                    break
                except tweepy.errors.TwitterServerError:
                    time.sleep(cons.i_TW_DELAY)

    return b_tweeted
