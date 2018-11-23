# AI-in-cybersecurity

How to Prepare Data
---------------------
Requirement: Binary codes that are already labelled as vulnerable(bad) or not vulnerable(good). This is required to train the AI model to recognise vulnerable and invulnerable codes.

In this project, binary codes are processed from codes from Juliet Test Suite, created by the National Security Agency’s (NSA) Center for Assured Software (CAS). It is a collection of codes in high level languages that may be sorted by their CWE categories. Each code in the test suite are also labelled as good,bad or mixed, depending on whether they have the CWE weakness within the code. As the goal of the project is the evaluation of binary codes, the codes from the test suite are compiled to binary codes, and then disassembled to assembly codes.

Each function of the code is extracted and disassembled from the binary code, and stored inside a text file. This project uses 14214 test cases (evenly split into good and bad ones), which implies that 14214 text files were created.

The end goal of preprocessing would be a 3D matrix of ones and zeroes. To do so, conversion from strings to numbers is required. As such, a dictionary is built for all keywords of assembly code. In this project, register keywords were entered manually, while other keywords such as mov, push and sub were extracted dynamically. The values of keywords in the dictionary are numbers, where no two keywords have the same number. All numbers and addresses are assigned to the custom keyword "num" (value: 1).

After the dictionary has been built, all words in assembly codes are replaced by their corresponding dictionary values. Each file would be an array of numbers, which represent assembly codes. 

After replacing the values, arrays should be trimmed or padded to a specific length. In this project, the specific length is 200.

If the array is longer than the specific length, it should be trimmed from the end.

If it is shorter, it should be padded with "0"s (or any number that is not in the dictionary).

As a lot of data is required for training, many files are processed in a similar fashion, and they share one dictionary. All files share one dictionary as consistency is required in the numbering of keywords. As the files are already labelled, vulnerable test cases are assigned as 0, and invulnerable test cases are assigned as 1. This data would eventually be stored in a .csv file.

The array of arrays would refer to a list of files, and each file is preprocessed. This is a 2D matrix, which is a step from completion of preprocessing.

To convert the 2D matrix into a 3D one, one-hot encoding is used, as the requirement to convert from 2D to 3D would be to turn each number into an array.

To encode a number within a range, a list of zeroes of the length equal to the highest number in range is created. (Assuming the smallest number is either 0 or 1.) Then, the nth place, where n is the number itself, is changed to 1.

For example, on a range from 1 to 3, a list [3,1,2] would be encoded as:

[[0,0,1],

[1,0,0],

[0,1,0]]

One-hot encoding can be achieved using the numpy.eye method. The actual code is in the DLModel Jupyter Notebook.

Store the 3D matrix into a .csv file, and it would then be ready for usage in AI training. The shape(dimension) of the 3D matrix should be (number_of_assembly_code_files x specific_length x length_of_dictionary+1). "+1" being the value used for padding.

For data that is used for predicting, it should also be processed in a similar fashion.

Experiments Excel Sheet
-------
This file contains the graphs produced by various test cases. Different worksheets have a different variable, which is used to determine how it will affect the performance of the AI model. Testing can be done by observing the test results in the file, and making conjectures.

The worksheets are as categorized: Unsorted, Dropout, Epoch, Neurons
