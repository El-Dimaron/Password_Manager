Code is used as an in-terminal password manager.

When executing a code, there are 2 options:
1. Create a new password [new];
2. View created password(s) [list].

When creating a new password, there are two optional arguments that need to be specified [--title] and [--login].

Additional optional arguments can be added to change the password creation parameters.
- -l, --letters - if True, both upper and lower registers letters will be used, if False - only lower ones (default, True);
- -s, --symbols - if True, the following symbols will be added to the password "!@#$%^&*()+" (default, False);
- -n, --numbers - if True, adds numbers (0-9) to the password (default, False); 
- -d, --duplicates - if True, only unique elements will be used, no repetition (default, False); 
- -p, --pass_length - determines the length of the password (default, 8).

Note: when it is necessary to create a unique-element password (duplicates=True), please do not set pass_length to a value higher than 30, as the password might run out of unique elements and the function will display an error.

Example for password creation (all arguments used):
python pass_manager.py new --title Facebook --login El-Dimaron -l True -s True -n True -d True -p 12


To view the existing password(s), command [list] is used.

If no additional argument is specified, the command will display the list of all created password title names.

If used with additional optional argument [--title], the title_name of the password title name should be added in order to view the password information.

Example for viewing existing password:
python pass_manager.py list --title Facebook

Enjoy the code and have a nice one!