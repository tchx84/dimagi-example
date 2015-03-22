#!/usr/bin/env python

# Copyright (c) 2015 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import json
from operator import mul
from operator import add
from urlparse import parse_qs
from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer


ADDRESS = '127.0.0.1'
PORT = 8888


class MathEngineHandler(BaseHTTPRequestHandler):
    """Web Development, Math Engine, Exercise taken from Dimagi's website
    http://www.dimagi.com/about/careers/exercises."""

    def do_response_OK(self, response):
        """ Respond to client with the dictionary and 200 OK."""

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response)

    def do_response_BAD(self):
        """ Respond to client with 400 BAD REQUEST."""

        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        """Process values param and respond to the client with a
        dictionary contaning the sum and product in JSON format."""

        try:
            # Extract values from params
            request_params = parse_qs(urlparse(self.path).query)
            request_raw_values = request_params.get('values', None)
            request_values = json.loads(request_raw_values[0])

            # Calculate sum and product
            # XXX only non-empty numbers lists are considered valid
            response_sum = reduce(add, request_values)
            response_product = reduce(mul, request_values)

            # Serialize data in JSON format
            response_data = json.dumps({'sum': response_sum,
                                        'product': response_product})
        except:
            self.do_response_BAD()
        else:
            print response_data
            self.do_response_OK(response_data)


if __name__ == '__main__':
    """Start server and keep it running."""

    server = HTTPServer((ADDRESS, PORT), MathEngineHandler)
    try:
        print 'MathEngine is running.'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'MathEngine has stopped.'
    server.server_close()
