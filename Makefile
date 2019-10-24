all:  run test

run: 
	./openfast ./Simple_Jacket_Decay/Main_SimpleTripod_FreeDecay.fst   


BASE=Simple_Jacket_Decay/Main_SimpleTripod_FreeDecay
EXT=out

test:
	python Test.py $(BASE)_ref.$(EXT) $(BASE).$(EXT)
