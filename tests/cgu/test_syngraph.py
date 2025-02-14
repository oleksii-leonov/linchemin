import json

import pytest

from linchemin.cgu.syngraph import (BipartiteSynGraph, MonopartiteMolSynGraph,
                                    MonopartiteReacSynGraph,
                                    extract_reactions_from_syngraph,
                                    merge_syngraph)
from linchemin.cgu.translate import translator
from linchemin.cheminfo.constructors import (ChemicalEquationConstructor,
                                             MoleculeConstructor)


def test_bipartite_syngraph_instance(az_path):
    """ To test that a BipartiteSynGraph instance is correctly generated. """
    syngraph = BipartiteSynGraph()
    assert len(syngraph.graph.keys()) == 0 and len(syngraph.graph.values()) == 0

    graph = json.loads(open(az_path).read())
    syngraph = translator('az_retro', graph[0], 'syngraph', out_data_model='bipartite')
    assert len(syngraph.graph.keys()) != 0 and len(syngraph.graph.values()) != 0
    assert syngraph.source is not None
    assert len(syngraph.get_roots()) == 1
    assert len(syngraph.get_leaves()) != 0

    syngraph2 = translator('az_retro', graph[0], 'syngraph', out_data_model='bipartite')
    syngraph3 = translator('az_retro', graph[1], 'syngraph', out_data_model='bipartite')
    assert syngraph == syngraph2
    assert syngraph3 != syngraph2


def test_add_new_node(ibm1_path):
    """ To test that the SynGraph method 'add_node' correctly add new nodes to a SynGraph instance. """
    graph = json.loads(open(ibm1_path).read())
    syngraph = translator('ibm_retro', graph[0], 'syngraph', out_data_model='bipartite')
    l1 = len(syngraph.graph)
    new_node = ('new_mol_smiles', ['new>reaction>smiles1', 'new>reaction>smiles2'])
    syngraph.add_node(new_node)
    l2 = len(syngraph.graph)
    assert 'new_mol_smiles' in syngraph.graph.keys()
    assert l1 != l2


def test_add_existing_node(ibm1_path):
    """ To test that if an already existing node is added to a SynGraph instance, the node is not duplicated. """
    graph = json.loads(open(ibm1_path).read())
    syngraph1 = translator('ibm_retro', graph[0], 'syngraph', out_data_model='bipartite')
    l1 = len(syngraph1.graph)
    molecule_constructor = MoleculeConstructor(molecular_identity_property_name='smiles')

    reactant = molecule_constructor.build_from_molecule_string(molecule_string='CCN',
                                                               inp_fmt='smiles')

    chemical_equation_constructor = ChemicalEquationConstructor(molecular_identity_property_name='smiles',
                                                                chemical_equation_identity_name='r_r_p')
    chemical_equation = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='CCN>>CCC(=O)NCC',
        inp_fmt='smiles')
    reaction = chemical_equation

    existing_node = (reactant, [reaction])
    syngraph1.add_node(existing_node)
    l2 = len(syngraph1.graph)
    assert l1 == l2


def test_add_existing_node_with_new_connections(ibm1_path):
    """ To test that new connections for an existing node are correctly added, without duplicates. """
    graph = json.loads(open(ibm1_path).read())
    syngraph = translator('ibm_retro', graph[0], 'syngraph', out_data_model='bipartite')
    l1 = len(syngraph.graph)

    molecule_constructor = MoleculeConstructor(molecular_identity_property_name='smiles')

    reactant = molecule_constructor.build_from_molecule_string(molecule_string='CCN',
                                                               inp_fmt='smiles')

    chemical_equation_constructor = ChemicalEquationConstructor(molecular_identity_property_name='smiles',
                                                                chemical_equation_identity_name='r_r_p')
    chemical_equation = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='CCN>>CCC(=O)NCC',
        inp_fmt='smiles')
    reaction = chemical_equation

    node = (reactant, [reaction, 'C1CCOC1.CCOC(=O)CC.CCN>>CCC(=O)NCC'])
    syngraph.add_node(node)

    l2 = len(syngraph.graph)
    assert l1 == l2
    assert 'C1CCOC1.CCOC(=O)CC.CCN>>CCC(=O)NCC' in syngraph[reactant]


def test_syngraph_source(az_path):
    """ To test that the source attribute of a SynGraph instance is correctly assigned. """
    graph_az = json.loads(open(az_path).read())
    syngraph = translator('az_retro', graph_az[1], 'syngraph', out_data_model='bipartite')

    assert 'az' in syngraph.source


def test_syngraph_merging(ibm1_path, az_path):
    """ To test that a list of Syngraph/MonopartiteSynGraph objects is correctly merged. """
    graph_ibm = json.loads(open(ibm1_path).read())
    all_routes_ibm = [translator('ibm_retro', g, 'syngraph', out_data_model='bipartite') for g in graph_ibm]

    graph_az = json.loads(open(az_path).read())
    all_routes_az = [translator('az_retro', g, 'syngraph', out_data_model='bipartite') for g in graph_az]

    synroutes = list(all_routes_ibm)
    synroutes.extend(iter(all_routes_az))
    # SynGraph instances generated by different CASPs can be merged
    merged = merge_syngraph(synroutes)
    assert type(merged) == BipartiteSynGraph

    roots = merged.get_roots()
    roots_smiles = [mol.smiles for mol in roots]
    assert roots_smiles == ['CCNC(=O)CC', 'Cc1cccc(C)c1N(CC(=O)Nc1ccc(-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1']
    leaves = merged.get_leaves()
    assert [mol.smiles for mol in leaves] == ['CCN', 'CCOC(=O)CC', 'CCO', 'C1CCOC1', 'CCC(=O)Cl', 'ClCCl', 'O',
                                              'CCOC(C)=O', 'CCC(=O)O', 'CCC(=O)OC(=O)CC', 'O=C(O)C1CCS(=O)(=O)CC1',
                                              'Nc1ccc(-c2ncon2)cc1', 'Cc1cccc(C)c1NCC(=O)O', 'CCOC(=O)CNc1c(C)cccc1C',
                                              'O=C(Cl)C1CCS(=O)(=O)CC1', 'Cc1cccc(C)c1N', 'O=C(Br)CBr']

    # MonopartiteSynGraph instances can be merged
    mp_syngraphs = [translator('az_retro', g, 'syngraph', out_data_model='monopartite_reactions') for g in graph_az]

    merged_mp_syngraph = merge_syngraph(mp_syngraphs)
    assert type(merged_mp_syngraph) == MonopartiteReacSynGraph and len(merged_mp_syngraph.graph) == 11

    # An error is raised if the input routes are in the wrong format
    with pytest.raises(TypeError) as te:
        all_routes = [translator('ibm_retro', g, 'networkx', out_data_model='bipartite') for g in graph_ibm]
        merge_syngraph(all_routes)
    assert "TypeError" in str(te.type)

    mixed_type = all_routes_ibm.extend(iter(mp_syngraphs))
    # An error is raised if the input routes have mixed formats
    with pytest.raises(TypeError) as te:
        merge_syngraph(mixed_type)
    assert "TypeError" in str(te.type)


def test_monopartite_syngraph(ibm1_path):
    """ To test that a MonopartiteMolSynGraph object is correctly generated """
    graph_ibm = json.loads(open(ibm1_path).read())
    mp_syngraph = translator('ibm_retro', graph_ibm[5], 'syngraph', out_data_model='monopartite_molecules')

    molecule_constructor = MoleculeConstructor(molecular_identity_property_name='smiles')
    mol1 = molecule_constructor.build_from_molecule_string(molecule_string='CCC(=O)Cl', inp_fmt='smiles')
    mol2 = molecule_constructor.build_from_molecule_string(molecule_string='CCNC(=O)CC', inp_fmt='smiles')

    assert mol1 in mp_syngraph.get_leaves()
    assert mol2 in mp_syngraph.get_roots()


def test_reaction_monopartite(az_path):
    graph_az = json.loads(open(az_path).read())
    mp_reac_syngraph = translator('az_retro', graph_az[0], 'syngraph', out_data_model='monopartite_reactions')

    chemical_equation_constructor = ChemicalEquationConstructor(molecular_identity_property_name='smiles',
                                                                chemical_equation_identity_name='r_r_p')
    ce_root = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1.O=C('
                        'O)C1CCS(=O)(=O)CC1>>Cc1cccc(C)c1N(CC(=O)Nc1ccc('
                        '-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1',
        inp_fmt='smiles')
    assert ce_root in mp_reac_syngraph.get_roots()
    mol_roots = mp_reac_syngraph.get_molecule_roots()
    assert 'Cc1cccc(C)c1N(CC(=O)Nc1ccc(-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1' in [m.smiles for m in mol_roots]
    mol_leaves = mp_reac_syngraph.get_molecule_leaves()
    leaves_smiles = ['O=C(O)C1CCS(=O)(=O)CC1', 'Cc1cccc(C)c1NCC(=O)O', 'Nc1ccc(-c2ncon2)cc1']
    assert [m.smiles for m in mol_leaves] == leaves_smiles


def test_get_reaction_leaves(az_path):
    """ To test the MonopartiteReacSynGraph method 'get_leaves' correctly identifies the leaves (ReactionStep)
            in the graph. """
    graph = json.loads(open(az_path).read())
    syngraphs = [translator('az_retro', g, 'syngraph', out_data_model='bipartite') for g in graph]
    tree = merge_syngraph(syngraphs)
    mol_roots = tree.get_roots()

    mp_syngraphs = [translator('az_retro', g, 'syngraph', out_data_model='monopartite_reactions') for g in graph]
    mp_tree = merge_syngraph(mp_syngraphs)
    reac_roots = mp_tree.get_roots()
    target = []
    for root in reac_roots:
        prod = root.smiles.split('>>')[-1]
        if prod not in target:
            target.append(prod)
    assert target[0] == mol_roots[0].smiles

    reac_leaves = mp_tree.get_leaves()
    assert len(reac_leaves) == 4


def test_extract_reactions(az_path):
    graph_az = json.loads(open(az_path).read())
    syngraph = translator('az_retro', graph_az[0], 'syngraph', 'monopartite_reactions')
    reactions = extract_reactions_from_syngraph(syngraph)
    assert len(reactions) == 2
    assert reactions[1]['input_string'] == 'Cc1cccc(C)c1NCC(=O)O.Nc1ccc(-c2ncon2)cc1>>Cc1cccc(C)c1NCC(=O)Nc1ccc(' \
                                              '-c2ncon2)cc1'

    syngraph = translator('az_retro', graph_az[0], 'syngraph', out_data_model='bipartite')
    reactions2 = extract_reactions_from_syngraph(syngraph)
    assert reactions == reactions2

    mpm_syngraph = translator('az_retro', graph_az[0], 'syngraph', out_data_model='monopartite_molecules')
    reactions3 = extract_reactions_from_syngraph(mpm_syngraph)
    assert reactions3 == reactions2

    with pytest.raises(TypeError) as te:
        extract_reactions_from_syngraph(['list'])
    assert "TypeError" in str(te.type)


def test_read_dictionary(az_path, ibm1_path):
    # monopartite reactions
    d = [
        {'query_id': 0, 'output_string': 'Cc1cccc(C)c1NCC(=O)O.Nc1ccc(-c2ncon2)cc1>>Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1'},
        {'query_id': 1, 'output_string': 'Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1.O=C(O)C1CCS(=O)(=O)CC1>>Cc1cccc(C)c1N(CC('
                                     '=O)Nc1ccc(-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1'}]
    syngraph = MonopartiteReacSynGraph(d)
    graph_az = json.loads(open(az_path).read())
    assert syngraph == translator('az_retro', graph_az[0], 'syngraph', 'monopartite_reactions')

    # bipartite
    d2 = [{'query_id': 0, 'output_string': 'CCC(=O)Cl.CCN>>CCNC(=O)CC'}]
    graph_ibm = json.loads(open(ibm1_path).read())
    syngraph = BipartiteSynGraph(d2)
    assert syngraph == translator('ibm_retro', graph_ibm[3], 'syngraph', 'bipartite')

    # monopartite molecules
    d3 = [{'query_id': 0, 'output_string': 'CCC(=O)Cl.CCN.ClCCl>>CCNC(=O)CC'}]
    mom_syngraph = MonopartiteMolSynGraph(d3)
    assert mom_syngraph == translator('ibm_retro', graph_ibm[4], 'syngraph', 'monopartite_molecules')


def test_hashing(ibm2_path):
    graph = json.loads(open(ibm2_path).read())
    syngraph_mpr = translator('ibm_retro', graph[0], 'syngraph', 'monopartite_reactions')
    # The hash key is created
    assert syngraph_mpr.uid
    uid1 = syngraph_mpr.uid
    chemical_equation_constructor = ChemicalEquationConstructor(molecular_identity_property_name='smiles',
                                                                chemical_equation_identity_name='r_r_p')
    ce = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1.O=C('
                        'O)C1CCS(=O)(=O)CC1>>Cc1cccc(C)c1N(CC(=O)Nc1ccc('
                        '-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1',
        inp_fmt='smiles')
    # If the SynGraph instance changes, the hash key is also modified
    syngraph_mpr.add_node((ce, []))
    assert syngraph_mpr.uid != uid1
    #prefixes of the uid indicate the type of SynGraph
    assert syngraph_mpr.uid[:3] == 'MPR'

    syngraph_mpm = translator('ibm_retro', graph[0], 'syngraph', 'monopartite_molecules')
    assert syngraph_mpm.uid[:3] == 'MPM'

    syngraph_mpm = translator('ibm_retro', graph[0], 'syngraph', 'bipartite')
    assert syngraph_mpm.uid[:2] == 'BP'
