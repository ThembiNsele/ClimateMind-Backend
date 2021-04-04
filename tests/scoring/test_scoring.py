import flask
import pytest
from app.scoring.build_localised_acyclic_graph import get_starting_nodes, get_iri, get_node_id
from app.scoring.persist_scores import persist_scores
from unittest.mock import patch
import app


def test_persist_scores(client):
    from app.models import Scores
    test_data = {
        "session-id": "1",
        "security": 1.0,
        "conformity": 1.0,
        "benevolence": 1.0,
        "tradition": 1.0,
        "universalism": 1.0,
        "self-direction": 1.0,
        "stimulation": 1.0,
        "hedonism": 1.0,
        "achievement": 1.0,
        "power": 1.0,
    }

    expected_scores = Scores()
    expected_scores.session_uuid = test_data["session-id"]
    expected_scores.security = test_data["security"]
    expected_scores.conformity = test_data["conformity"]
    expected_scores.benevolence = test_data["benevolence"]
    expected_scores.tradition = test_data["tradition"]
    expected_scores.universalism = test_data["universalism"]
    expected_scores.self_direction = test_data["self-direction"]
    expected_scores.stimulation = test_data["stimulation"]
    expected_scores.hedonism = test_data["hedonism"]
    expected_scores.achievement = test_data["achievement"]
    expected_scores.power = test_data["power"]

    with patch('app.scoring.persist_scores.db') as fake_db:
        persist_scores(test_data)
        session_has_been_added = False
        scores_have_been_added = False
        for called_args in fake_db.session.add.call_args_list:
            if type(called_args.args[0]) == app.models.Sessions and called_args.args[0].session_uuid == test_data[
                'session-id']:
                session_has_been_added = True
        for called_args in fake_db.session.add.call_args_list:
            if type(called_args.args[0]) == app.models.Scores:
                # Run through keys of test_data, make sure it matches.
                for key in test_data.keys():
                    if key == "session-id" or key =='self-direction':
                        # Session-id is replaced by session_uuid (different key name in test_data and Scores model)
                        # Besides, checking session-id is already done in the preceding for loop.
                        continue
                    assert getattr(called_args.args[0], key) == test_data[key]
                scores_have_been_added = True

        assert session_has_been_added
        assert scores_have_been_added
        assert fake_db.session.commit.call_count



def test_import_client_fixture_has_flask_application_context(client):
    # Test if the client fixture works properly

    # Dummy assert. Will run some code that requires an application context.
    # Therefore, test fails if client fixture doesn't request an application context.
    import app.scoring.score_nodes
    assert flask.current_app


@pytest.fixture
def score_nodes_class(client):
    from app.scoring.score_nodes import score_nodes
    return score_nodes


def test_get_iri():
    iri_full_string = "http://webprotege.stanford.edu/6aQR6SoftbrPsIW438WmR8AiVdc6"
    assert get_iri(iri_full_string) == "6aQR6SoftbrPsIW438WmR8AiVdc6"


def test_node_get_iri():
    node = dict(iri="http://webprotege.stanford.edu/6aQR6SoftbrPsIW438WmR8AiVdc6")
    assert get_node_id(node) == "6aQR6SoftbrPsIW438WmR8AiVdc6"


def test_get_starting_nodes(networkx_ontology):
    starting_nodes = get_starting_nodes(networkx_ontology)

    # Check starting nodes satisfy requirements described in get_starting_nodes. Check correctness.
    for sn in starting_nodes:
        assert "risk solution" not in networkx_ontology.nodes[sn]
        assert "test ontology" in networkx_ontology.nodes[sn]

        for source, destination, properties in networkx_ontology.out_edges(
                sn, data="type"
        ):
            assert "causes_or_promotes" not in properties

    # Check completeness.
    for node, data in networkx_ontology.nodes(data=True):
        if "risk solution" not in data and "test ontology" in data:
            has_no_child = True
            for source, destination, properties in networkx_ontology.out_edges(
                    node, data="type"
            ):
                if "causes_or_promotes" in properties:
                    has_no_child = False
                    break
            if has_no_child:
                assert node in starting_nodes


FAKE_USER_SCORES = {
    "benevolence": 1,
    "conformity": 0,
    "achievement": 1,
    "hedonism": -1,
    "tradition": 0,
    "security": 0,
    "power": 1,
    "universalism": -1,
    "self_direction": 1,
    "stimulation": 1,
}


def test_simple_scoring_algorithm(score_nodes_class):
    score_nodes_object = score_nodes_class(FAKE_USER_SCORES, 20, None)
    score_nodes_object.get_user_nodes()

    # Since the specific wording of each description of nodes might change, we test for existence of each property.

    score_nodes_key = set(score_nodes_object.__dict__.keys())

    correct_keys = set(
        ["NX_UTILS",
         "MAX_N_SOLUTIONS",
         "ALPHA",
         "SOL_PROCESSOR",
         "BEST_NODES",
         "CLIMATE_EFFECTS",
         "RATIO",
         "N",
         "SESSION_UUID",
         "USER_SCORES",
         "MYTH_PROCESSOR",
         "G", ]
    )
    assert correct_keys.issubset(score_nodes_key)


def test_get_scores_vector(score_nodes_class):
    # Test that get_scores_vector returns an array with the correct ordering of elements
    # Make sure we're not relying on the order of user scores that are entered.

    score_nodes_object = score_nodes_class(FAKE_USER_SCORES, 20, None)
    assert score_nodes_object.get_scores_vector()[0] == FAKE_USER_SCORES["achievement"]
    assert score_nodes_object.get_scores_vector()[1] == FAKE_USER_SCORES["benevolence"]
    assert score_nodes_object.get_scores_vector()[3] == FAKE_USER_SCORES["hedonism"]
    assert score_nodes_object.get_scores_vector()[5] == FAKE_USER_SCORES["security"]
    assert score_nodes_object.get_scores_vector()[7] == FAKE_USER_SCORES["stimulation"]
