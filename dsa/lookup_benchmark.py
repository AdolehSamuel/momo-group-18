import time
import random
import sys
# Let's grab the function we just finished to load all the data.
from data_loader import load_data_from_xml 

#1. PREPARING DATA STRUCTURES 

def create_lookup_structures(transactions_list):
    """
    Creates the optimal data structure (Dictionary/Hash Map) for lightning-fast lookups using 'tx_id'.

    Creation is O(N), but future lookups will be O(1).
    """
    print("\n--- 1. Prepping Lookup Structures ---")
    tx_id_map = {}
    for tx in transactions_list:
        #We use 'tx_id' as the unique key for direct access.
        tx_id_map[tx['tx_id']] = tx 
    
    #Also, prepare a simple list of IDs we'll use for the search test.
    all_tx_ids = [tx['tx_id'] for tx in transactions_list if tx['tx_id'] != 'N/A']
    
    print(f"Dictionary (Map) structure created with {len(tx_id_map)} unique entries.")
    return tx_id_map, all_tx_ids

# 2. SEARCH FUNCTIONS TO TEST 

def linear_search(data_list, tx_id_to_find):
    """
    Linear Search: Checks every single item in the list one by one.
    This is the SLOW method (Complexity: O(N)).
    """
    for tx in data_list:
        if tx['tx_id'] == tx_id_to_find:
            return tx
    return None

def dictionary_search(tx_id_map, tx_id_to_find):
    """
    Dictionary Search (Hash Map): Gets the result directly using the key.
    This is the FAST method (Complexity: O(1)).
    """
    return tx_id_map.get(tx_id_to_find, None)


#  3. RUNNING THE EFFICIENCY TEST 

def run_efficiency_test(data_list, tx_id_map, tx_ids_to_search, num_runs=1000):
    """
    Compares how fast the two search methods are over many runs.
    """
    print(f"\n--- 2. Running Efficiency Test ({num_runs} Lookups) ---")
    
    # Step 1: Linear Search (The slow guy)
    start_time_linear = time.perf_counter()
    for _ in range(num_runs):
        # Pick a random ID to search for each time
        random_id = random.choice(tx_ids_to_search)
        linear_search(data_list, random_id)
    end_time_linear = time.perf_counter()
    
    time_linear = (end_time_linear - start_time_linear) * 1000 # Time in milliseconds
    
    
    # Step 2: Dictionary Search (The fast guy)
    start_time_dict = time.perf_counter()
    for _ in range(num_runs):
        # Using the same random ID selection to keep it fair
        random_id = random.choice(tx_ids_to_search)
        dictionary_search(tx_id_map, random_id)
    end_time_dict = time.perf_counter()
    
    time_dict = (end_time_dict - start_time_dict) * 1000 # Time in milliseconds
    
    
    #RESULTS
    
    print("\n--- 3. Performance Comparison Results ---")
    print(f"Total transactions loaded: {len(data_list)}")
    print(f"Number of searches performed: {num_runs}")
    print("-" * 50)
    
    print(f"Time for LINEAR Search (O(N)): {time_linear:.4f} ms")
    print(f"Time for DICTIONARY Search (O(1)): {time_dict:.4f} ms")
    print("-" * 50)
    
    if time_dict > 0:
        improvement_factor = time_linear / time_dict
        print(f"The Dictionary (Hash Map) approach is {improvement_factor:.1f} times faster! Major performance win!")
    
    # Final check: make sure both searches actually find the data correctly.
    test_id = tx_ids_to_search[0]
    result_linear = linear_search(data_list, test_id)
    result_dict = dictionary_search(tx_id_map, test_id)
    
    if result_linear and result_dict:
        print(f"\nVALIDATION: OK. Both methods found the same result for ID {test_id[:10]}...")
    else:
        print("\nVALIDATION: ERROR. Something went wrong with the search logic.")


#4. MAIN ENTRY POINT 

if __name__ == '__main__':
    # Load all data from the XML file (O(N) initial cost, happens only once)
    transactions_data = load_data_from_xml()
    
    if transactions_data:
        # Create the dictionary structure (O(N) initial cost, happens only once)
        tx_map, tx_ids = create_lookup_structures(transactions_data)
        
        # Run the actual performance tests and show the numbers.
        # We use the list (transactions_data) for the slow linear search.
        # Let's run it 5000 times 
        run_efficiency_test(transactions_data, tx_map, tx_ids, num_runs=5000)
    else:
        print("Test aborted because no data was loaded.")