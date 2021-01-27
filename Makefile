CASES=

# --- Driver tests
CASES_DRIVER=
# CASES_DRIVER+= Driver_Test_Cable
# CASES_DRIVER+= Driver_Test_Rigid
# CASES_DRIVER+= Driver_Test_Joint
# CASES_DRIVER+= Driver_TetraSpar
#CASES_DRIVER+= Driver_MultiRigid ! TODO

# --- Main tests
# CASES+= SparPendulum_NoHeave
# CASES+= SparPendulumHydro_HeaveOnly
# CASES+= SparPendulumHydro
# CASES+= SparHanging
CASES+= TetraSpar_LC12
# CASES+= Monopile_Waves 
# CASES+= Monopile_Decay
# CASES+= Soil-SSI-Monopile Soil-SSI-Monopile-Baseline 
# CASES+= Soil-SSI-OC4_Jacket
# CASES+= OC4_Jacket_Decay
# CASES+= OC4_Jacket_WindWave


# --- New hydro fail...
# CASES= Spar
# CASES= Simple_Tripod_Decay
# CASES= Bipod_Decay
# CASES= Bipod_Decay_Pretension 
# CASES= Bipod_Decay_Rigid

# --- Inidividual tests
# CASES= SparPendulum_NoHeave
# CASES= Monopile_Waves
# CASES=Monopile-SoilDyn
# CASES=Spar Soil-SSI-Monopile
# CASES= OC4_Jacket_Decay
# CASES= OC4_Jacket_WindWave
# CASES+= Soil-SSI-OC4_Jacket
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
# CASES= Soil-SSI-OC4_Jacket
# CASES+= Soil-SSI-OC4_Jacket_DEBUG
# CASES= Monopile-SoilDyn-Simple
RULES= $(foreach case,$(CASES), run-$(case) test-$(case))

# 
DRIVER_FILES= $(foreach case, $(CASES_DRIVER), $(wildcard $(case)/*.dvr) )
DRIVER_RULES= $(foreach dvr, $(DRIVER_FILES), $(dvr)run $(dvr)test)

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
	@rm -f $*.SD.out
	@rm -f $*.SD.sum
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
