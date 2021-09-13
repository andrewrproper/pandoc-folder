

#
# == Pandoc-Folder ==
#
# Run pandoc on all matching files in a folder, to create one output
# document.


config = {
#   'out_folder_rel': 'out-pandoc',
#   'pandoc_exec_with_path_rel': [
#      'pandoc.exe'
#   ],
   'pandoc_settings_folder': '.pandoc-folder',
   'pandoc_settings_file': '.pandoc-folder.yml',
}


# =======================


import sys
from os import path
from pathlib import Path
import yaml
from pprint import pprint

# =======================


def fatal(message):
   print(f"FATAL - {message}");
   exit(1);

def parse_args():
   this_script = str(sys.argv[0])
   if(len(sys.argv)<2):
      print("")
      print(f"  Usage: {this_script} [path_to_folder\settings_file.yml]")
      print("")
      exit(1)

   settings_file = str(sys.argv[1])

   return { 'settings_file': settings_file }


def load_settings(settings_file):
   if ( not path.isfile(settings_file) ):
      fatal(f"settings file not found: {settings_file}");

   settings = {}
   with open(settings_file) as stream:
      try:
         settings = yaml.safe_load(stream)
      except yaml.YAMLError as ex:
         fatal(f"Failed to load YAML from [{settings_file}]: {ex}")

   print("=== loaded settings:")
   pprint(settings)
   print("===")

   return settings


def get_settings_path(settings_file):
   head_tail = path.split(settings_file);
   return head_tail[0]


def get_base_path(settings_path):
   parent_dir = str(Path(settings_path).parents[0])
   if (not path.isdir(parent_dir)):
      fatal(f"Failed to get parent dir of settings file: {settings_file}")
   return parent_dir

def path_norm_join(*args):
   return path.normpath(path.join(*args))


def parse_settings(settings_path, base_path, settings):
   full_path = {}

   if ( not settings['out_short_fn']):
      fatal("missing setting: out_short_fn")

   if ( not type(settings['out_folder_rel']) is list ):
      fatal("settings['out_folder_rel'] should be a list")
   out_folder_rel = path.join(*settings['out_folder_rel'])
   print(f"out_folder_rel: {out_folder_rel}")

   if ( settings['out_short_fn'] ):
      full_path['out_fn'] = path_norm_join(base_path, out_folder_rel, settings['out_short_fn'] )

   if ( settings['pandoc_defaults_file'] ):
      full_path['pandoc_defaults_file'] = path_norm_join(settings_path, settings['pandoc_defaults_file'] )
   if ( settings['pandoc_meta_file'] ):
      full_path['pandoc_meta_file'] = path_norm_join(settings_path, settings['pandoc_meta_file'] )
   if ( settings['pandoc_css_file'] ):
      full_path['pandoc_css_file'] = path_norm_join(settings_path, settings['pandoc_css_file'] )


   print("=== parsed settings:")
   pprint(full_path)
   print("===")


   return full_path


def main():

   args_dict = parse_args()
   settings_file = args_dict['settings_file']
   if( not settings_file):
      fatal("failed to get settings_file from args")

   print("")
   print(f"  starting with settings file: {settings_file}")
   print("")

   # ===================

   settings = load_settings(settings_file)
   settings_path = get_settings_path(settings_file)
   base_path = get_base_path(settings_path)
   print(f"base_path: {base_path}")
   s = parse_settings(settings_path=settings_path, base_path=base_path, settings= settings)



   # ===================

   print("")
   print("  done.")
   print("")


main()
