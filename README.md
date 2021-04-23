# String-analysis script

This program is designed to convert the output of MCL clustering analysis on a StringDB protein network and identify key GO terms that are related to each group. 

## Usage
Installing 

```
python -m pip install --index-url https://test.pypi.org/simple/ string-analysis-mkgloamglozer
```

Run parameters

```
python3 -m string-analysis csv_file, background
```

The program requires take one or more .csv files containing at least two columns. One column must contain Uniprot protein accession numbers and the other must contain the MCL cluster group to which the protein belongs. The accession column should be headed 'accession' and the cluster group column '__mclCluster'.

When the program is first run it must download several files and parse one large file. This takes some time. If you change the background the program must parse the file again. 

The program will automatically download the latest versions of the Gene ontology files when it is first run, however should you wish to update these files to the most recent version. This can be done using the command:
```
python3 -m string-analysis -u
```

## Output

This program will write word cloud images (.png) to a folder titled images/ within the folder that this 
script was run from. The filenames of these images will match the input file, with the group number appended. 
