# Acknowledgements
Contributions from Kevin Lewi for external FHIPE code

# Current Issues
The Kevin Lewi FHIPE implementation is not compatible with systems running open ssl 1.1.1 and above due to changes in how structures like BIGINT are being handled. It is recommended to either downgrade to openssl 1.02 or to try finding a wrapper that allows for compatibility fixes

# Summary of files
Ext_Files - contains the compiled c libraries from Kevin Lewi's code
External_Files - contains the libraries charm and flint - currently bein gused by Kevin Lewi's implementation. Given that there is no c api, there is no current use for them in the UDFs
CPP.cpp        - cpp file containing code for the UDF