"""Declared adaptive common-length continuation; fresh process only."""
import isolated

LENGTHS=[1.5,1.75,2.,2.25,2.5]


if __name__=='__main__':
    isolated.ELLS=LENGTHS
    isolated.main()
