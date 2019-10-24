
BASE=Simple_Jacket_Decay/Main_SimpleTripod_FreeDecay
EXT=out

BASE=./Monopile_Decay/Main_MonopileOnly
EXT=outb

BASE=./OC4_Jacket_Decay/OC4Jacket_FreeDecay
EXT=out

all:  run test

run: 
	./openfast $(BASE).fst

test:
	python Test.py $(BASE)_ref.$(EXT) $(BASE).$(EXT)
