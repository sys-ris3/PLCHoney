This will need to install **RS_Logix** from Rockwell Automation to open the programs.
- Download samples (*.exe) from Rockwell Samples
- The exe files are actually compressed code files. Unzip them in Windows.
- Open the *.ACD project files in RS_Logix

- The *.CSV files are exported tags and components.
- These files cannot be imported to OpenPLC_Editor:
  - Some data types defined in RS_Logix are not supported
  - Add on Instructions (AOI)
  - Input/Output may have read/write permissions, still not supported 
