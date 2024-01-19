# Versions Digger

**This script is an extra script. It helped me to search quickly GitHub links amoung all possible versions of the given `G:A`. This is not neccesasry for the correct execution of MGHL, just an extra tool.**

Versions Digger is a simple script that will take in input a GroupID and ArtefactI (from a file called `GroupID_ArtefactID.txt`), search for all versions available on Maven repository (for the given GroupID, ArtefatID) and output the first version that united to rhe GroupID and ArtefactID have a link to GitHup repository.

## Installation
Not needed, as you clone the MGHL repository, you already have a folder called `Versions Digger`. Enter into that directory and execute the `main.py` file.


## Usage
`versions/` directory contains one file for each `GroupID:ArtefactID` (syntax: `GroupID_ArtefactID.txt`) which contains a list of versions for that `G:A` as published on maven repository (may be many). From each file, read all the versions available, construct a GAV link to the POM file on maven download it and search inside for github links.

If you don't have the `GroupID_ArtefactID.txt` file for a specigic `GroupID:ArtefactID` you want to anlyze then you can create it using the main tool: edit the code so that it saves all the versions retrieved from maven into a file called `GroupID_ArtefactID.txt`.
 
The usage is very easy.

```bash
python3 main.py 
```
Be carefull, this will analyze all the files in the folder `versions/` so remove all unwanted files before launching it.

## License

[MIT](https://choosealicense.com/licenses/mit/)
