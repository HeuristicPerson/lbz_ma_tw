# Listenbrainz To Twitter (lbz2twitter)

"Listenbrainz to Twitter" (or just **lbz2twitter**) is a small script that reads
the music listening statistics from a [ListenBrainz](https://listenbrainz.org/)
user and posts the three most popular albums titles with their covers to
twitter.

**IMPORTANT NOTE:** **lbz2twitter** tries to publish the top albums from **last
month** and ListenBrainz updates that information on 3rd day of each month. So,
the ListenBrainz account must have been working for some time before you're able
to successfully run **lbz2twitter**. For example, if you start using your
ListenBrainz account on 15th of month A, you need to wait until 4th of month A+1
to post your most popular albums from month A.


# Configuration
 
**#TODO:** Write configuration documentation.
**#TODO:** Automate the creation and publishing of a Docker image (in DockerHub)
using GitHub automations.

Apologies, no proper documentation has been written yet. It should be almost
straightforward for anybody with Docker containers background to download the
tool, figure out the available environment variables and their meaning.


# Special Thanks

  * To [ListenBrainz](https://listenbrainz.org/) for providing the service to
    log user listening habits and derived statistics.
  * To [MusicBrainz](https://musicbrainz.org/) for providing the free and
    comprehensive music database that ListenBrainz relies on.
  * To MusicBrainz (yes, again) for [Picard](https://picard.musicbrainz.org/), a
    **marvelous** open source ID3 tagging tool to verify, validate and tag your
    audio files. In the particular context of **lbz2twitter**, it ensures that
    proper album is identified in ListenBrainz when playing a track.