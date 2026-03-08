import csv
import math
import os

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
# CREATE DATABASE FILES IF MISSING
# ===============================

if not os.path.exists("slurry_database.csv"):

    with open("slurry_database.csv","w",newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Option",
            "Active Material",
            "Binder",
            "Conductive Additive",
            "Electrode Type",
            "Source"
        ])

        writer.writerow([1,"Graphite","CMC","Super P","Anode","Default"])
        writer.writerow([2,"Graphite","PVDF","Super P","Anode","Default"])
        writer.writerow([3,"NMC","PVDF","Super P","Cathode","Default"])
        writer.writerow([4,"LFP","PVDF","Super P","Cathode","Default"])
        writer.writerow([5,"Silicon","CMC","Super P","Anode","Default"])
        writer.writerow([6,"LiNi0.5Mn1.5O4","PVDF","Super P","Cathode","Default"])

if not os.path.exists("specific_capacity_database.csv"):

    with open("specific_capacity_database.csv","w",newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Material",
            "Theoretical Capacity (mAh/g)"
        ])

        writer.writerow(["Graphite",372])
        writer.writerow(["Silicon",3579])
        writer.writerow(["LTO",175])
        writer.writerow(["NMC",160])
        writer.writerow(["LFP",170])
        writer.writerow(["LiNi0.5Mn1.5O4",147])

# ===============================
# FUNCTION TO SAVE NEW SLURRY
# ===============================

def save_new_slurry(active,binder,conductive,electrode_type):

    with open("slurry_database.csv","r") as f:
        rows = list(csv.reader(f))

    last_option = int(rows[-1][0])
    new_option = last_option + 1

    with open("slurry_database.csv","a",newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            new_option,
            active,
            binder,
            conductive,
            electrode_type,
            "User"
        ])

    print("\nNew slurry saved as option",new_option)

# ===============================
# LOAD SLURRY DATABASE
# ===============================

slurry_db = {}

with open("slurry_database.csv","r") as f:

    reader = csv.DictReader(f)

    for row in reader:

        option = int(row["Option"])

        slurry_db[option] = {

            "active":row["Active Material"],
            "binder":row["Binder"],
            "conductive":row["Conductive Additive"],
            "type":row["Electrode Type"],
            "source":row.get("Source","Default")

        }

# ===============================
# LOAD CAPACITY DATABASE
# ===============================

capacity_db = {}

with open("specific_capacity_database.csv","r") as f:

    reader = csv.DictReader(f)

    for row in reader:

        capacity_db[row["Material"]] = float(row["Theoretical Capacity (mAh/g)"])

# ===============================
# SHOW SLURRY OPTIONS
# ===============================

print("\nSelect slurry composition\n")

for k,v in slurry_db.items():

    text = f"{k} : {v['active']} + {v['binder']} + {v['conductive']} ({v['type']})"

    if v["source"] == "User":
        text += " [User Added]"

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

    save = input("Save this composition to database? (y/n): ")

    if save.lower()=="y":

        save_new_slurry(active,binder,conductive,electrode_type)

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
