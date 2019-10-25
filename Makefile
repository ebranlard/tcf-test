
CASES= Simple_Tripod_Decay Monopile_Decay OC4_Jacket_Decay
# CASES= Simple_Tripod_Decay
RULES= $(foreach case,$(CASES), run-$(case) test-$(case))

EXT=out
FAILFILE=FAIL

# all: run test
all: start $(RULES) summary

start:
	@rm -f $(FAILFILE)

run-%: 
	@echo "------------------------- RUN $* ----------------------------------"
	@rm -f $*/Main_$*.out
	@rm -f $*/Main_$*.sum
	./openfast $*/Main_$*.fst || true

test-%:
	@echo "------------------------- TEST $* ----------------------------------"
	@python Test.py $*/Main_$*_ref.$(EXT) $*/Main_$*.$(EXT) && { echo ""; } || { echo "Fail $*">> $(FAILFILE); }

summary:
	@echo "------------------------- SUMMARY ----------------------------------"
	@test -e $(FAILFILE) && { echo "[FAIL]"; cat $(FAILFILE); exit 1; } || { echo "[ OK ]"; } 
