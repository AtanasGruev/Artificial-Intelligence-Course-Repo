def dfs_frog_puzzle_wrapper(start_state, goal_state, frog_states_dict):
    """ Wrapping the DFS algorithms and providing
        some utility data structures. """
    visited = set()
    pred_dict = {}
    pred_dict[start_state] = []
    return dfs_frog_puzzle(start_state, goal_state, frog_states_dict,
                           visited, pred_dict)


def dfs_frog_puzzle(start_state, goal_state, frog_states_dict,
                    visited, pred_dict):
    """ Recursive DFS performed on the dictionary.
        Easy implementation without a stack leads to
        need of list for predecessors. """
    visited.add(start_state)
    if start_state == goal_state:
        pred_list = [goal_state]
        if pred_dict[goal_state]:
            pred_state = pred_dict[goal_state]
            while pred_dict[pred_state]:
                pred_list.append(pred_state)
                pred_state = pred_dict[pred_state]
        print(pred_list[::-1])
    else:
        for state in frog_states_dict[start_state]:
            if state not in visited:
                pred_dict[state] = start_state
                dfs_frog_puzzle(state, goal_state, frog_states_dict,
                                visited, pred_dict)


def perform_frog_move(current_state, from_position, to_position):
    """ Actually moving the frog around. """
    current_state_list = list(current_state)
    save_frog_position = current_state_list[from_position]
    current_state_list[from_position] = current_state_list[to_position]
    current_state_list[to_position] = save_frog_position
    return "".join(current_state_list)


def observe_possible_frog_moves(current_state):
    """ Find possible moves for current configuration. """
    possible_moves_list = []
    free_lilly_index = current_state.index('_')
    if free_lilly_index - 1 >= 0:
        if current_state[free_lilly_index - 1] == '>':
            possible_moves_list.append((free_lilly_index - 1,
                                        free_lilly_index))
    if free_lilly_index - 2 >= 0:
        if current_state[free_lilly_index - 2] == '>':
            possible_moves_list.append((free_lilly_index - 2,
                                        free_lilly_index))
    if free_lilly_index + 1 < len(current_state):
        if current_state[free_lilly_index + 1] == '<':
            possible_moves_list.append((free_lilly_index + 1,
                                        free_lilly_index))
    if free_lilly_index + 2 < len(current_state):
        if current_state[free_lilly_index + 2] == '<':
            possible_moves_list.append((free_lilly_index + 2,
                                        free_lilly_index))
    return possible_moves_list


def is_impossible_move(current_state):
    """ Easy check for impossible branch """
    return '>><<' in current_state

# Instead of the build_tree procedure, it would be more
# cost-efficient to directly traverse the states


def build_tree_wrapper(current_state, goal_state, frog_states_dict):
    """ Recursive wrapper """
    visited = set()
    build_tree(current_state, goal_state, frog_states_dict, visited)


def build_tree(current_state, goal_state, frog_states_dict, visited):
    """ In order to use already defined DFS,
        let us implement a dictionary, which will
        give rise to an UndirectedWeightedGraph """
    visited.add(current_state)
    frog_states_dict[current_state] = []
    if current_state != goal_state and not is_impossible_move(current_state):
        moves = observe_possible_frog_moves(current_state)
        for move_tuple in moves:
            next_state = perform_frog_move(current_state,
                                           move_tuple[0], move_tuple[1])
            frog_states_dict[current_state].append(next_state)
            if next_state not in visited:
                build_tree(next_state, goal_state, frog_states_dict, visited)


def main():
    """ Puzzle logic"""
    number_frogs = int(input('Enter number of frogs -> ').strip())
    start_state = '>'*number_frogs + '_' + '<'*number_frogs
    goal_state = '<'*number_frogs + '_' + '>'*number_frogs

    frog_state_dict = {}
    build_tree_wrapper(start_state, goal_state, frog_state_dict)
    dfs_frog_puzzle_wrapper(start_state, goal_state, frog_state_dict)


if __name__ == '__main__':
    main()
