# Greasing Event Detection

Main goal of the project was to test the ability of detecting weak signal of greasing in the vibration time series.

## Authors

**Xavier Bouteiller**

*xavier.bouteiller@mpdata.fr* 

##  Package ConvertDXD

### Description
the folder **ConvertDXD** contains the package ConvertDXD
It allows to evaluate the quality of monitored signal within a determined number of dxd files that have been produced since the last script's execution.
it returns 
- 2 log files (i.e. one whith information of each evaluated file, and one with values averaged over files) with calculated statistics: 
	- proportion of signal equals to 0 
	- also below a threshold 
	- above a threshold
- diagnostic figures representing the calculated statistics

### How to use
user need at least to fulfil 2 arguments (argparse could be used for that)
- packagedir: path to the folder where is stored the package ConvertDXD
- Working_path: path to the folder where are stored the dxd files

The program is associated with the python program **function_toparsefile2.py**

Example of execution from the shell using argparse:
``` 
python function_toparsefile2.py --packagedir D:\\python\\script --Working_Path C:\\data\\dxd --Nmax 5 
--JL 0 --FT_below 0.15 --FT_above 100
```

### Note
the files provided by dewesoft:
- DWDataReaderHeader.py
- DWDataReaderLib64.dll

are wrapped within the folder ConvertDXD


