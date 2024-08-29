# LibreOffice Calc to SQL Database Converter

## Compiling
Use the command `make` inside the direcotry

## Running
usage : `./ods_to_db ods_filename.ods database_filename.db ods_file_sheet_name database_table_name`

exeample: `./ods_to_db interventions.ods database.db Sheet1 interventions`

## Installing the program
To install this program in you Linux distribution for all users, you can do
`make install`

## Debugging
To debug, you can add the `-d` or `--debug` flag at the end of the arguments

## Dependencies
You must have python 3.12 and "Make" installed.


## Credits
### Python packages
pyexcel_ods3 : https://github.com/pyexcel/pyexcel-ods3
### Creator
Firas Zaazaa, FOSS