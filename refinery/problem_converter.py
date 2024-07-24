import os
import time
import nltk
import random
from nltk.corpus import words
from neo4j import GraphDatabase

# Program Properties
print_flag = False
random_seed = 4
random.seed(random_seed)

# Database Properties
ip = "3.99.79.114"
port = "7688"
username = 'neo4j'
password = 'mcgill123!'

# Setup Graph Data Structures
node_labels = []
edge_labels = []
connectivity_matrix = {}

# Download required NLTK data
nltk.download('words', quiet=True)

def convert_to_refinery():
    
    # Setup empty list for lines of reinfery problem
    refinery_problem = []

    for node_label in node_labels:
        # define a temp defintion of the node label in refinery format
        node_refinery_definition = []
        # count the number of outgoing edges for this node label 
        node_edge_counter = 0

        if print_flag: print("For Source Node: " + node_label)

        for target_node_label in connectivity_matrix[node_label]:
            edges = connectivity_matrix[node_label][target_node_label]
            
            if print_flag: print("To Target Node: " + target_node_label)
            
            if len(edges) == 0:
                if print_flag: print("No Edges Exist")
            else:
                for edge in edges:
                    node_edge_counter += 1
                    if print_flag: print("Edge #" + str(node_edge_counter) + ": " + str(edge))
                    node_refinery_definition.append('    ' + str(target_node_label) + '[1..*] ' + str(edge))
        
        if node_edge_counter == 0:
            node_refinery_definition.insert(0, 'class ' + str(node_label) + '.')
        else:
            node_refinery_definition.insert(0, 'class ' + str(node_label) + '{')
            node_refinery_definition.append('}')
        
        # Add a newline
        node_refinery_definition.append('')
        # Append node defintion to refinery problem data deifntion
        refinery_problem = refinery_problem + node_refinery_definition

    for line in refinery_problem:
        print(line)
    
    return refinery_problem


def generate_new_word(existing_words):
    # Get the list of all English words from the NLTK corpus
    word_list = words.words()
    
    # Convert the existing words to a set for faster lookup
    existing_words_set = set(existing_words)
    
    # Retry mechanism to find a new word
    attempts = 0
    new_word = None
    while not new_word and attempts < 100:
        # Select a random word from the word list
        random_word = random.choice(word_list).lower()
        
        # Ensure the new word is not in the existing words
        if random_word not in existing_words_set:
            new_word = random_word
        
        attempts += 1
    
    return new_word

def get_all_edges():
    # Collect all edges in the format (source_node_label, target_node_label, edge_label)
    all_edges = []
    for source_node_label in node_labels:
        for target_node_label in connectivity_matrix[source_node_label]:
            for edge_label in connectivity_matrix[source_node_label][target_node_label]:
                all_edges.append((source_node_label, target_node_label, edge_label))
    
    return all_edges

# Creates a new type and creates an edge to a random target node type
def add_node_label():
    # Generate a new node label
    new_node_label = generate_new_word(node_labels)

    # Add the new label to the connectivity matrix
    connectivity_matrix[new_node_label] = {end_label: set() for end_label in node_labels}

    # Add this new label to the node_labels list
    node_labels.append(new_node_label)

    for node_label in node_labels:
         connectivity_matrix[node_label][new_node_label] = set()

    # Create a new edge type label
    new_edge_label = generate_new_word(edge_labels)
    edge_labels.append(new_edge_label)

    # Select a random target node label from the existing labels
    target_node_label = random.choice(node_labels)

    # Add the new edge type between the the new node type and the randomly selected target node type
    connectivity_matrix[new_node_label][target_node_label].add(new_edge_label)

    return new_node_label, new_edge_label, target_node_label
    

# Deletes a node type and all associated edges
def delete_node_label():
    # Select a random node label from the existing labels to delete
    delete_node_label = random.choice(node_labels)

    # Remove the node label from the list
    node_labels.remove(delete_node_label)
    
    # Remove the node label as a target for all relationships
    for node_label in node_labels:
        del connectivity_matrix[node_label][delete_node_label]
    
    # Remove node label as a source for all relationships
    del connectivity_matrix[delete_node_label]

    # Recompute the edge label set
    temp_edge_labels = set()

    for source_node_label in node_labels:
        for target_node_label in connectivity_matrix[source_node_label]:
            for edge_type in connectivity_matrix[source_node_label][target_node_label]:
                temp_edge_labels.add(edge_type)
    
    edge_labels = list(temp_edge_labels)

    return delete_node_label

# Adds an edge type and creates an edge between two random node types
def add_edge_label():
    # Create a new edge type label
    new_edge_label = generate_new_word(edge_labels)
    edge_labels.append(new_edge_label)

    # Select a random source and target node label from the existing labels
    source_node_label = random.choice(node_labels)
    target_node_label = random.choice(node_labels)

    connectivity_matrix[source_node_label][target_node_label].add(new_edge_label)

    return source_node_label, new_edge_label, target_node_label

# Adds an existing edge type between two ramdom nodes
def add_edge():
    # Choose a random edge label
    random_edge_label = random.choice(edge_labels)

    # Select a random source and target node label from the existing labels
    source_node_label = random.choice(node_labels)
    target_node_label = random.choice(node_labels)

    connectivity_matrix[source_node_label][target_node_label].add(random_edge_label)

    return source_node_label, random_edge_label, target_node_label

# Adds an edge in reverse of an existing edge
def add_edge_reverse():
    # Get all edges
    all_edges = get_all_edges()

    # If no edges exist, return
    if not all_edges:
        print("No edges to add in reverse.")
        return None

    # Randomly select one edge
    random_edge = random.choice(all_edges)
    source_node_label, target_node_label, edge_label = random_edge

    # Add Edge in reverse
    connectivity_matrix[target_node_label][source_node_label].add(edge_label)

    return target_node_label, edge_label, source_node_label

# Deletes an edge type and all edges of that type
def delete_edge_label():
    # Choose a random edge label
    delete_edge_label = random.choice(edge_labels)

    # Remove the edge label from the list
    edge_labels.remove(delete_edge_label)

    # Delete edge label from connectivity matrix
    for source_node_label in node_labels:
        for target_node_label in connectivity_matrix[source_node_label]:
            connectivity_matrix[source_node_label][target_node_label].discard(delete_edge_label)
    
    return delete_edge_label

def move_edge():
    # Get all edges
    all_edges = get_all_edges()
    
    # If no edges exist, return
    if not all_edges:
        print("No edges to move.")
        return None

    # Randomly select one edge
    random_edge = random.choice(all_edges)
    source_node_label, target_node_label, move_edge_label = random_edge

    # Remove edge from existing node pair
    connectivity_matrix[source_node_label][target_node_label].discard(move_edge_label)

    # Select a random source and target node label from the existing labels
    random_source_node_label = random.choice(node_labels)
    random_target_node_label = random.choice(node_labels)

    # Add edge to a new node pair
    connectivity_matrix[random_source_node_label][random_target_node_label].add(move_edge_label)

    return random_source_node_label, move_edge_label, random_target_node_label

def change_edge_direction():
    # Get all edges
    all_edges = get_all_edges()

    # If no edges exist, return
    if not all_edges:
        print("No edges to reverse")
        return None
    
    # Randomly select one edge
    random_edge = random.choice(all_edges)
    source_node_label, target_node_label, flip_edge_label = random_edge

    # Remove edge from existing node pair
    connectivity_matrix[source_node_label][target_node_label].discard(flip_edge_label)

    # Add edge to reversed node pair
    connectivity_matrix[target_node_label][source_node_label].add(flip_edge_label)

    return target_node_label, flip_edge_label, source_node_label

def change_edge_multiplicity(): pass

def main():

    # Setup Datebase Connection
    url = "bolt://{}:{}".format(ip, port)
    driver = GraphDatabase.driver(url, auth=(username, password))


    # Setup the Queries
    get_node_labels_query = """
        CALL db.labels() YIELD label
        RETURN label
        ORDER BY label;
    """

    get_edge_labels_query = """
        CALL db.relationshipTypes() YIELD relationshipType
        RETURN relationshipType
        ORDER BY relationshipType;
    """

    # Get Connectivity Matrix
    get_connectivity_query = """
        MATCH (a)-[r]->(b)
        RETURN DISTINCT labels(a) AS startLabel, type(r) AS relationshipType, labels(b) AS endLabel
    """

    with driver.session() as session:
        # Get Node Labels 
        node_result = session.run(get_node_labels_query)
        for record in node_result:
            if print_flag: print(record)
            node_labels.append(record['label'])
        
        # Get the Edge Labels
        edge_result = session.run(get_edge_labels_query)
        for record in edge_result:
            if print_flag: print(record)
            edge_labels.append(record['relationshipType'])

        # Initialize the connectivity matrix
        for start_label in node_labels:
            connectivity_matrix[start_label] = {end_label: set() for end_label in node_labels}

        # Get Connectivity Data
        connectivity_result = session.run(get_connectivity_query)
        for record in connectivity_result:
            if print_flag: print(record)
            start_labels = record['startLabel']
            relationship_type = record['relationshipType']
            end_labels = record['endLabel']
            for start_label in start_labels:
                for end_label in end_labels:
                    connectivity_matrix[start_label][end_label].add(relationship_type)

    print(node_labels)
    print(edge_labels)
    print(connectivity_matrix)

    refinery_problem = convert_to_refinery()
    
    
    # Add a new node
    # change_edge_direction()
    # print(node_labels)
    # print(edge_labels)
    # print(connectivity_matrix)

    refinery_problem = convert_to_refinery()
    


if __name__ == '__main__':
    main()

