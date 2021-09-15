

#
# == Pandoc-Folder ==
#
# Run pandoc on all matching files in a folder, to create one output
# document.

# =======================
# ==== "constants"  ======
# (not to be changed, but not actually protected by python)
CONFIG_FILE_REL = 'pandoc-folder-config.yml'
# =======================
# =======================


import sys
import os
from os import path
from pathlib import Path
import yaml
from pprint import pprint
from fnmatch import fnmatch

# =======================
# ===== load config =====
script_path = Path(__file__).parent.resolve()
config_file = path.join(script_path, CONFIG_FILE_REL)
with open(config_file) as stream:
   try:
      # populate global 'config' variable
      config = yaml.safe_load(stream)
   except yaml.YAMLError as ex:
      print(f"FATAL - Failed to load YAML from [{config_file}]: {ex}")
# =======================



def fatal(message):
   print(f"FATAL - {message}")
   exit(1);

def info(message):
   print(f"INFO  - {message}")

def debug(message):
   if (config['debug']):
      print(f"DEBUG - {message}")

def debug_dump(message, object):
   if (config['debug']):
      print(f"DEBUG - === {message}")
      pprint(object)
      print(f"DEBUG - ===")


def parse_args():
   this_script = str(sys.argv[0])
   if(len(sys.argv)<2):
      print("")
      print(f"  Usage:   python {this_script} path_to_folder\settings_file.yml")
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

   debug_dump("loaded settings:", settings)
   return settings


def get_file_path(settings_file):
   head_tail = path.split(settings_file);
   return head_tail[0]

def get_base_path(settings_path):
   parent_dir = str(Path(settings_path).parents[0])
   if (not path.isdir(parent_dir)):
      fatal(f"Failed to get parent dir of settings path: {settings_path}")
   return parent_dir

def get_filename_part(in_full_file):
   return os.path.basename(in_full_file)

def get_rightmost_folder(in_path):
   head_tail = path.split(in_path);
   return head_tail[1]




def path_join_norm(*args):
   return path.normpath(path.join(*args))


def parse_settings(settings_path, base_path, raw_settings):
   if ( not raw_settings['source_files_suffix']):
      fatal("missing setting: source_files_suffix")

   parsed = {
      'source_files_suffix': raw_settings['source_files_suffix']
   }

   if ( not raw_settings['out_file_rel']):
      fatal("missing setting: out_file_rel")
   if ( not type(raw_settings['out_file_rel']) is list ):
      fatal("raw_settings['out_file_rel'] should be a list")
   parsed['out_file'] = path_join_norm(base_path, *raw_settings['out_file_rel'])

   if ( raw_settings['pandoc_defaults_file'] ):
      parsed['pandoc_defaults_file'] = path_join_norm(settings_path, raw_settings['pandoc_defaults_file'] )
   if ( raw_settings['pandoc_meta_file'] ):
      parsed['pandoc_meta_file'] = path_join_norm(settings_path, raw_settings['pandoc_meta_file'] )
   if ( raw_settings['pandoc_css_file'] ):
      parsed['pandoc_css_file'] = path_join_norm(settings_path, raw_settings['pandoc_css_file'] )

   debug_dump("parsed raw_settings:", parsed)
   return parsed


def find_source_files(base_path, source_files_suffix):
   pattern = f"*.{source_files_suffix}"
   found=[]
   for sub_path, subdirs, files in os.walk(base_path):
      for name in files:
         if ( fnmatch(name, pattern)):
            full_fn = path.join(sub_path, name)
            found.append(full_fn)
            debug(f"found: {full_fn}")
   return found;



def run_pandoc(settings, found_files, source_files_suffix):
   options = []

   out_path = get_file_path(settings['out_file'])
   if(not path.isdir(out_path)):
      # create the path if it doesn't already exist.
      os.makedirs(out_path,exist_ok=True)

   if ( settings['pandoc_css_file'] ):
      options.append( f'--css="{settings["pandoc_css_file"]}"' )
   if ( settings['pandoc_meta_file'] ):
      options.append( f'--metadata-file="{settings["pandoc_meta_file"]}"' )
   if ( settings['pandoc_defaults_file'] ):
      options.append( f'--defaults="{settings["pandoc_defaults_file"]}"' )

   options.append( f'-o "{settings["out_file"]}"')

   arguments = []
   for file in found_files:
      arguments.append(f'"{file}"')

   pandoc_command = ' '.join( map(str, [ config['pandoc_command'], *options, *arguments ]))
   debug_dump("pandoc_command:", pandoc_command)

   info(f"running pandoc on {len(found_files)} {source_files_suffix} files")
   print("----")
   exit_code = os.system(pandoc_command)
   print("----")
   if ( exit_code != 0):
      fatal(f"pandoc command failed with exit code {exit_code}")

   if(not path.isfile(settings['out_file'])):
      fatal(f"Failed to create output file: {settings['out_file']}")


   bytes = path.getsize(settings['out_file']);
   info(f"created output file ({bytes} bytes): {settings['out_file']}")

   if ( config['open_file_manager']):
      out_path = get_file_path(settings['out_file'])
      file_manager_command = ' '.join( map(str, [ config['file_manager_exe'], out_path]))
      info(f"opening {config['file_manager_exe']} to folder: {out_path}")
      os.system(file_manager_command)



def main():
   debug_dump("config:", config)

   args_dict = parse_args()
   settings_file = args_dict['settings_file']
   if( not settings_file):
      fatal("failed to get settings_file from args")

   # =======================
   # ==== load settings ====

   raw_settings = load_settings(settings_file)

   settings_path = get_file_path(settings_file)
   base_path = get_base_path(settings_path)
   debug_dump("base path:", base_path)

   if ( get_rightmost_folder(settings_path) != config['require_settings_folder_name']):
      fatal(f"settings folders name must be: {config['require_settings_folder_name']}")

   settings = parse_settings(settings_path, base_path, raw_settings)

   # =======================
   # ===== run pandoc ======

   found_files = find_source_files(base_path, settings['source_files_suffix'])
   debug(f"found {len(found_files)} .{settings['source_files_suffix']} files")

   run_pandoc(settings, found_files, settings['source_files_suffix'])

   # =======================


main()
