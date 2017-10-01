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


from indy import anoncreds, wallet

import json

import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def demo():
    logger.info("healthclaim sample -> started")

    pool_name = 'pool1'
    #change this after run or delet folder
    wallet_name = 'wallet9'

    # 1. Create My Wallet and Get Wallet Handle
    await wallet.create_wallet(pool_name, wallet_name, None, None, None)
    wallet_handle = await wallet.open_wallet(wallet_name, None, None)

    # 2. Issuer create Claim Definition for Schema
    # ROLE: Issuer of the schema, e.g. goverment or NGO
    schema = {
        'seqNo': 1,
        'data': {
            'name': 'healthrecord',
            'version': '1.0',
            'keys': ['age', 'sex', 'diseases', 'location', 'vaccinationOnRabis', 'vaccinationOnRabisDate', 'birthdate', 'name' , 'personid']
        }
    }
    schema_json = json.dumps(schema)

    claim_def_json = \
        await anoncreds.issuer_create_and_store_claim_def(wallet_handle,
                                                          'NcYxiDXkpYi6ov5FcYDi1e', schema_json, 'CL', False)

    # 3. Prover create Master Secret 
    # Role: Prover, here Refugee  (Verifier --> someone or a software agent at the border)
    await anoncreds.prover_create_master_secret(wallet_handle, 'master_secret')

    # 4. Claim offer is issued by the Issuer (Govermanent, NGO, Hospital)
    # this is so as to say 'offered by the Issuer for usage when needed'
    claim_offer_json = json.dumps({
        'issuer_did': 'NcYxiDXkpYi6ov5FcYDi1e',
        'schema_seq_no': 1
    })

    # Role: Prover (=Refugee). Refugee uses the offer from previous steo, here to ask for the claim that he was vaccinated)
    claim_req_json = await anoncreds.prover_create_and_store_claim_req(wallet_handle, 'BzfFCYk', claim_offer_json,
                                                                       claim_def_json, 'master_secret')

    # 5. Issuer create Claim for Claim Request, that is goverment or NGO hands the Claim on  request of the Refugee
    # There can be multiple claims for the same schema by multiple issuers, e.g different doctors or hospitaks
    claim_json = json.dumps({
        'age': ['52', '52'],
        'sex': ['man', '0'],
        'diseases': ['lung_condition', '23'],
        'location': ['Syria', '123123'],
        'vaccinationOnRabis': ['true', '1'],
        'vaccinationOnRabisDate': ['18', '18'],
        'birthdate': ['1.1.1980', '2'],
        'name': ['Ghadaffi', '1139481716457488690172217916278103335'],
        'personid': ['2823423432', '2823423432'],

    })

    (_, claim_json) = await anoncreds.issuer_create_claim(wallet_handle, claim_req_json, claim_json, -1)

    # 6. Prover (refugee) process and store Claim:
    # the refugee gets his claim and he can verify that the issuer was the one desired via cryptography and signatures
    # This claim with the signature is stored in a secure wallet
    # Note: we also check here that the claim was not revoked
    await anoncreds.prover_store_claim(wallet_handle, claim_json)

    # 7. A verifier (border control) creates a Prove request
    # Note that we ONLY request the vaccanition information here, we do not request the disease history
    # We even do not give the date of the vaccination (Requested attributes)rather only that the vaccination is still valid

    proof_req_json = json.dumps({
        'nonce': '123432421212',
        'name': 'proof_req_1',
        'version': '0.1',
        'requested_attrs': {
            'attr1_uuid': {'schema_seq_no': 1, 'name': 'name'}
        },
        'requested_predicates': {
            'predicate1_uuid': {'attr_name': 'vaccinationOnRabisDate', 'p_type': 'GE', 'value': 18}
        }
    })

   
    # Role: Prover (Refugee). For example one his iPhone with a wallet would show all the claims correspondin to the proof request
   # Note the refugee may have two claims fo the same matter,e.g. 2 claims for the same vaccation. He chooses, which one to share
    claim_for_proof_json = await anoncreds.prover_get_claims_for_proof_req(wallet_handle, proof_req_json)
    claims_for_proof = json.loads(claim_for_proof_json)

    claim_for_attr1 = claims_for_proof['attrs']['attr1_uuid']
    claim_uuid = claim_for_attr1[0]['claim_uuid']

    # 8. Prover (Refugee) create Proof for Proof Request, after (s)he selected the claim in his Iphone
    # Each proove may contain
       # claim_uuid: the id the refugee chose in previous step
       # self_attested_attributes: for example trivial questions like 'which dish do you love' ? which is not needed to be verified
       # requested_attrs & requested_predicates: see above !
    requested_claims_json = json.dumps({
        'self_attested_attributes': {},
        'requested_attrs': {'attr1_uuid': [claim_uuid, True]},
        'requested_predicates': {'predicate1_uuid': claim_uuid}
    })

    schemas_json = json.dumps({claim_uuid: schema})
    claim_defs_json = json.dumps({claim_uuid: json.loads(claim_def_json)})
    revoc_regs_json = json.dumps({})

    # Prover (Refugee) gets the claim from his wallet on his iPhone and has now a proof of his output
    # contains revealed attributes and cryptographic inforation so the verifier can verify the proof is correct
    proof_json = await anoncreds.prover_create_proof(wallet_handle, proof_req_json, requested_claims_json, schemas_json,
                                                     'master_secret', claim_defs_json, revoc_regs_json)
    proof = json.loads(proof_json)


    # 9. Verifier (border patrol or software agent)  verify proof
    assert await anoncreds.verifier_verify_proof(proof_req_json, proof_json, schemas_json, claim_defs_json,
                                                 revoc_regs_json)

    assert 'Ghadaffi' == proof['requested_proof']['revealed_attrs']['attr1_uuid'][1]

    # 10. Close wallet
    await wallet.close_wallet(wallet_handle)

    # 11. Delete wallet
    await wallet.delete_wallet(wallet_name, None)

    logger.info("healthclaim sample -> completed")
