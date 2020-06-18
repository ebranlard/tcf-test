CASES=
# --- Main tests
CASES+= Bipod_Decay_Pretension Bipod_Decay Simple_Tripod_Decay Monopile_Decay Spar
CASES+= Soil-SSI-Monopile Soil-SSI-Monopile-Baseline 
CASES+= Soil-SSI-OC4_Jacket
CASES+=OC4_Jacket_Decay OC4_Jacket_WindWave
CASES+= Bipod_Decay_Rigid

# --- Inidividual tests
# CASES=Monopile-SoilDyn
# CASES=Spar Soil-SSI-Monopile
# CASES= Bipod_Decay
# CASES+= Bipod_Decay_Pretension 
# CASES= Bipod_Decay Monopile_Decay
# CASES= OC4_Jacket_Decay
# CASES= OC4_Jacket_WindWave
# CASES+= Soil-SSI-OC4_Jacket
# CASES=Spar
# CASES = Bipod_Decay
# CASES= Simple_Tripod_Decay
# CASES= Monopile_Decay
# --- TODO NEW
# CASES= OC4_Jacket_Decay_RigidInterf
# CASES= Bipod_Decay_RigidInterf 
# CASES = SeaBedMoment
# CASES = Bug_Static
# CASES= Bipod_Decay_Ball
# CASES= Bipod_Decay_Pin
# CASES= Bipod_Decay_Universal
# CASES= Monopile_WavesTopMass
# CASES+= OC4_Jacket_WindWave
# CASES+= Soil-SSI-OC4_Jacket
# CASES+= Soil-SSI-OC4_Jacket_DEBUG
# CASES= Monopile-SoilDyn-Simple
RULES= $(foreach case,$(CASES), run-$(case) test-$(case))

CASES_DRIVER=
CASES_DRIVER+=Driver_Test_Cable
CASES_DRIVER+=Driver_Test_Rigid

DRIVER_FILES= $(foreach case, $(CASES_DRIVER), $(wildcard $(case)/*.dvr) )
DRIVER_RULES= $(foreach dvr, $(DRIVER_FILES), $(dvr)run $(dvr)test)
# DRIVER_RULES = $(patsubst %.dvr,%.rundvr,  $(DRIVER_FILES))

EXT=out
FAILFILE=FAIL

# default:
# 	./subdyn_driver Test_Cable/Main_Test_Cable_3Joints.dvr
# 	./openfast SeaBedMoment/OC6_phaseII_LC1_MonopileOnlySubDyn.fst  

# all: run test

all: start $(DRIVER_RULES) $(RULES) summary

start:
	@rm -f $(FAILFILE)

%.dvrrun: 
	@echo "------------------------- RUN $* ----------------------------------"
	rm -f $*.SD.out
	rm -f $*.SD.sum
	@./subdyn_driver $*.dvr || true

%.dvrtest: 
	@echo "------------------------- TEST $* ----------------------------------"
	@python Test.py $*.SD_ref.$(EXT) $*.SD.$(EXT) && { echo ""; } || { echo "Fail $*">> $(FAILFILE); }


run-%: 
	@echo "------------------------- RUN $* ----------------------------------"
	@rm -f $*/Main_$*.out
	@rm -f $*/Main_$*.sum
	@./openfast $*/Main_$*.fst || true

runnew-%: 
	@echo "------------------------- RUN $* ----------------------------------"
	@rm -f $*/Main_$*.out
	@rm -f $*/Main_$*.sum
	@./openfast $*/Main_$*.fst || true

test-%:
	@echo "------------------------- TEST $* ----------------------------------"
	@python Test.py $*/Main_$*_ref.$(EXT) $*/Main_$*.$(EXT) && { echo ""; } || { echo "Fail $*">> $(FAILFILE); }



summary:
	@echo "------------------------- SUMMARY ----------------------------------"
	@test -e $(FAILFILE) && { echo "[FAIL]"; cat $(FAILFILE); exit 1; } || { echo "[ OK ]"; } 
