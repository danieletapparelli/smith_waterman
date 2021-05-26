#!/usr/bin/env python

from smith_waterman_algorithm import SmithWaterman
from interface import Interface

def main():
   interface = Interface()
   sequence_a, sequence_b, match, mismatch, gap = interface.start()
   sequence_a = sequence_a.upper()
   sequence_b = sequence_b.upper()
   smith_waterman = SmithWaterman(sequence_a=sequence_a, sequence_b=sequence_b, match=match, mismatch=mismatch, gap=gap)
   smith_waterman.execute()


if __name__ == "__main__":
    main()
