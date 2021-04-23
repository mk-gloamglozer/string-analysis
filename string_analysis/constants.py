from os import path

RESOURCES_FOLDER = path.join(path.dirname(__file__), "resources")
TEXTFILE_FOLDER = path.join(RESOURCES_FOLDER, "text_files")
GAF_FILELOCATION = path.join(RESOURCES_FOLDER, "goa_human.gaf")
OBO_FILELOCATION = path.join(RESOURCES_FOLDER, "go.obo")
UPDATE_SCRIPT_LOCATION = path.join(RESOURCES_FOLDER,"update.sh")
COLORS ={
    1:'#33CCFF',
    2:'#9966FF',
    3:'#FF6666',
    4:'#99FF99',
    5:'#FFCC66'
}

URL_OBO = "http://purl.obolibrary.org/obo/go.obo"
URL_GAF = "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/goa_human.gaf.gz" 
GAF_ZIP_FILE = path.join(RESOURCES_FOLDER, "goa_human.gaf.gz")