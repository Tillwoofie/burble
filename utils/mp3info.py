# Written by Jeff Hickson (rvbcaboose@gmail.com).
# This file is part of burble, a plugin for Flinx. 

# Burble is free software, and comes with no warranty.
# It is licenced under the GNU GLP v3.
# The full terms of this are available in the LICENCE file,
# in the root of the project, at <http://www.gnu.org/licenses/>,
# or at <https://github.com/Tillwoofie/burble/blob/master/LICENSE>

import re

fid_pat = re.compile("^[0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z]$")

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
            
    except IOError:
        pass

    # do a basic check to see if we have tags
    if not id3[:3] == "TAG":
        id3 = None
    if not id3e[:4] == "TAG+":
        id3e = None

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
        info['track'] = ord(data[126:127])
    else:
        info['comment'] = striptag(data[97:127])
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


def get_IDv2(f):
    '''
    Gets the ID3v2 tags from a file. Supports minimally v2.3.
    '''
    v2meta = None
    v2tags = None
    try:
        fin = open(f, "rb", 0)
        try:
            # start by grabbing the meta info.
            # meta frame is 10 bytes long
            meta = fin.read(10)
            pmeta = parse_V2meta(meta)
            tags = None
            if pmeta is not None:
                # should be the entire length of the tags
                tags = parse_V2(fin.read(pmeta['size']))
        finally:
            fin.close()
    except IOError:
        pass
    return pmeta


def parse_V2(data, meta):
    '''
    Parse the v2 tags out of the provided data.
    '''
    if meta['extended']:
        # don't handle this right now.
        return None
    if meta['unsync'];
        #also don't support this yet.
        return None
    pos = 0
    while True:
        x = getv2Tag(data, pos)


def getv2Tag(data, pos):
    '''
    Gets the next tag from data, starting at pos.
    '''
    hdr = data[pos:pos+10]
    fid = hdr[0:4]
    rsize = hdr[4:8]
    size = ord(rsize[0]) + ord(rsize[1]) + ord(rsize[2]) + ord(rsize[3])
    rflags = hdr[8:10]
    if not validate_fid(fid):
        return (None, None) # This should change, not sure what to do now.
    # continue parsing tag
    npos = size + 10
    flags = dec_fflags(rflags)
    # we should parse additional information about the tags
    # any of these throw off parsing, sooo, do this later.
    if flags['COMP']:
        # had additional bytes after the header
        return (None, None)
    if flags['ENC']:
        # it is encrypted...
        return (None, None)
    if flags['GRP']
        # part of a group
        return (None, None)
    # if none of those, keep going...
    pass


def dec_fflags(flag_data):
    '''
    Decode the frame flags of a v2 tag.
    '''
    f = {}
    b1 = ord(flag_data[0])
    b2 = ord(flag_data[1])
    # these are about re-writing tags
    f['TAP'] = b1 & 127
    f['FAP'] = b1 & 64
    f['RO'] = b1 & 32
    # these specify additional info about this tag
    f['COMP'] = b2 & 127
    f['ENC'] = b2 & 64
    f['GRP'] = b2 & 32

    return f


def validate_fid(fid):
    if fid_pat.match(fid):
        return True
    else return False


def parse_V2meta(data):
    '''
    Grab the meta info from the tag.
    '''
    if not data[:3] == "ID3":
        # we didn't read an ID3v2 tag if this isn't true.
        return None
    meta = {}
    meta['major_version'] = ord(data[3:4])
    meta['minor_version'] = ord(data[4:5])
    meta['flags'] = ord(data[5:6])
    meta['size_bits'] = data[6:10]
    meta['unsync'] = bool(meta['flags'] & 127)
    meta['extended'] = bool(meta['flags'] & 64)
    meta['experimental'] = bool(meta['flags'] & 32)
    # the other bits should be zero... but not going to verify.
    s = meta['size_bits']
    s1 = ord(s[0:1]) & 126
    s2 = ord(s[1:2]) & 126
    s3 = ord(s[2:3]) & 126
    s4 = ord(s[3:4]) & 126
    meta['size'] = s1 + s2 + s3 + s4
    return meta


def test_printv1(v1tags):
    '''
    Prints the v1 tags for a test.
    '''
    pass


def test_printv2(v2tags):
    '''
    Prints the v2 tags for a test.
    '''
    # only print the meta for now.
    if v2tags is None:
        print "No Tags Found."
        return
    t = v2tags
    print "Version: {}.{}".format(t['major_version'], t['minor_version'])
    s = "Flags: unsync: {} extended: {} experimental: {}"
    print s.format(t['unsync'], t['extended'], t['experimental'])
    print "Size: {}".format(t['size'])


def striptag(data):
    return data.replace("\00", "").strip()
