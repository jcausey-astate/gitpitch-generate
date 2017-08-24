#!/usr/bin/env python
'''
`gitpitch-generate`
A tool for generating entire groups of presentations using GitPitch quickly and easily.
'''
from __future__ import print_function

import sys, os, subprocess
from shutil import copy2

def main():
    args = get_args()

    src_dir = args.src_dir    if args.src_dir    is not None else  os.path.join(os.getcwd(), 'assets', 'src')
    out_dir = args.output_dir if args.output_dir is not None else  os.getcwd()

    # * Look for Markdown files in the src directory; each .md file will become a directory at the top-level.
    # * Look for YAML files named the same as the presentation source .md files and use those preferentially.
    #     - If no custom YAML exists, but a 'common.yaml' is present, use that one.
    # * Run on the directory where the output files should go (the top level dir) (DEFAULT)
    #     - default: look for `assets/src` for Markdown and YAML files
    #     - if `src-dir` option is given, look in that directory for source files
    # * If `dest-dir` option is given, place output in that directory instead

    # * After generating output files, do a `git add .` and `git commit -a` in the top-level directory.

    # Look through the src directory for .md and matching .yaml files; use common.yaml for missing .yaml files, if 
    # it exists, or set to None if there is no common.yaml.
    md_and_yaml_files = {}
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.md'):
                file_path         = os.path.join(root, file)
                presentation_name = os.path.splitext(file)[0]
                yaml_file         = os.path.join(root,'{}.yaml'.format(presentation_name))
                if not os.path.isfile(yaml_file):
                    yaml_file = os.path.join(src_dir, 'common.yaml')
                    if not os.path.isfile(yaml_file):
                        yaml_file = None
                md_and_yaml_files[slugify(presentation_name)] = (file_path, yaml_file) 
    
    # Now move the source files into corresponding directories under the output top-level, and copy in 
    # the yaml files if supplied.
    for presentation_name in md_and_yaml_files:
        presentation_dir = os.path.join(out_dir, presentation_name)
        try:
            os.makedirs(presentation_dir)
        except OSError:
            pass
        
        md_file, yaml_file = md_and_yaml_files[presentation_name]
        
        copy2(md_file, os.path.join(presentation_dir, 'PITCHME.md'))
        if yaml_file is not None:
            copy2(yaml_file, os.path.join(presentation_dir, 'PITCHME.yaml'))

    # Now, create the index:
    index_yaml = os.path.join(src_dir, 'index.yaml')
    if os.path.isfile(index_yaml):
        copy2(index_yaml, os.path.join(out_dir, 'PITCHME.yaml'))

    index_md_body = ''
    for presentation_name in sorted(md_and_yaml_files.keys()):
        index_md_body += '[{0}](?p={0})\n\n'.format(presentation_name)

    with open(os.path.join(out_dir, 'PITCHME.md'), 'wb') as fout:
        fout.write(index_md_body)

    # Now initiate a git commit:
    subprocess.call(['cd', out_dir])
    check_for_repo = subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'], stderr=subprocess.STDOUT)
    if check_for_repo.strip().lower() != 'true':
        subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit'])

    print('\nFinished generating your GitPitch presentations.')
    print('Remember: You must manually remove any presentations that are no longer current.\n')
    print('To publish, perform a `git push` next.\n')


def slugify(value, allow_unicode=False):
    '''
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    @remarks: 
        This function was adapted from the original found in the Django project:
        https://github.com/django/django/blob/master/django/utils/text.py

        Copyright (c) Django Software Foundation and individual contributors.
        All rights reserved.

        Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

            1. Redistributions of source code must retain the above copyright notice,
               this list of conditions and the following disclaimer.

            2. Redistributions in binary form must reproduce the above copyright
               notice, this list of conditions and the following disclaimer in the
               documentation and/or other materials provided with the distribution.

            3. Neither the name of Django nor the names of its contributors may be used
               to endorse or promote products derived from this software without
               specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
        ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    '''
    import unicodedata, re
    value = unicode(str(value))
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def get_args(do_usage=False):
    '''
    Parse command-line arguments.
    '''
    import argparse
    parser = argparse.ArgumentParser(
        prog='{0}'.format(os.path.basename(sys.argv[0])),
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__)
    
    parser.add_argument('--src-dir', metavar='source_directory', required=False, default=None,
        help='Directory containing Markdown and YAML source files for each presentation.')
    parser.add_argument('--output-dir', metavar='output_directory', required=False, default=None,
        help='Top-level directory where the main presentation index and sub-presentations will be placed.')

    if do_usage is not False:
        if type(do_usage) == type('str'):
            print(do_usage, file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

if __name__ == '__main__':
    main()