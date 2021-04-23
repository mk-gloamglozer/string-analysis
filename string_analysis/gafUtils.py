from goscripts import gaf_parser,obo_tools
import pandas as pd
import glob
import os
import sys
import json
import re
import hashlib

class GafMap(dict):

    VERSIONID = "version"
    OF_BACKGROUND = "background"
    MAPID = "map"

    def __init__(self,gaf_map:dict,version:str,of_background:str):
        self.version = version
        self.of_background = of_background
        super().__init__({k:list(v) for k,v in gaf_map.items()})

    def as_dict(self):
        return {
            GafMap.VERSIONID:self.version,
            GafMap.OF_BACKGROUND:self.of_background,
            GafMap.MAPID:{k:v for k,v in self.items()}
        }
    
    @staticmethod
    def from_dict(json_dict):
        try:
            return GafMap(
                json_dict[GafMap.MAPID], 
                json_dict[GafMap.VERSIONID], 
                json_dict[GafMap.OF_BACKGROUND])
        except KeyError:
            return None

class GafManager:

    def __init__(self, gaf_file: str):
        self.gaf_file = gaf_file 

    def generate_gafmap(self, background:list) -> GafMap:
        gaf_map = self._read_map(background)

        if not gaf_map:
            gaf_map = self._new_gafmap(background)
        
        return gaf_map

    def _new_gafmap(self, background:list) -> GafMap:
        print("Gaf map not found or out of date!")
        print("Parsing gaf file...")
        gaf = gaf_parser.importGAF(self.gaf_file,background)
        version = None
        with open(self.gaf_file,'r') as f:
            for l in f:
                match = re.search(r'^!\w+-version:\ *(.*)', l)
                if not match:
                    continue
                version = match.group(1)
                break
        if not version:
            raise ValueError("no version found in gaf file\n please ensure that the file contains a line in the format !*-version: [version]")

        gafmap = GafMap(gaf,version,self._background_hash(background))
        self._save_gafmap(gafmap)
        return gafmap

    def _save_gafmap(self, gafmap: GafMap):
        with open(self._map_name(), 'w') as f:
            json.dump(gafmap.as_dict(), f)
        print("Saved new gaf configuration")

    def _read_map(self,background:list) -> GafMap:
        try:
            with open(self._map_name(),'r') as f:
                temp = json.load(f)
                gaf_map =  GafMap.from_dict(temp)

                if gaf_map.of_background != self._background_hash(background):
                    return None

                return gaf_map

        except FileNotFoundError:
            return None
        except KeyError:
            return None
        except json.JSONDecodeError:
            return None
        


    def _map_name(self) -> str:
        return self.gaf_file.replace(".gaf", ".json")

    def _background_hash(self, background:list):
        background = sorted(background)
        hasher = hashlib.md5("".join(background).encode())
        digest = hasher.digest()
        return str(int.from_bytes(digest, "big"))