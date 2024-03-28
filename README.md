#Python Compiler

Work from my Compilers course taken at IU Bloomington Fall 2023. The goal of the course was to write a compiler for a limited version of the python language. Features include basic integer math and storage, register allocation, conditionals, loops, and tuples. Functions were successfully added later, but broke certain aspects of local testing and so were not included here.

#How to use

To run the test suite, nagivate to `run-tests.py` and run it. The simple `if` statment there on line 49 can be used to choose between full testing suite and individual tests.

Note that for tuple functionality `select_instructions`, `assign_homes`, and `patch_instructions` must be removed from the `interp_dict` beforehand. The `_free_ptr` variable used for tuples does not gel with how the interpreter handles testing the x86 files. This functionality has been tested and verified to be working correctly externally, but these tests are not easily replicated locally. This does cause the testing suite to display only 75/120 passes as successful. If one  re-adds `select_instructions`, `assign_homes`, and `patch_instructions` to the `interp_dict` and runs non-tuple tests individually, they can verify that these passes do in fact succeed. 



This was a group project, based off of support code given by our professor. Our work can be found primarily in compiler.py, although we wrote sections of utils and other files as well. I wrote a large majority of this, but do not claim to have written the entireity of the file. Thank you to my group mates Jordan Keyser and Anudeep Annangi. I would also like to mention Ade Adebowale and Selina Zheng, who left our group early in the project but did contribute significantly to getting it off the ground.
