from linchemin.cgu.syngraph import (BipartiteSynGraph, MonopartiteReacSynGraph, MonopartiteMolSynGraph, merge_syngraph,
                                    extract_reactions_from_syngraph)
from linchemin.cgu.translate import translator
from linchemin.cheminfo.reaction import ChemicalEquation, ChemicalEquationConstructor
from linchemin.cheminfo.molecule import Molecule, MoleculeConstructor
import json
import pytest


def test_bipartite_syngraph_instance():
    """ To test that a BipartiteSynGraph instance is correctly generated. """
    syngraph = BipartiteSynGraph()
    assert len(syngraph.graph.keys()) == 0 and len(syngraph.graph.values()) == 0

    graph = json.loads(open("data/az_retro_output_raw.json").read())
    syngraph = translator('az_retro', graph[0], 'syngraph', out_data_model='bipartite')
    assert len(syngraph.graph.keys()) != 0 and len(syngraph.graph.values()) != 0
    assert syngraph.source is not None
    assert len(syngraph.get_roots()) == 1
    assert len(syngraph.get_leaves()) != 0

    syngraph2 = translator('az_retro', graph[0], 'syngraph', out_data_model='bipartite')
    syngraph3 = translator('az_retro', graph[1], 'syngraph', out_data_model='bipartite')
    assert syngraph == syngraph2
    assert syngraph3 != syngraph2


def test_add_new_node():
    """ To test that the SynGraph method 'add_node' correctly add new nodes to a SynGraph instance. """
    graph = json.loads(open("data/ibmrxn_retro_output_raw.json").read())
    syngraph = translator('ibm_retro', graph[0], 'syngraph', out_data_model='bipartite')
    l1 = len(syngraph.graph)
    new_node = ('new_mol_smiles', ['new>reaction>smiles1', 'new>reaction>smiles2'])
    syngraph.add_node(new_node)
    l2 = len(syngraph.graph)
    assert 'new_mol_smiles' in syngraph.graph.keys()
    assert l1 != l2


def test_add_existing_node():
    """ To test that if an already existing node is added to a SynGraph instance, the node is not duplicated. """
    graph = json.loads(open("data/ibmrxn_retro_output_raw.json").read())
    syngraph1 = translator('ibm_retro', graph[0], 'syngraph', out_data_model='bipartite')
    l1 = len(syngraph1.graph)
    """
    
    reactant = Molecule('CCN', inp_fmt='smiles', identity_property_name='smiles')
    molecules, roles, rdrxn = process_reaction_string(input_string='CCN>>CCC(=O)NCC', inp_fmt='smiles',
                                                      identity_property_name='smiles')
    reaction = ChemicalEquation(molecules=molecules, roles=roles)
    """
    molecule_constructor = MoleculeConstructor(identity_property_name='smiles')

    reactant = molecule_constructor.build_from_molecule_string(molecule_string='CCN',
                                                               inp_fmt='smiles')

    chemical_equation_constructor = ChemicalEquationConstructor(identity_property_name='smiles')
    chemical_equation = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='CCN>>CCC(=O)NCC',
        inp_fmt='smiles')
    reaction = chemical_equation

    existing_node = (reactant, [reaction])
    syngraph1.add_node(existing_node)
    l2 = len(syngraph1.graph)
    assert l1 == l2


def test_add_existing_node_with_new_connections():
    """ To test that new connections for an existing node are correctly added, without duplicates. """
    graph = json.loads(open("data/ibmrxn_retro_output_raw.json").read())
    syngraph = translator('ibm_retro', graph[0], 'syngraph', out_data_model='bipartite')
    l1 = len(syngraph.graph)

    molecule_constructor = MoleculeConstructor(identity_property_name='smiles')

    reactant = molecule_constructor.build_from_molecule_string(molecule_string='CCN',
                                                               inp_fmt='smiles')

    chemical_equation_constructor = ChemicalEquationConstructor(identity_property_name='smiles')
    chemical_equation = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='CCN>>CCC(=O)NCC',
        inp_fmt='smiles')
    reaction = chemical_equation

    node = (reactant, [reaction, 'C1CCOC1.CCOC(=O)CC.CCN>>CCC(=O)NCC'])
    syngraph.add_node(node)

    l2 = len(syngraph.graph)
    assert l1 == l2
    assert 'C1CCOC1.CCOC(=O)CC.CCN>>CCC(=O)NCC' in syngraph[reactant]


def test_syngraph_source():
    """ To test that the source attribute of a SynGraph instance is correctly assigned. """
    graph_az = json.loads(open("data/az_retro_output_raw.json").read())
    syngraph = translator('az_retro', graph_az[1], 'syngraph', out_data_model='bipartite')

    assert 'az' in syngraph.source


def test_syngraph_merging():
    """ To test that a list of Syngraph/MonopartiteSynGraph objects is correctly merged. """
    graph_ibm = json.loads(open("data/ibmrxn_retro_output_raw.json").read())
    all_routes_ibm = [translator('ibm_retro', g, 'syngraph', out_data_model='bipartite') for g in graph_ibm]

    graph_az = json.loads(open("data/az_retro_output_raw.json").read())
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


def test_monopartite_syngraph():
    """ To test that a MonopartiteMolSynGraph object is correctly generated """
    graph_ibm = json.loads(open("data/ibmrxn_retro_output_raw.json").read())
    mp_syngraph = translator('ibm_retro', graph_ibm[5], 'syngraph', out_data_model='monopartite_molecules')

    molecule_constructor = MoleculeConstructor(identity_property_name='smiles')
    mol1 = molecule_constructor.build_from_molecule_string(molecule_string='CCC(=O)Cl', inp_fmt='smiles')
    mol2 = molecule_constructor.build_from_molecule_string(molecule_string='CCNC(=O)CC', inp_fmt='smiles')

    assert mol1 in mp_syngraph.get_leaves()
    assert mol2 in mp_syngraph.get_roots()


def test_reaction_monopartite():
    graph_az = json.loads(open("data/az_retro_output_raw.json").read())
    mp_reac_syngraph = translator('az_retro', graph_az[0], 'syngraph', out_data_model='monopartite_reactions')

    chemical_equation_constructor = ChemicalEquationConstructor(identity_property_name='smiles')
    ce_root = chemical_equation_constructor.build_from_reaction_string(
        reaction_string='Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1.O=C('
                        'O)C1CCS(=O)(=O)CC1>>Cc1cccc(C)c1N(CC(=O)Nc1ccc('
                        '-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1',
        inp_fmt='smiles')
    assert ce_root in mp_reac_syngraph.get_roots()


def test_get_reaction_leaves():
    """ To test the MonopartiteReacSynGraph method 'get_leaves' correctly identifies the leaves (ReactionStep)
            in the graph. """
    graph = json.loads(open("data/az_retro_output_raw.json").read())
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


def test_extract_reactions():
    graph_az = json.loads(open("data/az_retro_output_raw.json").read())
    syngraph = translator('az_retro', graph_az[0], 'syngraph', 'monopartite_reactions')
    reactions = extract_reactions_from_syngraph(syngraph)
    assert len(reactions) == 2
    assert reactions[1]['reaction_string'] == 'Cc1cccc(C)c1NCC(=O)O.Nc1ccc(-c2ncon2)cc1>>Cc1cccc(C)c1NCC(=O)Nc1ccc(' \
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


def test_read_dictionary():
    # monopartite reactions
    d = [
        {'id': 0, 'reaction_string': 'Cc1cccc(C)c1NCC(=O)O.Nc1ccc(-c2ncon2)cc1>>Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1',
         'inp_fmt': 'smiles'},
        {'id': 1, 'reaction_string': 'Cc1cccc(C)c1NCC(=O)Nc1ccc(-c2ncon2)cc1.O=C(O)C1CCS(=O)(=O)CC1>>Cc1cccc(C)c1N(CC('
                                     '=O)Nc1ccc(-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1',
         'inp_fmt': 'smiles'}]
    syngraph = MonopartiteReacSynGraph(d)
    graph_az = json.loads(open("data/az_retro_output_raw.json").read())
    assert syngraph == translator('az_retro', graph_az[0], 'syngraph', 'monopartite_reactions')

    # bipartite
    d2 = [{'id': 0, 'reaction_string': 'CCC(=O)Cl.CCN>>CCNC(=O)CC', 'inp_fmt': 'smiles'}]
    graph_ibm = json.loads(open("data/ibmrxn_retro_output_raw.json").read())
    syngraph = BipartiteSynGraph(d2)
    assert syngraph == translator('ibm_retro', graph_ibm[3], 'syngraph', 'bipartite')

    # monopartite molecules
    d3 = [{'id': 0, 'reaction_string': 'CCC(=O)Cl.CCN.ClCCl>>CCNC(=O)CC', 'inp_fmt': 'smiles'}]
    mom_syngraph = MonopartiteMolSynGraph(d3)
    assert mom_syngraph == translator('ibm_retro', graph_ibm[4], 'syngraph', 'monopartite_molecules')
