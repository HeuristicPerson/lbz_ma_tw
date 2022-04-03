"""
Library with classes to store MusicBrainz and ListenBrainz data.
"""

import musicbrainzngs
import pylistenbrainz

from . import cons


class Release:
    """
    Class to store data about releases (which are each of the multiple versions of a music album)
    """
    def __init__(self):
        self.i_listen_count = 0
        self.lu_artist_mbids = []  #
        self.u_artist_msid = ''
        self.u_artist_name = ''    # Release artist name # TODO: Check what's the value type when multiple artists are present
        self.u_release_mbid = ''   # MB release ID
        self.u_release_msid = ''
        self.u_release_name = ''
        self.lo_covers = []        # List of covers obtained from MusicBrainz website.

    def __str__(self):
        u_out = '<Release>\n'
        u_out += '  .i_listen_count:  %s\n' % self.i_listen_count
        u_out += '  .lu_artist_mbids: %s\n' % self.lu_artist_mbids
        u_out += '  .u_artist_msid:   %s\n' % self.u_artist_msid
        u_out += '  .u_artist_name:   %s\n' % self.u_artist_name
        u_out += '  .u_release_mbid:  %s\n' % self.u_release_mbid
        u_out += '  .u_release_msid:  %s\n' % self.u_release_msid
        u_out += '  .u_release_name:  %s\n' % self.u_release_name

        if not self.lo_covers:
            u_out += '  .lo_covers: []\n'
        else:
            u_covers = ''
            for o_cover in self.lo_covers:
                u_covers += str(o_cover)

            for i_line, u_line in enumerate(u_covers.splitlines()):
                if i_line == 0:
                    u_out += '  .lo_covers: %s\n' % u_line
                else:
                    u_out += '              %s\n' % u_line

        return u_out

    def from_lb_json(self, pdx_json):
        """
        Function to populate the object from a json data chunk obtained from ListenBrainz describing a release.

        :param pdx_json:
        :type pdx_json: Dict[Union[Str, Int, List[Str]]]

        :return: Nothing, the object will be populated
        """
        self.i_listen_count = pdx_json['listen_count']
        self.lu_artist_mbids = pdx_json['artist_mbids']
        self.u_artist_msid = pdx_json['artist_msid']
        self.u_artist_name = pdx_json['artist_name']
        self.u_release_mbid = pdx_json['release_mbid']
        self.u_release_msid = pdx_json['release_msid']
        self.u_release_name = pdx_json['release_name']

    def fetch_mb_covers(self):
        """
        Method to load the MusicBrainz covers.

        :return: Nothing, the covers will be stored in the object.
        """
        self.lo_covers = []

        if self.u_release_mbid:
            for i_try in range(cons.i_DL_RETRIES):
                try:
                    ldx_data = musicbrainzngs.get_image_list(self.u_release_mbid)['images']
                    for dx_data in ldx_data:
                        o_image = _Image()
                        o_image.from_dict_data(dx_data)
                        if o_image.b_front:
                            self.lo_covers.append(o_image)
                    break
                except musicbrainzngs.musicbrainz.ResponseError:
                    pass


class _Image:
    def __init__(self):
        self.b_approved = False  # Whether the image has been approved
        self.b_back = False      # Whether the image correspond to the back of the release
        self.u_comment = ''      # Comment of the image
        self.i_edit = 0          # Edit id
        self.b_front = False     # Whether the image coprrespond to the front of the release
        self.i_id = 0            # Id of the image
        self.u_image = ''        # URL of the image
        self.du_thumbnails = {}  # Dictionary with thumbnails of the image. The key correspond to some available sizes
                                 # among '1200', '250', '500', 'large', 'small'
        self.lu_types = []       # List containing some "tags" about the images. E.g. "Back" for a back image.

    def __str__(self):
        u_out = '<Image>\n'
        u_out += u'  .b_approved:    %s\n' % self.b_approved
        u_out += u'  .b_back:        %s\n' % self.b_back
        u_out += u'  .u_comment:     %s\n' % self.u_comment
        u_out += u'  .i_edit:        %s\n' % self.i_edit
        u_out += u'  .b_front:       %s\n' % self.b_front
        u_out += u'  .i_id:          %s\n' % self.i_id
        u_out += u'  .u_image:       %s\n' % self.u_image
        u_out += u'  .du_thumbnails: %s\n' % self.du_thumbnails
        u_out += u'  .lu_types:      %s\n' % self.lu_types
        return u_out

    def from_dict_data(self, pdx_data):
        """
        Method to populate the cover object from the dictionary data provided by musicbrainz library.

        :param pdx_data: Dictionary with data extracted from MusicBrainz using their library.
        :type pdx_data: Dict

        :return: Nothing
        """
        self.b_approved = pdx_data['approved']
        self.b_back = pdx_data['back']
        self.u_comment = pdx_data['comment']
        self.i_edit = pdx_data['edit']
        self.b_front = pdx_data['front']
        self.i_edit = pdx_data['edit']
        self.i_id = pdx_data['id']
        self.u_image = pdx_data['image']
        self.du_thumbnails = pdx_data['thumbnails']
        self.lu_types = pdx_data['types']


def get_lb_releases(pu_user, pi_count=25, pi_offset=0, pu_time_range='all_time'):
    """
    Function to get the latest releases for a user from ListenBrainz.

    :param pu_user: Name of ListenBrainz user to query
    :type pu_user: Str

    :param pi_count: Number of releases to get (they will be sorted from the most listened to the less listened.
    :type pi_count: Int

    :param pi_offset: Offset when querying the releases. e.g. if 0, the list will start from the first release (the most
                      listened), if 1, the first result will be the second most listened release.
    :type pi_offset: Int

    :param pu_time_range: String describing the time range of the query. Valid values are:
                            - 'all_time'
                            - 'month'
                            - 'this_month'
                            - 'week'
                            - 'year'
    :type pu_time_range: Str

    :return:
    :rtype List[lb_mb_data.Release]
    """

    client = pylistenbrainz.ListenBrainz()
    dx_data = client.get_user_releases(username=pu_user,
                                       count=pi_count,
                                       offset=pi_offset,
                                       time_range=pu_time_range)

    try:
        ldx_releases = dx_data['payload']['releases']
    except TypeError:
        ldx_releases = []

    lo_releases = []
    for dx_result in ldx_releases:
        o_release = Release()
        o_release.from_lb_json(dx_result)
        o_release.fetch_mb_covers()
        lo_releases.append(o_release)

    return lo_releases
