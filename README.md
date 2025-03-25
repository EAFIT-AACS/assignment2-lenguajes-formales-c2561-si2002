# Pushdown Automaton Simulation
## Project Information
This project implements a Pushdown Automaton (PDA) based on the following context-free grammar:
S → aSb | ε
### The program allows:
1.	Manually entering a string to verify if it belongs to the language.
2.	Automatically generating valid and invalid strings and testing them.
3.	Step-by-step visualization, showing the stack state and remaining input string.
(aca pones lo tuyo)
### Requirements
To run the code, you need:

•	Python 3.x

•	Operating System: Windows, Linux, or macOS

•	Command-line terminal (CMD, PowerShell, or Bash)
### Execution Instructions
1.	Clone the Repository
…
2.	Run the Program
…
3. Use the Interactive Menu
•	Option 1: Manually enter a string.
•	Option 2: Generate valid and invalid strings automatically.
•	Option 3: Exit the program.
Technical Explanation
The PDA operates under the following rules:
1.	Each 'a' is pushed onto the stack.
2.	Each 'b' pops an 'a' from the stack.
3.	If the stack is empty at the end, the string is accepted.
4.	If the stack have an carácter at the end of the process or if there is an error during processing, the string is rejected.
During execution, the program prints:
•	Current symbol being read
•	Stack state before and after processing
•	Remaining input string
Versions Used
•	Operating System: [Your OS Version Here]
•	Programming Language: Python 3.
•	Development Tools: Visual Studio Code, Google Colab
Group Members
•	Juan Jose Escobar
•	Samuel Llano
Notes
•	Developed for the Formal Languages course.
