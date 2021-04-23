from goscripts import obo_tools
import pandas as pd
from . import warnings
from . import gafUtils
import os
from os import path
import re

CLUSTER_COL = "__mclCluster"
ACCESSION_COL = "accession"
ALT_ACCESSION_COL = "query term"

class GroupTerm:
    def __init__(self, group:str, terms:list):
        self.group = group
        self.terms = terms

def generate(inputfilenames, 
        obo_path:str, 
        gaf_path:str, 
        background:list,
        out_folder:str):

    obo_map = obo_tools.importOBO(obo_path,False)
    gaf_map = gafUtils.GafManager(gaf_path).generate_gafmap(background)

    for inputfile in inputfilenames:
        warnings.set_header(inputfile)
        df = df_from_input(inputfile)
        create_term_files(df, obo_map, gaf_map,inputfile,out_folder)
        warnings.flush()

def write_groupterm(groupterm:GroupTerm, input_file:str,out_folder:str):

    terms = groupterm.terms
    group = groupterm.group

    if len(terms) < 1:
        warnings.add_warning("No terms were mapped")
        return

    out_path = re.sub(r'\.\w+$', f"_group_{int(group)}.txt" ,os.path.basename(input_file))
    out_path = os.path.join(out_folder,out_path)

    if not path.exists(out_folder):
        os.makedirs(out_folder)
    
    with open(out_path,'w') as f:
        f.write('\n'.join(terms))

def df_from_input(inputfile:str) -> pd.DataFrame:
    try:
        return pd.read_csv(inputfile)
    except Exception as e:
        raise ValueError(str(e))

def create_term_files(df:pd.DataFrame,
        obo_map:dict, 
        gaf_map:gafUtils.GafMap,
        inputfile, out_folder) -> GroupTerm:
    try:
        for group, data in df.groupby(by=CLUSTER_COL):
            accessions = _accessions_from_dataframe(data)
            terms = _terms_from_accessions(accessions, obo_map, gaf_map)
            group_term = GroupTerm(group,terms)
            write_groupterm(group_term, inputfile,out_folder)
    except KeyError:
        raise ValueError(f"Missing column name: {CLUSTER_COL}")

def _terms_from_accessions(accessions:list, obo_map:dict, gaf_map:dict) -> list:

    terms = [
        obo_map.get(term)
        for accession in accessions
        for term in gaf_map.get(accession, [])
    ]

    terms = [t.name for t in terms if t is not None]
    return terms



def _accessions_from_dataframe(data:pd.DataFrame) ->  pd.Series:

    try:
        return data[ACCESSION_COL]
    except KeyError:
        try:
            accessions = data[ALT_ACCESSION_COL]
            warnings.add_warning(f"Using {ALT_ACCESSION_COL} as backup column. This may give undesired results if the String ID was used as query rather than Accession.\n")
            return accessions
        except KeyError:
            raise ValueError("No applicable column found")

