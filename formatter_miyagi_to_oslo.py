# this is a format transformer for interaction files from miyagi .snt format to oslo format.
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
# * resulting interaction file in standard oslo format.
sp_file = "oslo_test_orb.dat"
int_file = "oslo_test.dat"


# * ----------------------------------------------
# * main programe
# * ----------------------------------------------
orbit_number = 0
interaction_number = 0
orbit = []
interaction = []


mu = 938.91897  # nucleon mass
b = 197.326968 / math.sqrt(mu * hw)  # harmonic oscillator length


def orbit_tz(index):
    temp = orbit[index - 1][4]
    return temp


# read and store sp data.
with open(input_file, "r", encoding="utf-8", newline="") as f:
    h = 0
    for line in f:
        line = line.replace("\n", "")
        temp = line.split(" ")
        if h == 1:
            while "" in temp:
                temp.remove("")
            orbit_number = int(temp[0]) * 2
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
            orbit.append(temp_orbit)
        h = h + 1

# write sp data.
with open(sp_file, "w") as fsp_w:
    fsp_w.write(
        "   ----> Oscillator parameters, Model space and single-particle data\n"
    )
    fsp_w.write(
        "Mass number A of chosen nucleus (important for CoM corrections):          0\n"
    )
    fsp_w.write(
        "Oscillator length and energy: "
        + "{:.6E}".format(b)
        + " "
        + "{:.6E}".format(hw)
        + "\n"
    )
    fsp_w.write(" Min and max value of partial wave ang. mom           0          10\n")
    fsp_w.write(" Max value of relative orb mom or cm orb mom,  l or L=           11\n")
    fsp_w.write(
        " Max value of relative n: "
        + str(max(orbit[i][1] for i in range(len(orbit))))
        + "\n"
    )
    fsp_w.write(
        " Max value of 2*n + l+ cm 2*N +L for large space: "
        + str(2 * max(2 * orbit[i][1] + orbit[i][2] for i in range(len(orbit))))
        + "\n"
    )
    fsp_w.write(
        " Max value of 2*n + l+ cm 2*N +L for model space: "
        + str(2 * max(2 * orbit[i][1] + orbit[i][2] for i in range(len(orbit))))
        + "\n"
    )
    fsp_w.write(" Total number of single-particle orbits " + str(len(orbit)) + "\n")
    fsp_w.write(
        "Legend: {:>4} {:>8} {:>8} {:>8} {:>8} {:>8} {:>18} {:>18}  {:>16} {:>16} \n".format(
            "",
            "n",
            "l",
            "2j",
            "tz",
            "2n+l",
            "HO-energy",
            "evalence",
            "particle/hole",
            "inside/outside",
        )
    )
    for temp_orbit in orbit:
        fsp_w.write(
            "Number: {:>4} {:>8} {:>8} {:>8} {:>8} {:>8} {:>18} {:>18}  {:>16} {:>16}\n".format(
                temp_orbit[0],
                temp_orbit[1],
                temp_orbit[2],
                temp_orbit[3],
                temp_orbit[4],
                2 * temp_orbit[1] + temp_orbit[2],
                "{:.6E}".format((2 * temp_orbit[1] + temp_orbit[2] + 1.5) * hw),
                "0.000000E+00",
                "particle",
                "inside",
            )
        )

# write interaction data.
with open(int_file, "w") as fint_w:
    with open(input_file, "r", encoding="utf-8", newline="") as f:
        h = 0
        for line in f:
            line = line.replace("\n", "")
            temp = line.split(" ")
            if h == (orbit_number + 5):
                while "" in temp:
                    temp.remove("")
                interaction_number = int(temp[0])
                print(interaction_number)

                fint_w.write("   ----> Interaction part\n")
                fint_w.write("Nucleon-Nucleon interaction model: see-name\n")
                fint_w.write("Type of calculation: see-name\n")
                fint_w.write("Number and value of starting energies:   1\n")
                fint_w.write(" 0.000000E+00\n")
                fint_w.write(
                    "Total number of twobody matx elements: "
                    + str(interaction_number)
                    + " 0 0 0\n"
                )
                fint_w.write(
                    "Matrix elements with the following legend, NOTE no hbar_omega/A for Hcom, p_ip_j and r_ir_j\n"
                )
                fint_w.write(
                    "{:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}  {:>18} {:>18} {:>18} {:>18} \n".format(
                        "Tz",
                        "Par",
                        "2J",
                        "a",
                        "b",
                        "c",
                        "d",
                        "<ab|V|cd>",
                        "<ab|Hcom|cd>",
                        "<ab|r_ir_j|cd>",
                        "<ab|p_ip_j|cd>",
                    )
                )

            if h >= (orbit_number + 8):
                while "" in temp:
                    temp.remove("")
                temp_a = int(temp[0])
                temp_b = int(temp[1])
                temp_c = int(temp[2])
                temp_d = int(temp[3])
                temp_tz = int((orbit_tz(temp_a) + orbit_tz(temp_b)) / 2)
                temp_par = -1
                temp_2j = 2 * int(temp[4])
                temp_v = float(temp[5])
                fint_w.write(
                    "{:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}  {:>18} {:>18} {:>18} {:>18} \n".format(
                        str(temp_tz),
                        str(temp_par),
                        str(temp_2j),
                        str(temp_a),
                        str(temp_b),
                        str(temp_c),
                        str(temp_d),
                        "{:.6E}".format(temp_v),
                        "0.000000E+00",
                        "0.000000E+00",
                        "0.000000E+00",
                    )
                )

            h = h + 1
