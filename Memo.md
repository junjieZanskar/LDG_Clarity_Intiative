# LDG Model Investigation

## Question 1:
**What’s the latest update and what’s the recent version?**

**Answer:**
[Latest Update Document](https://docs.google.com/document/d/1Dj4S8lhh6gbPJRFLeR2p_CRws_2S2Tym/edit)

The version number is **LDG-ver5-L90**, a `.DAT` file is available. 
https://drive.google.com/file/d/1xZpEdeee5hrr0ag-9YBIXtf2p3nvYlRd/view?usp=sharing

Inside the `.DAT` file, it has a version history with a description of changes.

## Version History

| Version Name | Change |
|--------------|----------------------------------------------------------------------------------------------------------------------------------|
| ver4-A1      | 44x45x16, Faults put into model by hand |
| ver4-A2      | Added deviated, implement dual porosity |
| ver4-A3      | Basic hot plate model |
| ver4-B4      | Based on natural state matches, lower hot plate |
| ver4-C6      | Added production/injection start iterations |
| ver4-C7      | Feedzone isolation in model P457 |
| ver5-D8      | Shallow regrid |
| ver5-D9      | Used Net=.10 for fract volume |
| ver5-D10     | Adjust dip in fault 5, Iterate natural state |
| ver5-D11     | Increase PI and use PAV for pressure matching/PI, add SVWRITES, move 557 to layer 5, filed in fault1 material over to 45-7 |
| ver5-D12     | High perm under fault1, fault1 deep |
| ver5-D13     | Water tagging |
| ver5-D14     | i13-7 to layer 2 outflow, i53-7 needs Fault5 perm x10, barrier between 44-7 and 55-7, deep connect, tmults |
| ver5-D15     | Matrix-fracture tmulted, barrier up one layer, i55-7 back shallower, increase in-between by a factor of 5 |
| ver5-D16     | Fault2 deep x5 perm, in-between x5 perm, 557 still shallow |
| ver5-D17     | Barrier down to layer 11, extend north and south, reduce perms in outflow layer factor of ten |
| ver5-D18     | Increase matrix perm k=.5 and por=.1, double perm on 45-7 side, triple perm on 55-7 side |
| ver5-D19     | Use fracspac 5 in outflow material with kZ=5 reduced in outflow |
| ver5-D20A    | Multiply all by 1.5, kma=.75, keep aquifer on bottom |
| ver5-D20A2   | Clay on top of fault, no natural state long run |
| ver5-D21A2   | Made changes to improve heat at 63-7, thicker fault N-S |
| ver5-E22A2   | 66A in layers 2 and 3, add between1 material west of 537 |
| ver5-E23A2   | Try down and up |
| ver5-E24A2   | Limit aquifers to only fault |
| ver5-F33     | Fixed hot plate |
| ver5-G34     | 8 component water |
| ver5-G37     | Put real 45A track, moved 53-7 injection up one layer, made 53-7 just one feed, take out tmults |
| ver5-G39     | Move 557 feed same depth as 45A |
| ver5-H40     | Changed perm connected 557 and 45A, hole in fault |
| ver5-H41     | Move 457 up to Layer 8 |
| ver5-H42     | Shorter run cut out up to 2019 |
| ver5-H43     | No hole |
| ver5-H44     | Medium hole, more sv prints |
| ver5-H45     | 557 feed back shallow |
| ver5-I57     | ALMOD |
| ver5-I58     | FLOWPath through barrier |
| ver5-I59     | FLOWPath through barrier and surface |
| ver5-I61     | Update |
| ver5-I62     | Extend crack to layer 8 |
| ver5-I63     | Reduce PI on 45/45A |
| ver5-I64     | Reduce perm of downflow to adjust drawdown 100 instead of 1000 |
| ver5-I70     | Reduce perm of downflow, reduce perm deepFault1 (lay7+) from 4E4 to 1E4 match drawdown |
| ver5-I71     | Put frac space 200m in downflow |
| ver5-I72     | Put bvmul=.33 on matrix of downflow |
| ver5-I73     | Added block of downflows in layer 8 for 45-7 |
| ver5-I74     | Return perm deepFault1 (lay7+) from 1E4 to 4E4, perm of downflow to 1000 |
| ver5-I75     | Extend crack to layer 8 vert perm, BV and frac not changed |
| ver5-K76     | Put together for update |
| ver5-K77     | Permmult 0.50 for pressure, lower ITER 0.01 |
| ver5-K78     | Permmult 0.33 for pressure, lower ITER 0.01, thinned down step, tracer out |
| ver5-K79     | Put in I3218, and data update, took out thinned down |
| ver5-K80     | Put in I3218, added fault for 32-18 |
| ver5-K81     | Put P53ST and I53ST, with fault, but messed up temp match |
| ver5-K82     | Put back i3218, no fault, put iter 0.001 |
| ver5-K83     | Injection temp 75, fixed IS file |
| ver5-K84     | Injection same as K83, put 3218 fault |
| ver5-L90     | Fix I177, inject temp down 10C after 1/2020, seasonal injection 70C/80C instead of 90C |

## Comments and Observations

1. The version history shows numerous manual changes, such as multiplying permeability by 10 and altering injection temperatures.
2. It appears that the postfix is incremented. I searched for `.sim` files throughout the entire Model folder, and the latest one I found is `LDG-ver5-M92.sim`.

## Question 2:
**How is the fracture represented in their TETRAD Model? Can we export the fracture model?**

**Note:** I have crashing issue when exporting `frac.perm`.

We may not necessarily need PetraSim, as it is primarily a post-processor/visualizer. All necessary data is available.

**TODO:**

## Question 3:
**What are the initial conditions and natural state of their model?**

**TODO:**

## Question 4:
**Why did they choose the Dual Porosity Model? Is our workflow capable of implementing it?**

**TODO:**

## Question 5:
**Can we run the model, and is there a free version of TETRAD software available?**

**TODO:**


