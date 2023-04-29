![](https://raw.githubusercontent.com/HeuristicPerson/pod_dl/v1.x.dev/images/logo-grey_and_green.png)

# ListenBrainz to Mastodon and Twitter

## >>> First the most important thing <<< ##

You can invite me to a **[☕ Ko-Fi](https://ko-fi.com/zipzop)**. It'll warm my
heart for at least 10 minutes... which is much more than nothing!

## Introduction

"ListenBrainz to Mastodon and Twitter" (or just **lbz_ma_tw**) is a small script
that reads the music listening statistics from a
[ListenBrainz](https://listenbrainz.org/) user and posts the three most popular
albums titles with their covers to twitter.

**IMPORTANT NOTE:** **lbz_ma_tw** tries to publish the top albums from **last
month** and ListenBrainz updates that information on 3rd day of each month. So,
the ListenBrainz account must have been working for some time before you're able
to successfully run **lbz_ma_tw**. For example, if you start using your
ListenBrainz account on 15th of month A, you need to wait until 4th of month A+1
to post your most popular albums from month A.


## Configuration
 
**#TODO:** Improve configuration documentation.

Apologies, no proper documentation has been written yet. It should be almost
straightforward for anybody with Docker containers background to download the
tool, figure out the available environment variables and their meaning.


### Environment variables

  * `UID` User ID of the user running the tool (1000 by default).
  * `GID` Group ID of the user running the tool (1000 by default).
  * `DEBUG` Whether debug options must be activated (1, "on", or "yes" to turn
    them on).
  * `LB_USER` Name of the ListenBrainz user to get most popular albums from.
  * `LB_FETCH` Number of most popular albums to fetch from ListenBrainz. e.g. if
    you want to display top 3 albums, it's a good idea to fetch at least three
    times that value, so you should put 9.
  * `LB_VERIFIED` Number of verified albums to display. This is the final number
    of albums in the top list to be displayed. But remember that only verified
    albums will be used.
  * `DL_RETRIES` (default 5) Number of retries when downloading album covers.
    Before posting the tweet with the top albums, covers must be downloaded.
  * `DL_DELAY` (default 5) Number of seconds between cover download retries.
  * `LOCALE` (default en_UK.UTF-8) Locale to be used when generating the tweet
    with the top albums.
  * `MA_INSTANCE` Mastodon instance URL.
  * `MA_TOKEN` Mastodon token to post the messages.
  * `TW_CONSUMER_KEY` Twitter consumer key to post the messages.
  * `TW_CONSUMER_SECRET` Twitter consumer secret to post the messages.
  * `TW_ACCESS_TOKEN` Twitter access token to post the messages.
  * `TW_ACCESS_TOKEN_SECRET` Twitter access token secret to post the messages.
  * `MSG_RETRIES` (default 5) Number of retries when submitting the messages.
  * `MSG_DELAY` (default 5) Number of seconds between tweet retries.
  * `MSG_HOUR` Hour (0-23) when top albums tweet should be submitted.
  * `TZ` (default "Europe/London") Timezone to be used as reference.


## Special Thanks

  * To [ListenBrainz](https://listenbrainz.org/) for providing the service to
    log user listening habits and derived statistics.
  * To [MusicBrainz](https://musicbrainz.org/) for providing the free and
    comprehensive music database that ListenBrainz relies on.
  * To MusicBrainz (yes, again) for [Picard](https://picard.musicbrainz.org/), a
    **marvelous** open source ID3 tagging tool to verify, validate and tag your
    audio files. In the particular context of **lbz2twitter**, it ensures that
    proper album is identified in ListenBrainz when playing a track. 
