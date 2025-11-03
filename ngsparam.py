import sys
import csv
from math import exp



# Fixed pKa values for sidechains
pKa_fixed = {"K": 10.0, "R": 12.0, "H": 5.98, "D": 4.05, "E": 4.45, "C": 9.0, "Y": 10.0}
# Approx. N-terminal pKa depending on residue
Nterm_pKa = {"A": 7.59, "M": 7.0, "S": 6.93, "P": 8.36, "T": 6.82, "V": 7.44, "E": 7.70}
# C-terminal default pKa
Cterm_default = 3.55
# C-terminal corrections for D/E
pK_cterm = {"D": 4.55, "E": 4.75}

aa_weights = {
    "A": 89.0932, "R": 174.201, "N": 132.1179, "D": 133.1027,
    "C": 121.1582, "E": 147.1293, "Q": 146.1445, "G": 75.0666,
    "H": 155.1546, "I": 131.1729, "L": 131.1729, "K": 146.1876,
    "M": 149.2113, "F": 165.1891, "P": 115.1305, "S": 105.0926,
    "T": 119.1192, "W": 204.2252, "Y": 181.1885, "V": 117.1463
}

aa_extinction = {
    "W": 5500,
    "Y": 1490,
    "C": 125
}

aa_volume = {
    "A": 88.6, "R": 173.4, "N": 114.1, "D": 111.1, "C": 108.5, "E": 138.4,
    "Q": 143.8, "G": 60.1, "H": 153.2, "I": 166.7, "L": 166.7, "K": 168.6,
    "M": 162.9, "F": 189.9, "P": 112.7, "S": 89.0, "T": 116.1, "W": 227.8,
    "Y": 193.6, "V": 140.0
}

aa_ai = {"A": 71.09, "V": 99.07, "I": 100.00, "L": 97.00, "F": 100.00, "C": 50.00, "M": 60.00}

# ===================
# DIWV (Instability Index) from Biopython
# ===================

DIWV = {'A': {'A': 1.0, 'C': 44.94, 'E': 1.0, 'D': -7.49,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': -7.49,
              'K': 1.0, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 1.0, 'P': 20.26, 'S': 1.0, 'R': 1.0,
              'T': 1.0, 'W': 1.0, 'V': 1.0, 'Y': 1.0},
        'C': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 20.26,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': 33.60,
              'K': 1.0, 'M': 33.60, 'L': 20.26, 'N': 1.0,
              'Q': -6.54, 'P': 20.26, 'S': 1.0, 'R': 1.0,
              'T': 33.60, 'W': 24.68, 'V': -6.54, 'Y': 1.0},
        'E': {'A': 1.0, 'C': 44.94, 'E': 33.60, 'D': 20.26,
              'G': 1.0, 'F': 1.0, 'I': 20.26, 'H': -6.54,
              'K': 1.0, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 20.26, 'P': 20.26, 'S': 20.26, 'R': 1.0,
              'T': 1.0, 'W': -14.03, 'V': 1.0, 'Y': 1.0},
        'D': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': 1.0, 'F': -6.54, 'I': 1.0, 'H': 1.0,
              'K': -7.49, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 1.0, 'P': 1.0, 'S': 20.26, 'R': -6.54,
              'T': -14.03, 'W': 1.0, 'V': 1.0, 'Y': 1.0},
        'G': {'A': -7.49, 'C': 1.0, 'E': -6.54, 'D': 1.0,
              'G': 13.34, 'F': 1.0, 'I': -7.49, 'H': 1.0,
              'K': -7.49, 'M': 1.0, 'L': 1.0, 'N': -7.49,
              'Q': 1.0, 'P': 1.0, 'S': 1.0, 'R': 1.0,
              'T': -7.49, 'W': 13.34, 'V': 1.0, 'Y': -7.49},
        'F': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 13.34,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': 1.0,
              'K': -14.03, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 1.0, 'P': 20.26, 'S': 1.0, 'R': 1.0,
              'T': 1.0, 'W': 1.0, 'V': 1.0, 'Y': 33.601},
        'I': {'A': 1.0, 'C': 1.0, 'E': 44.94, 'D': 1.0,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': 13.34,
              'K': -7.49, 'M': 1.0, 'L': 20.26, 'N': 1.0,
              'Q': 1.0, 'P': -1.88, 'S': 1.0, 'R': 1.0,
              'T': 1.0, 'W': 1.0, 'V': -7.49, 'Y': 1.0},
        'H': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': -9.37, 'F': -9.37, 'I': 44.94, 'H': 1.0,
              'K': 24.68, 'M': 1.0, 'L': 1.0, 'N': 24.68,
              'Q': 1.0, 'P': -1.88, 'S': 1.0, 'R': 1.0,
              'T': -6.54, 'W': -1.88, 'V': 1.0, 'Y': 44.94},
        'K': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': -7.49, 'F': 1.0, 'I': -7.49, 'H': 1.0,
              'K': 1.0, 'M': 33.60, 'L': -7.49, 'N': 1.0,
              'Q': 24.64, 'P': -6.54, 'S': 1.0, 'R': 33.60,
              'T': 1.0, 'W': 1.0, 'V': -7.49, 'Y': 1.0},
        'M': {'A': 13.34, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': 58.28,
              'K': 1.0, 'M': -1.88, 'L': 1.0, 'N': 1.0,
              'Q': -6.54, 'P': 44.94, 'S': 44.94, 'R': -6.54,
              'T': -1.88, 'W': 1.0, 'V': 1.0, 'Y': 24.68},
        'L': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': 1.0,
              'K': -7.49, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 33.60, 'P': 20.26, 'S': 1.0, 'R': 20.26,
              'T': 1.0, 'W': 24.68, 'V': 1.0, 'Y': 1.0},
        'N': {'A': 1.0, 'C': -1.88, 'E': 1.0, 'D': 1.0,
              'G': -14.03, 'F': -14.03, 'I': 44.94, 'H': 1.0,
              'K': 24.68, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': -6.54, 'P': -1.88, 'S': 1.0, 'R': 1.0,
              'T': -7.49, 'W': -9.37, 'V': 1.0, 'Y': 1.0},
        'Q': {'A': 1.0, 'C': -6.54, 'E': 20.26, 'D': 20.26,
              'G': 1.0, 'F': -6.54, 'I': 1.0, 'H': 1.0,
              'K': 1.0, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 20.26, 'P': 20.26, 'S': 44.94, 'R': 1.0,
              'T': 1.0, 'W': 1.0, 'V': -6.54, 'Y': -6.54},
        'P': {'A': 20.26, 'C': -6.54, 'E': 18.38, 'D': -6.54,
              'G': 1.0, 'F': 20.26, 'I': 1.0, 'H': 1.0,
              'K': 1.0, 'M': -6.54, 'L': 1.0, 'N': 1.0,
              'Q': 20.26, 'P': 20.26, 'S': 20.26, 'R': -6.54,
              'T': 1.0, 'W': -1.88, 'V': 20.26, 'Y': 1.0},
        'S': {'A': 1.0, 'C': 33.60, 'E': 20.26, 'D': 1.0,
              'G': 1.0, 'F': 1.0, 'I': 1.0, 'H': 1.0,
              'K': 1.0, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 20.26, 'P': 44.94, 'S': 20.26, 'R': 20.26,
              'T': 1.0, 'W': 1.0, 'V': 1.0, 'Y': 1.0},
        'R': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': -7.49, 'F': 1.0, 'I': 1.0, 'H': 20.26,
              'K': 1.0, 'M': 1.0, 'L': 1.0, 'N': 13.34,
              'Q': 20.26, 'P': 20.26, 'S': 44.94, 'R': 58.28,
              'T': 1.0, 'W': 58.28, 'V': 1.0, 'Y': -6.54},
        'T': {'A': 1.0, 'C': 1.0, 'E': 20.26, 'D': 1.0,
              'G': -7.49, 'F': 13.34, 'I': 1.0, 'H': 1.0,
              'K': 1.0, 'M': 1.0, 'L': 1.0, 'N': -14.03,
              'Q': -6.54, 'P': 1.0, 'S': 1.0, 'R': 1.0,
              'T': 1.0, 'W': -14.03, 'V': 1.0, 'Y': 1.0},
        'W': {'A': -14.03, 'C': 1.0, 'E': 1.0, 'D': 1.0,
              'G': -9.37, 'F': 1.0, 'I': 1.0, 'H': 24.68,
              'K': 1.0, 'M': 24.68, 'L': 13.34, 'N': 13.34,
              'Q': 1.0, 'P': 1.0, 'S': 1.0, 'R': 1.0,
              'T': -14.03, 'W': 1.0, 'V': -7.49, 'Y': 1.0},
        'V': {'A': 1.0, 'C': 1.0, 'E': 1.0, 'D': -14.03,
              'G': -7.49, 'F': 1.0, 'I': 1.0, 'H': 1.0,
              'K': -1.88, 'M': 1.0, 'L': 1.0, 'N': 1.0,
              'Q': 1.0, 'P': 20.26, 'S': 1.0, 'R': 1.0,
              'T': -7.49, 'W': 1.0, 'V': 1.0, 'Y': -6.54},
        'Y': {'A': 24.68, 'C': 1.0, 'E': -6.54, 'D': 24.68,
              'G': -7.49, 'F': 1.0, 'I': 1.0, 'H': 13.34,
              'K': 1.0, 'M': 44.94, 'L': 1.0, 'N': 1.0,
              'Q': 1.0, 'P': 13.34, 'S': 1.0, 'R': -15.91,
              'T': -7.49, 'W': -9.37, 'V': 1.0, 'Y': 13.34},
        }

def read_fasta_multiseq(filename):
    """Read a multi-sequence FASTA and return dict {header: sequence}."""
    sequences = {}
    header = None
    seq = ""
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header and seq:
                    sequences[header] = seq.upper()
                header = line[1:].split()[0]
                seq = ""
            else:
                seq += line
        if header and seq:
            sequences[header] = seq.upper()
    return sequences

def molecular_weight(seq):
    return sum(aa_weights[aa] for aa in seq) - (len(seq) - 1) * 18.01528

def calculate_pI(seq, epsilon=0.0001):
    seq = seq.upper()
    Nterm = Nterm_pKa.get(seq[0], 7.5)
    last = seq[-1]
    Cterm = pK_cterm.get(last, Cterm_default)

    # Count charged residues
    counts = {aa: seq.count(aa) for aa in "KRHDECY"}
    # Avoid double-counting C-terminal D/E
    if last in ["D", "E"]:
        counts[last] = max(0, counts[last]-1)

    # Positive: K, R, H + Nterm
    pos_groups = [(pKa_fixed[aa], counts[aa]) for aa in "KRH" if counts[aa] > 0]
    pos_groups.append((Nterm, 1))
    # Negative: D, E, C, Y + Cterm
    neg_groups = [(pKa_fixed[aa], counts[aa]) for aa in "DECY" if counts[aa] > 0]
    neg_groups.append((Cterm, 1))

    def net_charge(ph):
        pos = sum(c / (1 + 10**(ph - pk)) for pk, c in pos_groups)
        neg = sum(c / (1 + 10**(pk - ph)) for pk, c in neg_groups)
        return pos - neg

    def bisect(low, high):
        mid = (low + high)/2
        charge = net_charge(mid)
        if high - low < epsilon:
            return mid
        if charge > 0:
            return bisect(mid, high)
        else:
            return bisect(low, mid)

    return round(bisect(4.0, 12.0), 2)


def extinction_coefficient(seq):
    return (seq.count("W") * aa_extinction["W"] + seq.count("Y") * aa_extinction["Y"] + seq.count("C") * aa_extinction["C"]) / (sum(aa_weights[aa] for aa in seq) - (len(seq) - 1) * 18.01528)

def instability_index(seq):
    score = 0
    for i in range(len(seq) - 1):
        score += DIWV.get(seq[i], {}).get(seq[i+1], 0)
    return (10.0 / len(seq)) * score

def aliphatic_index(seq):
    a, b = 2.9, 3.9
    total = len(seq)
    ai = (seq.count("A") + a * seq.count("V") + b * (seq.count("I") + seq.count("L"))) / total * 100
    return ai

def half_life(seq):
    nterm = seq[0]
    if nterm in ["A", "G", "M", "S", "T", "V"]:
        return ">30 hours"
    elif nterm in ["I", "L", "N", "Q", "C"]:
        return "10 hours"
    elif nterm in ["R", "K", "H"]:
        return "2 minutes"
    elif nterm in ["F", "Y", "W"]:
        return "2 minutes"
    elif nterm in ["D", "E"]:
        return "3 minutes"
    else:
        return "Unknown"

if len(sys.argv) != 2:
    print("Usage: python protparam_csv.py <input_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = input_csv.rsplit(".", 1)[0] + "_params.csv"

with open(input_csv, newline='') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["sequence_alignment_aa_mod", "Length", "MW", "pI",
                                      "Extinction_Coefficient", "Instability_Index",
                                      "Aliphatic_Index", "Half_life"]

    with open(output_csv, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            seq = row["sequence_alignment_aa"] + "VSS"
            row["sequence_alignment_aa_mod"] = seq
            row["Length"] = len(seq)
            row["MW"] = round(molecular_weight(seq), 2)
            row["pI"] = calculate_pI(seq)
            row["Extinction_Coefficient"] = round(extinction_coefficient(seq), 2)
            row["Instability_Index"] = round(instability_index(seq), 2)
            row["Aliphatic_Index"] = round(aliphatic_index(seq), 2)
            row["Half_life"] = half_life(seq)

            writer.writerow(row)

print(f"Processed CSV saved as {output_csv}")
