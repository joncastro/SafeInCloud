"""Desafe for Safe In Cloud (safe-in-cloud.com).
A python utility to decrypt Safe In Cloud databases files

Usage:
  desafe card <file> [<filter>...] [-p] [-r] [-d]
  desafe label <file>
  desafe export <file> (json|xml) [<output-file>]
  desafe (-h | --help)

self.args:
  card    Print cards
  label   Print labels
  export  Exports given file in clear in the given format (json or xml).
  file    Safe in Cloud database file path
  filter  optional words to filter entries

Options:
  -p --password     Print passwords.
  -r --raw          Print information keeping the original format.
  -d --deleted      Included deleted items.
  -h --help         Show this screen.
  -v --version      Show version.
"""

import struct
import sys
import getpass
import StringIO
import xmltodict
import zlib
import json
from docopt import docopt
from Crypto.Cipher import AES
from passlib.utils import pbkdf2


class Desafe:

    def __init__(self, desafe_filename, password):
        self.desafe_filename = desafe_filename
        self.password = password

    def __get_byte(self, f):
        return struct.unpack('B', f.read(1))[0]

    def __get_short(self, f):
        return struct.unpack('H', f.read(2))[0]

    def __get_array(self, f):
        size = self.__get_byte(f)
        return struct.unpack("%ds" % size, f.read(size))[0]

    def decrypt(self):

        # load database
        with open(self.desafe_filename, 'r') as f:
            magic = self.__get_short(f)
            sver = self.__get_byte(f)
            salt = self.__get_array(f)

            skey = pbkdf2.pbkdf2(self.password, salt, 10000, 32)
            iv = self.__get_array(f)
            cipher = AES.new(skey, AES.MODE_CBC, iv)
            salt2 = self.__get_array(f)
            block = self.__get_array(f)
            decr = cipher.decrypt(block)
            sub_fd = StringIO.StringIO(decr)
            iv2 = self.__get_array(sub_fd)
            pass2 = self.__get_array(sub_fd)
            check = self.__get_array(sub_fd)

            skey2 = pbkdf2.pbkdf2(pass2, salt2, 1000, 32)

            cipher = AES.new(pass2, AES.MODE_CBC, iv2)
            data = cipher.decrypt(f.read())

            decompressor = zlib.decompressobj()
            return decompressor.decompress(data) + decompressor.flush()


def is_valid(filters, content):
    if filters is None or len(filters) <= 0:
        return True
    strcontent = json.dumps(content).lower()
    for filter in filters:
        if filter.lower() in strcontent.lower():
            return True
    return False


class Shell(object):

    def __init__(self):
        self.args = docopt(__doc__, version='Desafe for Safe In Cloud 0.0.1')
        # print self.args

        file_path = self.args['<file>']
        try:
            open(file_path, "rb")  # or "a+", whatever you need
        except IOError:
            print "ERROR: could not open file '{}'".format(file_path)
            sys.exit(1)

        db = Desafe(file_path, getpass.getpass())
        try:
            self.xmldata = db.decrypt()
        except Exception:
            print "ERROR: could not decrypt file '{}'. Ensure provided password is valid".format(file_path)
            sys.exit(1)
        self.doc = xmltodict.parse(self.xmldata)

        # execute the commmand option
        if self.args['export']:
            self.export()
        if self.args['label']:
            self.print_labels()
        if self.args['card']:
            self.print_cards()

    def export(self):

        if self.args['json']:
            output = json.dumps(self.doc, indent=4)
        else:  # it must be xml
            output = self.xmldata

        if self.args['<output-file>']:
            try:
                with open(self.args['<output-file>'], "w") as f:
                    f.write(output)
            except Exception:
                print "ERROR: could not write on '{}'".format(self.args['<output-file>'])
                sys.exit(1)
        else:
            print output

    def print_labels(self):
        for db in self.doc:
            if 'label' not in self.doc[db] or len(self.doc[db]['label']) <= 0:
                print "database does not contain labels"
                return

            for label in self.doc[db]['label']:
                if '@name' in label:
                    print "label: {}".format(label['@name'])

    def print_cards(self):
        for db in self.doc:
            if 'card' not in self.doc[db] or len(self.doc[db]['card']) <= 0:
                print "database does not contain cards"
                return

            for card in self.doc[db]['card']:
                if is_valid(self.args['<filter>'], card):
                    # skip deleted ones
                    if '@deleted' in card and card['@deleted'] == 'true' and not self.args['--deleted']:
                        continue

                    if self.args['--raw']:
                        ocard = card
                        if not self.args['--password'] and 'field' in card:
                            fields = []
                            for field in card['field']:
                                if '@type' not in field or 'password' != field['@type']:
                                    fields.append(field)
                            ocard['field'] = fields
                        print json.dumps(ocard, indent=4)
                    else:
                        ocard = {'title': 'unknown', 'field': []}
                        if '@title' in card:
                            ocard['title'] = card['@title']
                        if 'field' in card:
                            # ensure field is a list
                            if not isinstance(card['field'], (list)):
                                field = []
                                field.append(card['field'])
                                card['field'] = field

                            for field in card['field']:
                                if not self.args['--password'] and '@type' in field and 'password' == field['@type']:
                                    continue
                                ofield = {'name': 'Unknown', 'text': ''}

                                if '@name' in field and field['@name']:
                                    ofield['name'] = field['@name']
                                if '#text' in field and field['#text']:
                                    ofield['text'] = field['#text']
                                ocard['field'].append(ofield)

                        print "Card: {}".format(ocard['title'])
                        for field in ocard['field']:
                            print "  {}: {}".format(field['name'], field['text'])


def main():
    Shell()

if __name__ == "__main__":
    Shell()
