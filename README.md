# OpenViBE GDF File Fixer

The OpenViBE GDF File Fixer is a graphical interface designed to fix corrupted
GDF Files that were created by OpenViBE.  
It allows you to open one or more GDF files in order to check if they are corrupted
and fix them if needed.

Note that this tool only looks for a specific corruption that was introduced in specific versions of OpenViBE (seel below).

## Which files need to be fixed ?

Any GDF file generated with OpenViBE from the versions **v3.0.0**, **v3.1.0**, **v3.2.0**, **v3.3.0** is impacted.

## Which files do not need fixing ?

Any GDF file generated with OpenViBE 2.2.0 and earlier.  
The impacted versions of OpenViBE are also being patched into v3.#.1. The patched versions will also be safe to use for GDF recording. 

## How are the files corrupted ?

The corruption in the files is impacting the stimulations.  
An error in the Event Table header causes a shift in the stimulations, which 
means that the times of the stimulations are correct but the stimulation codes
are shifted. Finally the **last stimulation is lost**.

**Expected record:**

| Event Id | Event Date | Event Duration |
|---------:|:-----------|:---------------|
|    32769 | 1.00000000 |  0.0000000000  |
|      768 | 5.00000000 |  0.0000000000  |
|      786 | 7.00000000 |  0.0000000000  |
| ...      | ...        |  ...           |


**Record on reading:**  

| Event Id | Event Date | Event Duration | Observation                             |
|---------:|:-----------|:---------------|:---------------------------------------:|
|        3 | 1.00000000 |  0.0000000000  | Random stimulation at first event date  |
|    32769 | 5.00000000 |  0.0000000000  | First stimulation at second event date  |           |
|      786 | 7.00000000 |  0.0000000000  | Second stimulation at third event date  |           |
| ...      | ...        |  ...           | And so on...                            |

<br/>

#### The technical issue:
To be more precise, the corruption in the header of the Event Table is 
due to the field _"Number of Events"_ being written on 8 bytes, instead of 4.  
Parsers read 4 bytes for the _"Number of Events"_ field, and then expect to read stimulation codes, except
they start by reading the 4 extras bytes of data that were not supposed to be there.

## How can it be fixed ?

As it happens, only the Event Table header is corrupted, and OpenViBE actually
wrote all the stimulations to the file. They are just not processed since they
are not expected by the GDF readers.

The OpenViBE GDF File Fixer is therefore parsing files in order to detect a 
discrepancy between the header information and the actual size of the file,
and fix the header if needed, without any information loss on the recovered file.

## How to run OpenViBE GDF File Fixer

###### _- Requirement:_ Python 3.7

Run the following command:  
`python src/main.py`