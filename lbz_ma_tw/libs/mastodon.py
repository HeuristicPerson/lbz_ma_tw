"""
Library to send messages to mastodon.
"""
import mastodon
import urllib3


def toot(ps_text, pls_images='', pb_debug=False, ps_instance='', ps_token='', pi_retries=5, ):
    """
    Function to publish information in Mastodon.
    :param ps_text:
    :type ps_text: Str

    :param pls_images: List with the URL of images to be uploaded.
    :type pls_images: List[Str]

    :param pb_debug: Whether the function is working in debug mode or not. In debug mode, the toots won't be sent at
                     all.
    :type pb_debug: Bool

    :return: A boolean indicating whether the post was successful or not.
    :rtype: Bool
    """
    # [0/?] Initialization
    #---------------------
    b_published = False

    # [2/?] Actual tweet posting
    #---------------------------
    if pb_debug:
        b_published = True

    else:
        # [1/?] Authentication
        #----------------------
        #TODO: Replace mastodon server from with one read from environment variables
        o_mastodon = mastodon.Mastodon(access_token=ps_token, api_base_url=ps_instance)

        # [2/?] Uploading the image of the entry to mastodon
        #---------------------------------------------------
        ls_media_ids = []
        if pls_images:
            o_http_pool = urllib3.PoolManager()
            for s_image in pls_images:
                o_response = o_http_pool.request('GET', s_image)
                s_img_data = o_response.data
                #TODO: Guess the mime_type from the file extension. Create a function because it'll helpful for twitter also
                ds_media_meta = o_mastodon.media_post(media_file=s_img_data, mime_type='image/jpeg')
                s_media_id = ds_media_meta['id']
                ls_media_ids.append(s_media_id)

        # [3/?] Posting the message
        #--------------------------
        for i_retry in range(pi_retries):
            o_mastodon.status_post(ps_text, media_ids=ls_media_ids)
            b_published = True
            break
            #time.sleep(i_DELAY)

    return b_published
