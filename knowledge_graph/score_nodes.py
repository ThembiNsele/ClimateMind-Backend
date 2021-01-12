import pickle
import networkx as nx
import sys
from collections import Counter
from knowledge_graph.make_graph import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)
from knowledge_graph.build_localised_acyclic_graph import build_localised_acyclic_graph
from knowledge_graph.store_climate_feed_data import store_climate_feed_data
import numpy as np
import random
from collections import OrderedDict


def get_node_id(node):
    """Node IDs are the unique identifier in the IRI. This is provided to the
    front-end as a reference for the feed, but is never shown to the user.

    Example http://webprotege.stanford.edu/R8znJBKduM7l8XDXMalSWSl

    Parameters
    ----------
    node - A networkX node
    """
    offset = 4  # .edu <- to skip these characters and get the unique IRI
    full_iri = node["iri"]
    pos = full_iri.find("edu") + offset
    return full_iri[pos:]


def get_description(node):
    """Long Descriptions are used by the front-end to display explanations of the
    climate effects shown in user feeds.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_longDescription"][0]
    except:
        return "No long desc available at present"


def get_myth_claim(node):
    """Myth claims are used by the front-end to display a description of a phrase or claim the user might hear when someone says the myth.

    Parameters
    ----------
    node - A networkX myth node
    """
    try:
        return node["properties"]["schema_mythClaim"][0]
    except:
        return "No myth claim available at present"


def get_myth_rebuttal(node):
    """Myth rebuttals are used by the front-end to display a description of a reason or rebuttal the user could say in response to someone saying the myth.
    The rebuttals are the reason(s) why the myth is not true and what the science says is true.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_mythRebuttal"][0]
    except:
        return "No myth rebuttal available at present"


def get_myth_sources(node):
    """Myth sources are used by the frontend to display the source of the myth."""
    try:
        # return list(set(node["properties"]["schema_organizationSource"]))
        return list(set(node["myth sources"]))
    except:
        return []


def get_myth_video_urls(node):
    """Myth video are used by the frontend to display the video url of the myth."""
    if node["properties"]["schema_video"]:
        try:
            return list(set(node["properties"]["schema_video"]))
        except:
            return "No videos available at present"
    else:
        return None


def get_myth_fallacy(node):
    """Myth fallacy (also called 'faulty logic description') are used by the front-end to display a description of why a myth is logically wrong.

    Parameters
    ----------
    node - A networkX node
    """
    if node["properties"]["schema_mythFallacy"]:
        try:
            return node["properties"]["schema_mythFallacy"][0]
        except:
            return "No faulty logic description available at present"
    else:
        return None


def get_short_description(node):
    """Short Descriptions are used by the front-end to display explanations of the
    climate effects shown in user feeds.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_shortDescription"][0]
    except:
        return "No short desc available at present"


def get_image_url(node):
    """Images are displayed to the user in the climate feed to accompany an explanation
    of the climate effects. The front-end is provided with the URL and then requests
    these images from our server.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_image"][0]
    except:
        # Default image url if image is added
        return "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"


def get_effect_specific_myths(node, G):
    """Climate change impacts sometimes have myths about them.
    This function takes a node and returns the IRIs of any myths about the impact.

    Parameters
    ----------
    node - A networkX node
    """

    try:
        # if node["label"] == "decrease in population of moose available to hunt": breakpoint()
        if "impact myths" in node.keys() and node["impact myths"]:
            G = get_pickle_file(
                "Climate_Mind_DiGraph.gpickle"
            )  # the graph G should be the same everywhere in the app but for some reason it is not... grr!
            IRIs = []
            for myth_name in node["impact myths"]:
                myth = G.nodes[myth_name]
                IRIs.append(get_node_id(myth))
        return IRIs
    except:
        return []


def get_solution_specific_myths(node, G):
    """Climate change solutions sometimes have myths about them.
    This function takes a node and returns the IRIs of any myths about the solution.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        if "solution myths" in node.keys() and node["solution myths"]:
            # G = get_pickle_file("Climate_Mind_DiGraph.gpickle") #the graph G should be the same everywhere in the app but for some reason it is not... grr!
            IRIs = []
            for myth_name in node["solution myths"]:
                myth = G.nodes[myth_name]
                IRIs.append(get_node_id(myth))
        return IRIs
    except:
        return []


def get_image_url_or_none(node):
    """Images are displayed to the user in the climate feed to accompany an explanation
    of the climate effects. The front-end is provided with the URL and then requests
    these images from our server.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_image"][0]
    except:
        # Default image url if image is added
        return None


def get_causal_sources(node):
    """Sources are displayed to the user in the sources tab of the impacts overlay page.
    This function returns a list of urls of the sources to show on the impact overlay page for an impact/effect.
    Importantly, these sources aren't directly from the networkx node, but all the networkx edges that cause the node.
    Only returns edges that are directly tied to the node (ancestor edge sources are not used)
    Parameters
    ----------
    node - A networkX node
    """
    if "causal sources" in node and len(node["causal sources"]) > 0:
        causal_sources = node["causal sources"]

    try:
        return causal_sources
    except:
        return (
            []
        )  # Default source if none #should this be the IPCC? or the US National Climate Assessment?


def get_solution_sources(node):
    """Returns a flattened list of custom solution source values from each node key that matches
    custom_source_types string.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["solution sources"]
    except:
        return []


def get_is_possibly_local(node):
    if "isPossiblyLocal" in node:
        if node["isPossiblyLocal"]:
            return 1
        else:
            return 0
    else:
        return 0


def get_scores_vector(user_scores):
    """Extracts scores from a dictionary and returns the scores as a vector.

    Used in simple_scoring to compute a dot product.

    Parameters
    ----------
    user_scores - Dictionary of Scores
    """
    return [
        user_scores["achievement"],
        user_scores["benevolence"],
        user_scores["conformity"],
        user_scores["hedonism"],
        user_scores["power"],
        user_scores["security"],
        user_scores["self_direction"],
        user_scores["stimulation"],
        user_scores["tradition"],
        user_scores["universalism"],
    ]


OFFSET = 4  # .edu <- to skip these characters and get the unique IRI
ALPHA = (
    2  # variable for transforming user questionnaire scores to exponential distribution
)
MAX_N_SOLUTIONS = 4
RATIO = 0.5  # ratio of number of adaptation to mitigation solutions to aspire to show in the user's feed


def simple_scoring(G, user_scores, session_id):
    """Each climate effects node will have personal values associated with it. These
    values are stored as a vector within the node. This vector is run through the
    dot product with the users scores to determine the overall relevance of the node
    to a user's values.

    Parameters
    ----------
    G - A NetworkX Graph
    user_scores - A dictionary of personal values (keys) and scores (values)
    """
    climate_effects = []
    user_scores_vector = np.array(get_scores_vector(user_scores))
    modified_user_scores_vector = np.power(user_scores_vector, ALPHA)
    localised_acyclic_graph = build_localised_acyclic_graph(G, session_id)

    for node in G.nodes:
        if "personal_values_10" in G.nodes[node] and any(
            G.nodes[node]["personal_values_10"]
        ):
            node_values_associations_10 = G.nodes[node]["personal_values_10"]
            d = {
                "effectId": get_node_id(G.nodes[node]),
                "effectTitle": G.nodes[node]["label"],
                "effectDescription": get_description(G.nodes[node]),
                "effectShortDescription": get_short_description(G.nodes[node]),
                "imageUrl": get_image_url(G.nodes[node]),
                "effectSources": get_causal_sources(G.nodes[node]),
                "isPossiblyLocal": get_is_possibly_local(
                    localised_acyclic_graph.nodes[node]
                ),
                "effectSpecificMythIRIs": get_effect_specific_myths(G.nodes[node], G),
            }

            if any(v is None for v in node_values_associations_10):
                score = None
            else:
                node_values_associations_10 = np.array(node_values_associations_10)
                # double the magnitude of the backfire-effect representation:
                modified_node_values_associations_10 = np.where(
                    node_values_associations_10 < 0,
                    2 * node_values_associations_10,
                    node_values_associations_10,
                )
                score = np.dot(
                    modified_user_scores_vector, modified_node_values_associations_10
                )
                d["effectSolutions"] = get_user_actions(
                    G.nodes[node]["label"], MAX_N_SOLUTIONS, RATIO
                )

            d["effectScore"] = score
            climate_effects.append(d)

    return climate_effects


def get_best_nodes(climate_effects, n):
    """Returns the top n Nodes for a user along with the scores for those nodes.
    If a node has no score, it will be assigned -inf as it could be risky to show
    a user an unreviewed climate effect. (may have a backfire effect).

    Parameters
    ----------
    nodes_with_scores - Dictionary containing NetworkX nodes and Integer scores
    n - Integer to specify # of desired scores
    """
    best_nodes = sorted(
        climate_effects, key=lambda k: k["effectScore"] or float("-inf"), reverse=True
    )[:n]
    return best_nodes


def get_pickle_file(filename):
    G = nx.read_gpickle(filename)
    return G


def get_user_nodes(user_scores, n, session_id):
    """Returns the top n Nodes for a user feed.

    Parameters
    ----------
    nodes_with_scores - Dictionary containing NetworkX nodes and Integer scores
    n - Integer to specify # of desired scores
    """
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")

    valid_test_ont = get_valid_test_ont()
    not_test_ont = get_non_test_ont()

    get_test_ontology(G, valid_test_ont, not_test_ont)
    climate_effects = simple_scoring(G, user_scores, session_id)
    best_nodes_for_user = get_best_nodes(climate_effects, n)
    store_climate_feed_data(session_id, best_nodes_for_user)
    return best_nodes_for_user


def solution_randomizer(
    adaptation_solutions,
    mitigation_solutions,
    max_solutions,
    adaptation_to_mitigation_ratio=0.5,
):
    """Takes list of solutions and decides which adaptation solutions to randomly show and which mitigation solutions to randomly show.

    Parameters
    ----------
    adaptation_solutions - A list of adaptation solutions
    mititgation_solutions - A list of mitigation solutions
    max_solutions - integer of how many solutions total to return
    adaptation_to_mitigation_ratio - A decimal from 0 to 1 that reflects the percentage of solutions to be adaptation solutions to aspire to show where possible (rounded down)
    """
    number_adaptation_max = np.math.floor(
        max_solutions * adaptation_to_mitigation_ratio
    )
    if len(adaptation_solutions) <= number_adaptation_max:
        number_mitigation = max_solutions - len(adaptation_solutions)
        solutions = adaptation_solutions + random.sample(
            mitigation_solutions, number_mitigation
        )
    else:
        solutions = random.sample(
            adaptation_solutions, number_adaptation_max
        ) + random.sample(mitigation_solutions, max_solutions - number_adaptation_max)
    return solutions


def get_user_actions(effect_name, max_solutions, adaptation_to_mitigation_ratio):
    """Takes the name of a climate effect and returns a list of actions associated with
    that node.

    Parameters
    ----------
    effect_name - A string
    max_n - maximum number of results to return
    """
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")
    solution_names = G.nodes[effect_name]["adaptation solutions"]
    adaptation_solutions = []
    mitigation_solutions = []
    for solution in solution_names:
        try:
            s_dict = {
                "iri": get_node_id(G.nodes[solution]),
                "solutionTitle": G.nodes[solution]["label"],
                "solutionType": "adaptation",
                "shortDescription": get_short_description(G.nodes[solution]),
                "longDescription": get_description(G.nodes[solution]),
                "imageUrl": get_image_url_or_none(G.nodes[solution]),
                "solutionSpecificMythIRIs": get_solution_specific_myths(
                    G.nodes[solution], G
                ),
                "solutionSources": get_solution_sources(G.nodes[solution]),
            }

            # only include direct adaptation solutions (ignore adaptation solutions that are upstream for now)
            for neighbor in G.neighbors(effect_name):
                if (
                    G[effect_name][neighbor]["type"]
                    == "is_inhibited_or_prevented_or_blocked_or_slowed_by"
                    and neighbor == solution
                ):
                    adaptation_solutions.append(s_dict)

        except:
            pass
    solution_names = G.nodes["increase in greenhouse effect"]["mitigation solutions"]
    for solution in solution_names:
        # if solution == "producing electricity via concentrated solar power": breakpoint()
        try:
            s_dict = {
                "iri": get_node_id(G.nodes[solution]),
                "solutionTitle": G.nodes[solution]["label"],
                "solutionType": "mitigation",
                "shortDescription": get_short_description(G.nodes[solution]),
                "longDescription": get_description(G.nodes[solution]),
                "imageUrl": get_image_url_or_none(G.nodes[solution]),
                "solutionSpecificMythIRIs": get_solution_specific_myths(
                    G.nodes[solution], G
                ),
                "solutionSources": get_solution_sources(G.nodes[solution]),
            }
            mitigation_solutions.append(s_dict)
        except:
            pass
    solutions = solution_randomizer(
        adaptation_solutions,
        mitigation_solutions,
        max_solutions,
        adaptation_to_mitigation_ratio,
    )
    return solutions


def get_user_general_myth_nodes():
    """Returns a list of general myths and some information about those general myths.
    # The myths will later be ranked based on user's personal values (although not being done in the current implementation).
    # Parameters
    ----------
    # user_scores - User's personal values scores (same format as that stored in the SQL database).
    """
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")
    # all_myths = nx.get_node_attributes(G, "myth")
    general_myths = G.nodes["increase in greenhouse effect"]["general myths"]
    # for myth in all_myths:
    #    if
    general_myths_details = []
    for myth in general_myths:
        d = {
            "iri": get_node_id(G.nodes[myth]),
            "mythTitle": G.nodes[myth]["label"],
            "mythClaim": get_myth_claim(G.nodes[myth]),
            "mythRebuttal": get_myth_rebuttal(G.nodes[myth]),
            "mythSources": get_myth_sources(G.nodes[myth]),
            "mythVideos": get_myth_video_urls(G.nodes[myth]),
            "faultyLogicDescription": get_myth_fallacy(G.nodes[myth]),
        }

        general_myths_details.append(d)

    return general_myths_details


def get_specific_myth_info(iri):
    """
    Returns infomation for a specific myth.
    """
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")
    all_myths = nx.get_node_attributes(G, "myth")

    specific_myth = None

    for myth in all_myths:
        if get_node_id(G.nodes[myth]) == iri:
            specific_myth = myth

    if specific_myth:
        myth = {
            "iri": get_node_id(G.nodes[specific_myth]),
            "mythTitle": G.nodes[specific_myth]["label"],
            "mythClaim": get_myth_claim(G.nodes[specific_myth]),
            "mythRebuttal": get_myth_rebuttal(G.nodes[specific_myth]),
            "mythSources": get_myth_sources(G.nodes[specific_myth]),
            "mythVideos": get_myth_video_urls(G.nodes[specific_myth]),
            "faultyLogicDescription": get_myth_fallacy(G.nodes[specific_myth]),
        }
        return myth
    else:
        return False


def get_user_general_solution_nodes():
    """Returns a list of general solutions and some information about those general solutions.
    # The myths will later be ranked based on user's personal values (although not being done in the current implementation).
    # Parameters
    ----------
    # user_scores - User's personal values scores (same format as that stored in the SQL database).
    """
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")
    # all_myths = nx.get_node_attributes(G, "myth")
    general_solutions = G.nodes["increase in greenhouse effect"]["mitigation solutions"]
    # for myth in all_myths:
    #    if
    general_solutions_details = []
    for solution in general_solutions:
        d = {
            "iri": get_node_id(G.nodes[solution]),
            "solutionTitle": G.nodes[solution]["label"],
            "solutionType": "mitigation",
            "shortDescription": get_short_description(G.nodes[solution]),
            "longDescription": get_description(G.nodes[solution]),
            "imageUrl": get_image_url_or_none(G.nodes[solution]),
            "solutionSpecificMythIRIs": get_solution_specific_myths(
                G.nodes[solution], G
            ),
            "solutionSources": get_solution_sources(G.nodes[solution]),
        }

        if d not in general_solutions_details:
            general_solutions_details.append(d)

    return general_solutions_details
