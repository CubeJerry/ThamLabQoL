import sys
from math import exp

# ===================
# pKa values
# ===================
pKa = {
    "Cterm": 3.55,
    "Nterm": 8.6,
    "C": 9.0,
    "D": 4.05,
    "E": 4.45,
    "H": 5.98,
    "Cys": 8.18,
    "Tyr": 10.07,
    "Lys": 10.53,
    "Arg": 12.48
}

# ===================
# Amino acid properties
# ===================
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


# (Include your DIWV dict here exactly as you pasted — truncated above for brevity)
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




# ===================
# Functions
# ===================
def read_fasta(filename):
    """Read the first sequence from a FASTA file."""
    seq = ""
    with open(filename, "r") as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq += line.strip()
    return seq.upper()

def molecular_weight(seq):
    return sum(aa_weights[aa] for aa in seq) - (len(seq) - 1) * 18.01528

def calculate_pI(seq, epsilon=0.01):
    pKa_fixed = {"K": 10, "R": 12, "H": 5.98, "D": 4.05, "E": 4.45, "C": 9, "Y": 10.0}
    Nterm_pKa = {"A": 7.59, "M": 7.00, "S": 6.93, "P": 8.36, "T": 6.82, "V": 7.44, "Q": 7.70}
    Nterm = Nterm_pKa.get(seq[0], 7.5)
    Cterm = 3.55

    charged_counts = {aa: seq.count(aa) for aa in "KRHDECY"}
    p_list = [(pKa_fixed[aa], charged_counts[aa]) for aa in "KRH" if charged_counts[aa] > 0] + [(Nterm, 1)]
    n_list = [(pKa_fixed[aa], charged_counts[aa]) for aa in "DECY" if charged_counts[aa] > 0] + [(Cterm, 1)]

    def charge_func(ph):
        pos = sum(c / (1 + 10**(ph - pk)) for pk, c in p_list)
        neg = sum(c / (1 + 10**(pk - ph)) for pk, c in n_list)
        return pos - neg

    ph = 7.0
    step = 3.5
    last_charge = charge_func(ph)

    while abs(last_charge) >= epsilon:
        ph += step if last_charge > 0 else -step
        last_charge = charge_func(ph)
        step /= 2.0

    return round(ph, 2)

def extinction_coefficient(seq):
    return (seq.count("W") * aa_extinction["W"] + seq.count("Y") * aa_extinction["Y"] + seq.count("C") * aa_extinction["C"])/(sum(aa_weights[aa] for aa in seq) - (len(seq) - 1) * 18.01528)

def instability_index(seq):
    score = 0
    for i in range(len(seq) - 1):
        dipep = DIWV.get(seq[i], {}).get(seq[i+1], 0)
        score += dipep
    return (10.0 / len(seq)) * score

def aliphatic_index(seq):
    a, b = 2.9, 3.9
    total = len(seq)
    ai = (seq.count("A") + a * seq.count("V") + b * (seq.count("I") + seq.count("L"))) / total * 100
    return ai

def half_life(seq):
    nterm = seq[0]
    if nterm in ["A", "G", "M", "S", "T", "V"]:
        return ">30 hours (mammalian reticulocytes)"
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

# ===================
# Main
# ===================
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python protparam_like.py <FASTA_FILE>")
        sys.exit(1)

    fasta_file = sys.argv[1]
    seq = read_fasta(fasta_file)

    print(f"Sequence: {seq}")
    print(f"Molecular weight: {molecular_weight(seq):.2f} Da")
    print(f"Theoretical pI: {calculate_pI(seq)}")
    print(f"Extinction coefficient (reduced): {extinction_coefficient(seq)}")
    print(f"Instability index: {instability_index(seq):.2f}")
    print(f"Aliphatic index: {aliphatic_index(seq):.2f}")
    print(f"Estimated half-life: {half_life(seq)}")
