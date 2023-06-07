# this is a format transformer for interaction files from miyagi code to nicolas GSM code.
import math

# * ----------------------------------------------
# * input
# * ----------------------------------------------
# * original interaction file by miyagi code.
input_file = "TwBME-HO_NN-only_N3LO_EMN500_srg2.2_hw12-with-coulomb_emax12_e2max24.snt"
hw = 12

# * ----------------------------------------------
# * output
# * ----------------------------------------------
# * resulting interaction file in standard nicolas GSM code.
result_file = "v2body_HO_lab_TwBME-HO_NN-only_N3LO_EMN500_srg2.2_hw12-with-coulomb_emax12_e2max24.dat"


# * ----------------------------------------------
# * main programe
# * ----------------------------------------------
orbit_number = 0
orbit = []
interaction = []

orbit_table = "spdfghijklmnox"

mu = 938.91897  # nucleon mass
b = 197.326968 / math.sqrt(mu * hw)  # harmonic oscillator length


def orbit_name(index):
    n = str(orbit[index - 1][1])
    l = orbit_table[orbit[index - 1][2]]
    j = str(orbit[index - 1][3]) + "/2"
    temp = n + l + j
    return temp


def orbit_tz(index):
    temp = orbit[index - 1][4]
    return temp


with open(result_file, "w") as f_w:
    f_w.write(str(b) + "\n")
    with open(input_file, "r", encoding="utf-8", newline="") as f:
        h = 0
        for line in f:
            line = line.replace("\n", "")
            temp = line.split(" ")

            if h == 1:
                while "" in temp:
                    temp.remove("")
                orbit_number = int(temp[0]) * 2
                # print(orbit_number)

            elif h > 1 and h <= (orbit_number + 1):
                while "" in temp:
                    temp.remove("")
                temp_orbit = [
                    int(temp[0]),
                    int(temp[1]),
                    int(temp[2]),
                    int(temp[3]),
                    int(temp[4]),
                ]
                # print(temp_orbit)
                orbit.append(temp_orbit)

            elif h >= (orbit_number + 8):
                while "" in temp:
                    temp.remove("")
                tz = int((orbit_tz(int(temp[0])) + orbit_tz(int(temp[1]))) / 2)
                interaction_temp = (
                    str(orbit_name(int(temp[0])))
                    + " "
                    + str(orbit_name(int(temp[1])))
                    + " "
                    + str(orbit_name(int(temp[2])))
                    + " "
                    + str(orbit_name(int(temp[3])))
                    + " "
                    + temp[4]
                    + " "
                    + str(tz)
                    + " "
                    + temp[5]
                    + "\n"
                )
                f_w.writelines(interaction_temp)
            h = h + 1
