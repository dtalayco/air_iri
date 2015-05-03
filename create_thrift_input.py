#!/usr/bin/env python
#
# This script reads in an AIR/IRI switch description and 
# produces thrift input files for the switch.

import re
import os
import argparse
import tenjin.util

from air.air_instance import AirInstance

class ThriftAirInstance(AirInstance):
    """
    Use the AIR processing on the YAML input and extend
    """

    def render_dict_gen(self):
        """
        Create the rendering dictionary for this switch's input

        Probably this is just the AIR parent object
        """
        self.render_dict = {}
        self.render_dict["air"] = self
        self.render_dict["switch_prefix"] = self.name

    def __init__(self, input, name):
        AirInstance.__init__(self)
        self.name = name
        self.add_content(input)
        self.render_dict_gen()

    def process_files(self, template_dir, target_dir):

        global args

        # Files to ignore when looking for templates
        ignore_pattern = re.compile('^\..*|.*\.cache$|.*~$')

        # Line prefix to use for templates processed by Tenjin
        tenjin_prefix = "::"

        def file_name_ignore(filename):
            return ignore_pattern.match(filename)

        # for each file in template dir apply tenjin to it with local dict
        for root, subdirs, files in os.walk(template_dir):
            for filename in files:
                if file_name_ignore(filename):
                    continue
                template_file = os.path.join(root, filename)
                template_rel = os.path.relpath(os.path.join(root, filename),
                                               template_dir)
                target_file = os.path.join(target_dir, template_rel)
                try:
                    os.makedirs(os.path.dirname(target_file))
                except OSError:
                    pass
                if args.verbose:
                    print "Template: ", template_file
                    print "  Target: ", target_file

                with open(target_file, "w") as f:
                    # Use relative path for template name and give template dir
                    tenjin.util.render_template(f, template_rel, 
                                                self.render_dict,
                                                template_dir,
                                                prefix=tenjin_prefix)


config_defaults = {
    "template_dir" : "templates",
    "dest_dir" : "thrift",
    "name" : "ichiban"
}

parser = argparse.ArgumentParser(description='Produce thrift intf files',
        usage="%(prog)s source [source ...] [options]")
parser.set_defaults(**config_defaults)
parser.add_argument('sources', metavar='sources', type=str, nargs='+',
                    help='The source file to load')
parser.add_argument('-t', '--template_dir', type=str,
                    help='Where to find templates')
parser.add_argument('-o', '--output', type=str,
                    help='Where to put results')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Verbose output")
parser.add_argument('-n', '--name', type=str,
                    help="Name of switch instance")

args = parser.parse_args()

t = ThriftAirInstance(args.sources, args.name)
t.process_files(args.template_dir, args.dest_dir)
