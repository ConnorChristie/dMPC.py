import json
# import web3

# from web3 import Web3, HTTPProvider
# from web3.contract import ConciseContract

from .field import (
    GF,
    GF64,
)

from .sharing import (
    ShamirSharingScheme,
    PseudoRandomSecretShare,
)

from .utils.polynomials import lagrange_interpolation
from .sharing.prss import PRF

players = frozenset([GF64(1), GF64(2), GF64(3), GF64(4), GF64(5)])
prss = PseudoRandomSecretShare(players, 5, 2)
sham = ShamirSharingScheme(5, 2)

seeds = prss.generate_seeds(players, GF64)
seeds = [
    (frozenset([GF64(1), GF64(2)]), '1'),
    (frozenset([GF64(1), GF64(3)]), '2'),
    (frozenset([GF64(1), GF64(4)]), '3'),
    (frozenset([GF64(1), GF64(5)]), '4'),
    (frozenset([GF64(2), GF64(3)]), '5'),
    (frozenset([GF64(2), GF64(4)]), '6'),
    (frozenset([GF64(2), GF64(5)]), '7'),
    (frozenset([GF64(3), GF64(4)]), '8'),
    (frozenset([GF64(3), GF64(5)]), '9'),
    (frozenset([GF64(4), GF64(5)]), '10'),
]

prfs = {subset: PRF(key, GF64) for subset, key in seeds}

pts = [
    (GF64(1), prss.share(GF64(1), prfs, GF64(2))),
    (GF64(2), prss.share(GF64(2), prfs, GF64(2))),
    (GF64(3), prss.share(GF64(3), prfs, GF64(2))),
    (GF64(4), prss.share(GF64(4), prfs, GF64(2))),
    (GF64(5), prss.share(GF64(5), prfs, GF64(2)))
]

zeros = [
    (GF64(1), prss.zero_share(GF64(1), prfs, GF64(2), 1)),
    (GF64(2), prss.zero_share(GF64(2), prfs, GF64(2), 1)),
    (GF64(3), prss.zero_share(GF64(3), prfs, GF64(2), 1)),
    (GF64(4), prss.zero_share(GF64(4), prfs, GF64(2), 1)),
    (GF64(5), prss.zero_share(GF64(5), prfs, GF64(2), 1))
]


orig = sham.share(GF64(123))

nee = [
    (GF64(1), orig[0][1] + zeros[0][1]),
    (GF64(2), orig[1][1] + zeros[1][1]),
    (GF64(3), orig[2][1] + zeros[2][1]),
    (GF64(4), orig[3][1] + zeros[3][1]),
    (GF64(5), orig[4][1] + zeros[4][1]),
]

print("mod", sham.recombine(zeros))
print("orig", sham.recombine(orig))
print("nee", sham.recombine(nee))

# contract_interface = json.load(open('./export/development.json'))['MPC']

# w3 = Web3(HTTPProvider('http://localhost:8545'))
# contract = w3.eth.contract(abi=contract_interface['abi'], address=contract_interface['address'], ContractFactoryClass=ConciseContract)

print("\nother")
num_shares = 3
threshold = 1
secret = 15

scheme = ShamirSharingScheme(num_shares, threshold)
shares = scheme.share(GF64(secret))

old_ids = [GF64(1), GF64(2), GF64(3)]
new_ids = [GF64(13), GF64(12), GF64(11)]
old_new_shares = {share[0]: dict(scheme.reshare(share, new_ids)) for share in shares}

all_new = []

for new_id in new_ids:
    interpol_arr = []

    for id in old_ids:
        interpol_arr.append((id, old_new_shares[id][new_id]))

    all_new.append((new_id, lagrange_interpolation(new_id, interpol_arr)))



# hehehe = [
#     (GF64(15), lagrange_interpolation(15, [
#         (GF64(1), new_shares1[15]),
#         (GF64(2), new_shares2[15]),
#         (GF64(3), new_shares3[15]),
#         (GF64(4), new_shares4[15]),
#         (GF64(5), new_shares5[15])
#     ])),
#     (GF64(14), lagrange_interpolation(14, [
#         (GF64(1), new_shares1[14]),
#         (GF64(2), new_shares2[14]),
#         (GF64(3), new_shares3[14]),
#         (GF64(4), new_shares4[14]),
#         (GF64(5), new_shares5[14])
#     ])),
#     (GF64(13), lagrange_interpolation(13, [
#         (GF64(1), new_shares1[13]),
#         (GF64(2), new_shares2[13]),
#         (GF64(3), new_shares3[13]),
#         (GF64(4), new_shares4[13]),
#         (GF64(5), new_shares5[13])
#     ])),
#     (GF64(12), lagrange_interpolation(12, [
#         (GF64(1), new_shares1[12]),
#         (GF64(2), new_shares2[12]),
#         (GF64(3), new_shares3[12]),
#         (GF64(4), new_shares4[12]),
#         (GF64(5), new_shares5[12])
#     ])),
#     (GF64(11), lagrange_interpolation(11, [
#         (GF64(1), new_shares1[11]),
#         (GF64(2), new_shares2[11]),
#         (GF64(3), new_shares3[11]),
#         (GF64(4), new_shares4[11]),
#         (GF64(5), new_shares5[11])
#     ]))
# ]

# print(scheme.recombine(shares))

# print(shares)
# print(all_new)

print("sup", scheme.recombine(all_new))
