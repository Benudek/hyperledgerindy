# hyperledgerindy
hyperledger indy distrubuted identity management

# Hackathon Dublin: Decentralised Identity
#                           Sharing of health records
#
# Scenario:
# This code implements a scenario where a refugee arrives into a country seeking asylum and the border patrol
# asks him to verify he made an important vaccanition recent enough to be valid.
#
# The refugee can proove this get access without sharing any other medical information than
#   (s)he made the rabies vaccination
#   the vaccination is still valid
# The refugee could use his smartphone to initiate the process and show records
# The refugee will not need to rely on the goverment of his home country
# The refugee will not need an online connection to the party testfying that he did the vaccination

# Roles in this scenario are:

# Prover: the person to proove a claim
#         Controls a wallet, a secret store the prover holds to control and access claims

# Issuer: the organisation which validates a claim of the Prover
#         can be goverment bodies, NGOs, hospitals or doctors

# Schema Definition Provider:   An Organisation, which provides Data formats for e.g. health data
#                               Typically, but necessarily this is a goverment body

# A Verifier is the party to which the proover presents the proove.
#     This could be a person like in our person the border or a software agent

# Claims are
#     Statements about the Identity of the Prover,
#     controlled by the Provers wallet.
#     operate on top of Data defined in Schemas
#     consist of 2 parts:
#         the data itself (e.g. being above a certain age)
#         a data structure to handle revocations, e.g. a revoked driver license for drunk driving


# The Solution is implemented on top of Hyperlederg indy and Sovereign.
# Among other features this decentralised Identity Management will allow persons
#      Define their Identity in different Relations from them to Issuer(s)
#      Hence, separate parts of their identities such that no central entity knows all of them
#      to not store personal identifiable data on the Blockchain,
#         even if the cryptographty was broken only parts of the Identity not tied to a person are visible
#      Generate claims over them, which are verified by Issuers, even though Issuers might not be reachable,
#         this is possible by storing the Keys on the Ledger, which is always accessible

# The Solution Scenario Implemented could be transferred to a person, which has to conduct a lot of doctors visits, like e.g.
# a pregnant woman and wants a way to share her healthdata in a very efficient and secure manner

#The solution was tested from a local macintosh with a testnetwork running on docker
