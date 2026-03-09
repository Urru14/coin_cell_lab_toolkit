import math

print("\nBATTERY ELECTRODE LAB CALCULATOR")
print("----------------------------------")

# ===============================
# LAB CONSTANTS
# ===============================

ELECTRODE_DIAMETER = 16
CU_FOIL = 18.1
AG_FOIL = 7.92

area = math.pi * (ELECTRODE_DIAMETER/20)**2

# ===============================
# SLURRY DATABASE (DIRECT)
# ===============================

slurry_db = {

1: {"active":"Graphite","binder":"CMC","conductive":"Super P","type":"Anode","source":"Default"},
2: {"active":"Graphite","binder":"PVDF","conductive":"Super P","type":"Anode","source":"Default"},
3: {"active":"NMC","binder":"PVDF","conductive":"Super P","type":"Cathode","source":"Default"},
4: {"active":"LFP","binder":"PVDF","conductive":"Super P","type":"Cathode","source":"Default"},
5: {"active":"Silicon","binder":"CMC","conductive":"Super P","type":"Anode","source":"Default"},
6: {"active":"LiNi0.5Mn1.5O4","binder":"PVDF","conductive":"Super P","type":"Cathode","source":"Default"}

}

# ===============================
# SPECIFIC CAPACITY DATABASE
# ===============================

capacity_db = {

"Graphite":372,
"Silicon":3579,
"LTO":175,
"NMC":160,
"LFP":170,
"LiNi0.5Mn1.5O4":147

}

# ===============================
# SHOW SLURRY OPTIONS
# ===============================

print("\nSelect slurry composition\n")

for k,v in slurry_db.items():

    text = f"{k} : {v['active']} + {v['binder']} + {v['conductive']} ({v['type']})"

    print(text)

print(f"{len(slurry_db)+1} : Custom")

choice = int(input("\nOption: "))

# ===============================
# CUSTOM SLURRY
# ===============================

if choice not in slurry_db:

    print("\nCustom slurry")

    active = input("Active material: ")
    binder = input("Binder: ")
    conductive = input("Conductive additive: ")
    electrode_type = input("Electrode type (Anode/Cathode): ")

else:

    data = slurry_db[choice]

    active = data["active"]
    binder = data["binder"]
    conductive = data["conductive"]
    electrode_type = data["type"]

# ===============================
# THEORETICAL CAPACITY
# ===============================

if active in capacity_db:

    capacity = capacity_db[active]

    print("\nDetected active material:",active)
    print("Electrode type:",electrode_type)
    print("Theoretical capacity:",capacity,"mAh/g")

    confirm = input("Use this value? (y/n): ")

    if confirm.lower()=="n":

        capacity = float(input("Enter theoretical capacity (mAh/g): "))

else:

    print("\nMaterial not in capacity database")

    capacity = float(input("Enter theoretical capacity (mAh/g): "))

# ===============================
# SLURRY PREPARATION
# ===============================

target_mass = float(input("\nTarget slurry mass (mg): "))

print("\nEnter component masses (mg)\n")

active_mass_slurry = float(input(f"{active}: "))
binder_mass = float(input(f"{binder}: "))
carbon_mass = float(input(f"{conductive}: "))

actual_mass = active_mass_slurry + binder_mass + carbon_mass

print("\nActual slurry mass:",actual_mass,"mg")
print("Difference from target:",actual_mass-target_mass,"mg")

active_fraction = active_mass_slurry/actual_mass

# ===============================
# NUMBER OF CELLS
# ===============================

cells = int(input("\nNumber of cells: "))

for i in range(cells):

    print("\n------ Cell",i+1,"------")

    print("\nSelect substrate / foil")
    print("1 : Cu foil (18.1 mg)")
    print("2 : Ag foil (7.92 mg)")
    print("3 : Enter foil mass manually")

    sub = int(input("Option: "))

    if sub == 1:
        foil_mass = CU_FOIL

    elif sub == 2:
        foil_mass = AG_FOIL

    else:
        foil_mass = float(input("Enter foil mass (mg): "))

    total_mass = float(input("Total electrode mass (mg): "))

    film_mass = total_mass - foil_mass

    active_mass = film_mass * active_fraction

    areal_loading = active_mass/area

    print("\nSlurry film mass:",film_mass,"mg")
    print("Active material mass:",active_mass,"mg")
    print("Areal loading:",areal_loading,"mg/cm²")

# ===============================
# C-RATE CURRENTS
# ===============================

    active_g = active_mass/1000

    current_1C = capacity*active_g

    print("\nC-rate currents")

    print("1C =",current_1C,"mA")
    print("C/2 =",current_1C/2,"mA")
    print("C/5 =",current_1C/5,"mA")
    print("C/10 =",current_1C/10,"mA")

    custom = input("\nCustom C-rate? (y/n): ")

    if custom.lower()=="y":

        rate = float(input("Enter C-rate: "))

        print("Current =",current_1C*rate,"mA")

print("\nCalculation complete.")
