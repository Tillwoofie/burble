# Written by Jeff Hickson (rvbcaboose@gmail.com).
# This file is part of burble, a plugin for Flinx. 

# Burble is free software, and comes with no warranty.
# It is licenced under the GNU GLP v3.
# The full terms of this are available in the LICENCE file,
# in the root of the project, at <http://www.gnu.org/licenses/>,
# or at <https://github.com/Tillwoofie/burble/blob/master/LICENSE>


def get_IDv1(f):
    '''
    Grabs the ID3v1, and attempts extended ID3v1 extraction.
    '''
    id3 = None
    id3e = None
    try:
        fin = open(f, "rb", 0)
        try:
            # len of basic tag is 128 bytes, extended is 227
            # seek relative to end by the sum of both tags.
            fin.seek(-(128+227), 2) 
            id3e = fin.read(227)
            id3 = fin.read(128)
            finally:
                fin.close()
            
            # do a basic check to see if we have tags
            if not id3[:3] == "TAG":
                id3 = None
            if not id3e[:4] == "TAG+":
                id3e = None
    except IOError:
        pass

    # do some processing with the tags we may have.
    if id3:
        tag3 = parse_id3v1(id3)
    else:
        tag3 = None

    if id3e:
        tag3e = parse_id3v1e(id3e)
    else:
        tag3e = None
    return (tag3, tag3e)


def parse_id3v1(data):
    '''
    Parse the ID3v1 tag format.
    '''
    info = {}
    info['title'] = striptag(data[3:33])
    info['artist'] = striptag(data[33:63])
    info['album'] = striptag(data[63:93])
    info['year'] = striptag(data[93:97])
    if data[125:126] == "\00":
        # track num present
        info['comment'] = striptag(data[97:125])
        info['track'] = ord([126:127])
    else:
        info['comment'] = striptag([97:127])
        info['track'] = None
    info['genre'] = ord(data[127:128])
    return info


def parse_id3v1e(data):
    '''
    Parse the extended ID3v1 tag format.
    '''
    info = {}
    info['title'] = striptag(data[4:64])
    info['artist'] = striptag(data[64:124])
    info['album'] = striptag(data[124:184])
    info['speed'] = ord(data[184:185])
    info['genre'] = striptag(data[185:215])
    info['start'] = striptag(data[215:221])
    info['end'] = striptag(data[221:227])
    return info


def striptag(data)
    return data.replace("\00", "").strip()
