import os
import sys

sys.path.append(os.getcwd().rsplit(os.sep, maxsplit=1)[0])


if __name__ == '__main__':
    import notebook
    notebook.start_program()
