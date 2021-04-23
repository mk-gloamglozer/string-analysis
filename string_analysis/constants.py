from os import path

RESOURCES_FOLDER = path.join(path.dirname(__file__), "..", "resources")
TEXTFILE_FOLDER = path.join(RESOURCES_FOLDER, "text_files")
GAF_FILELOCATION = path.join(RESOURCES_FOLDER, "goa_human.gaf")
OBO_FILELOCATION = path.join(RESOURCES_FOLDER, "go.obo")
COLORS ={
    1:'#33CCFF',
    2:'#9966FF',
    3:'#FF6666',
    4:'#99FF99',
    5:'#FFCC66'
}