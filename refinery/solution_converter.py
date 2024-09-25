# Load the solution file
import re
from neo4j import GraphDatabase
import sys

# Program Properties
print_flag = False

# Setup Datebase Connection
ip = "3.99.79.114"
port = "7687"
username = 'neo4j'
password = 'mcgill123!'

# Example Solution File
input_solution_file = "/Users/fozail/SchoolDev/graphs4value/testing/pipeline/5.1.0/graphAddEdge30R1.solution"

def main():

    url = "bolt://{}:{}".format(ip, port)
    driver = GraphDatabase.driver(url, auth=(username, password))

    solution_file = open(input_solution_file, 'r')
    solution_file_lines = solution_file.readlines()
    solution_file_lines_stripped = []


    start_index = 0
    count = 0
    # Strips the newline character
    for line in solution_file_lines:
        line_stripped = line.strip()
        solution_file_lines_stripped.append(line_stripped)
        if 'declare' in line_stripped:
            if print_flag: print("Found start of graph data: " + str(count))
            start_index = count
        
        count += 1


    graph_instance = solution_file_lines_stripped[start_index:]

    # node_regex = "([a-zA-Z])\w+\(([a-zA-Z])\w+\)."
    node_regex = "^(\w+)\((\w+)\)\.$"
    # transition_regex = "([a-zA-Z])\w+\(([a-zA-Z])\w+, ([a-zA-Z])\w+\)."
    transition_regex = "^(\w+)\((\w+),\s*(\w+)\)\.$"
    delimiters = ["(", ")", ",", "."]

    node_types = set()
    num_nodes = 0
    transition_types = set()
    num_edges = 0
    for line in graph_instance:

        if re.search(node_regex, line):
            regex_match = re.search(node_regex, line)
            node_type = regex_match.group(1)  # This will be 'Actor'
            node_id = regex_match.group(2)  # This will be 'actor5'
            # print("Node Line: ", line)
            if print_flag: print("Node Type:", node_type, "| Node ID:", node_id)
            node_types.add(node_type)
            num_nodes += 1
            with driver.session() as session:
                create_node_query = "MERGE ({}:{} {{rid: '{}'}})".format(node_id, node_type, node_id)
                if print_flag: print("Create Node Query:", create_node_query)
                session.run(create_node_query)
        elif re.search(transition_regex, line):
            regex_match = re.search(transition_regex, line)
            # Get the transition type
            transition_type = regex_match.group(1)
            # Remove the Refinery specific numbering for transitions
            transition_type = transition_type[:-1]
            transition_source = regex_match.group(2)
            transition_target = regex_match.group(3)
            # print("Transition Line: ", line)
            if print_flag: print("Transition Type:", transition_type, "| Source Node:", transition_source, "-> Target Node:", transition_target)
            transition_types.add(transition_type)
            num_edges += 1
            with driver.session() as session:
                create_edge_query = """
                MATCH (a {{rid: '{}'}}), (b {{rid: '{}'}})
                MERGE (a)-[r:{}]->(b)
                RETURN type(r)
                """.format(transition_source, transition_target, transition_type)
                if print_flag: print("Create Edge Query:", create_edge_query)
                session.run(create_edge_query)
        else:
            if print_flag: print("Metadata: ", line)

    print("Node Types:", node_types)
    print("Transition Types:", transition_types)
    print("Number of Nodes:", num_nodes)
    print("Number of Edges:", num_edges)

    # Close Database Session
    driver.close()

if __name__ == '__main__':
    input_solution_file = str(sys.argv[1])
    ip = str(sys.argv[2])
    main()