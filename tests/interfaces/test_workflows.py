from linchemin.interfaces.workflows import process_routes, get_workflow_options, MergingStep
from linchemin.interfaces.facade import facade

import pytest
import os
import unittest.mock


@unittest.mock.patch('linchemin.IO.io.write_json')
def test_workflow_basic(mock_os):
    path = "../cgu/data/az_retro_output_raw.json"
    input_dict = {path: 'az'}
    out = process_routes(input_dict)
    assert out

    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_os.assert_called_with(routes, "routes.json")

    path2 = "../cgu/data/ibm_output2.json"
    input_dict_multicasp = {path: 'az',
                            path2: 'ibmrxn'}
    out = process_routes(input_dict_multicasp)
    assert out

    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_os.assert_called_with(routes, "routes.json")

    # error raised for invalid casp
    with pytest.raises(KeyError) as ke:
        input_dict2 = {path: 'wrong_casp'}
        process_routes(input_dict2, output_format='json')
    assert "KeyError" in str(ke.type)

    # error raised for invalid output format
    with pytest.raises(KeyError) as ke:
        input_dict = {path: 'az'}
        process_routes(input_dict, output_format='jpg')
    assert "KeyError" in str(ke.type)

    # error raised for invalid functionality
    with pytest.raises(KeyError) as ke:
        process_routes(input_dict, output_format='csv', functionalities=['func'])
    assert "KeyError" in str(ke.type)


@unittest.mock.patch('linchemin.IO.io.dict_list_to_csv')
@unittest.mock.patch('linchemin.IO.io.dataframe_to_csv')
def test_workflow_metric(mock_dataframe, mock_csv):
    path = "../cgu/data/ibm_output2.json"
    input_dict = {path: 'ibmrxn'}
    out = process_routes(input_dict, output_format='csv', functionalities=['compute_descriptors'],
                         descriptors=['branching_factor', 'nr_steps'],
                         parallelization=True, n_cpu=16)
    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_csv.assert_called_with(routes, "routes.csv")
    mock_dataframe.assert_called_with(out.descriptors, 'descriptors.csv')


@unittest.mock.patch('linchemin.interfaces.workflows.write_syngraph')
def test_merging(mock_writer1):
    path = "../cgu/data/az_retro_output_raw.json"
    input_dict = {path: 'az'}
    out = process_routes(input_dict, output_format='png', functionalities=['merging'])
    mock_writer1.assert_called_with(out.routes_list, 'bipartite', 'png', 'routes')


@unittest.mock.patch('linchemin.IO.io.dict_list_to_csv')
@unittest.mock.patch('linchemin.IO.io.dataframe_to_csv')
def test_workflow_cluster_dist_matrix(mock_dataframe, mock_csv):
    path = "../cgu/data/askos_output.json"
    input_dict = {path: 'askcos'}
    out = process_routes(input_dict, output_format='csv', functionalities=['clustering'])
    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_csv.assert_called_with(routes, "routes.csv")
    mock_dataframe.assert_called_with(out.clustered_descriptors, "cluster_metrics.csv")


@unittest.mock.patch('linchemin.IO.io.write_nx_to_graphml')
def test_workflow_graphml(mock_graphml):
    path = "../cgu/data/askos_output.json"
    input_dict = {path: 'askcos'}
    out = process_routes(input_dict, output_format='graphml')
    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_graphml.assert_called()


def test_helper(capfd):
    assert type(get_workflow_options()) == dict
    assert 'functionalities' in get_workflow_options()
    get_workflow_options(verbose=True)
    out, err = capfd.readouterr()
    assert 'input_dict' in out


@unittest.mock.patch('linchemin.IO.io.dict_list_to_csv')
@unittest.mock.patch('linchemin.IO.io.write_json')
def test_reaction_strings_extraction(mock_json, mock_csv):
    path = "../cgu/data/az_retro_output_raw.json"
    input_dict = {path: 'az'}
    out = process_routes(input_dict, output_format='csv', functionalities=['extracting_reactions'])
    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_csv.assert_called_with(routes, "routes.csv")
    mock_json.assert_called_with(out.reaction_strings, "reaction_strings.json")


@unittest.mock.patch('linchemin.IO.io.dict_list_to_csv')
@unittest.mock.patch('linchemin.IO.io.write_json')
def test_graphml(mock_json, mock_csv):
    path = "../cgu/data/az_retro_output_raw.json"
    input_dict = {path: 'az'}
    out = process_routes(input_dict, output_format='csv', functionalities=['extracting_reactions'])
    routes, meta = facade('translate', 'syngraph', out.routes_list, 'noc', out_data_model='bipartite')
    mock_csv.assert_called_with(routes, "routes.csv")
    mock_json.assert_called_with(out.reaction_strings, "reaction_strings.json")


def test_full_workflow():
    path = "../cgu/data/az_retro_output_raw.json"
    input_dict = {path: 'az'}
    process_routes(input_dict, out_data_model='monopartite_reactions',
                   functionalities=['compute_descriptors', 'clustering_and_d_matrix', 'merging'])
    assert os.path.exists('distance_matrix.csv')
    os.remove('distance_matrix.csv')
    assert os.path.exists('cluster_metrics.csv')
    os.remove('cluster_metrics.csv')
    assert os.path.exists('routes.json')
    os.remove('routes.json')
    assert os.path.exists('descriptors.csv')
    os.remove('descriptors.csv')
    assert os.path.exists('tree.json')
    os.remove('tree.json')
