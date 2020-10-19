from collections import deque


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


# The previous implementation (found below) is very inefficient indeed -
# exponential in time due to the tree being build explicitly.
# Instead, here a build-and-traverse approach is adopted.
def build_and_traverse(start_state, goal_state):
    """ DFS traverses the 'frog' tree by exploring the branches
        in-depth. Function returns when a solution is reached. """
    stack = deque([start_state])
    path_dict = {}
    path_dict[start_state] = 'NULL'
    visited = set(start_state)
    while stack:
        current_state = stack.pop()
        if current_state == goal_state:
            print_state = goal_state
            while path_dict[print_state] != 'NULL':
                print(print_state)
                print_state = path_dict[print_state]
            print(start_state)
            break
        if current_state not in visited:
            visited.add(current_state)
        possible_moves = observe_possible_frog_moves(current_state)
        for move in possible_moves:
            child_state = perform_frog_move(current_state, move[0], move[1])
            path_dict[child_state] = current_state
            if child_state not in visited:
                stack.append(child_state)


# Instead of the build_tree procedure, it would be much more
# cost-efficient to directly traverse the states
# The more effective approach is implemented above.


def is_impossible_move(current_state):
    """ Easy check for impossible branch
        (two more options available)
        ADD: ><<...; ADD ...>>< """
    return '>><<' in current_state


def build_tree_wrapper(current_state, goal_state, frog_states_dict):
    """ Recursive wrapper """
    visited = set()
    build_tree(current_state, goal_state, frog_states_dict, visited)


def build_tree(current_state, goal_state, frog_states_dict, visited):
    """ In order to use already defined DFS,
        let us implement a dictionary, which will
        give rise to a dictionary, which is then
        fed to the DFS procedure. """
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


def main():
    """ Puzzle logic"""
    number_frogs = int(input('Enter number of frogs -> ').strip())
    start_state = '>'*number_frogs + '_' + '<'*number_frogs
    goal_state = '<'*number_frogs + '_' + '>'*number_frogs

    # frog_state_dict = {}
    # build_tree_wrapper(start_state, goal_state, frog_state_dict)
    # dfs_frog_puzzle_wrapper(start_state, goal_state, frog_state_dict)

    build_and_traverse(start_state, goal_state)


if __name__ == '__main__':
    main()
