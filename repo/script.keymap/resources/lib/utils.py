# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Thomas Amland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import defusedxml.ElementTree as ET
import xml.etree.ElementTree as UET
import json
import xbmc
import xbmcaddon

tr = xbmcaddon.Addon().getLocalizedString
settings = xbmcaddon.Addon().getSetting


def rpc(method, **params):
    params = json.dumps(params)
    query = '{"jsonrpc": "2.0", "method": "%s", "params": %s, "id": 1}' % (
        method, params)
    return json.loads(xbmc.executeJSONRPC(query))


def read_keymap(filename):
    ret = []
    with open(filename, 'r') as xml:
        tree = ET.iterparse(xml)
        for _, keymap in tree:
            for context in keymap:
                for device in context:
                    for mapping in device:
                        key1 = mapping.get('id') or mapping.tag
                        key2 = mapping.get('mod')
                        key = ' + '.join((key1, key2)) if key2 else key1
                        action = mapping.text
                        if action:
                            ret.append(
                                (context.tag.lower(), action.lower(), key.lower()))
    return ret


def write_keymap(keymap, filename):
    contexts = list(set([c for c, a, k in keymap]))

    builder = UET.TreeBuilder()
    builder.start("keymap", {})
    for context in contexts:
        builder.start(context, {})
        builder.start("keyboard", {})
        for c, a, k in keymap:
            if c == context:
                k = k.split(' + ')
                if len(k) > 1:
                    builder.start("key", {"id":k[0], "mod":k[1]})
                else:
                    builder.start("key", {"id":k[0]})
                builder.data(a)
                builder.end("key")
        builder.end("keyboard")
        builder.end(context)
    builder.end("keymap")
    element = builder.close()
    UET.ElementTree(element).write(filename, 'utf-8')
