// https://adventofcode.com/2021/day/15
// clear && g++ -Wall -Wextra -Werror -std=c++17 -o Day15.out ./Day15.cpp && ./Day15.out

#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
#include <deque>
#include <set>
#include <map>
#include <climits>

using namespace std;

vector<vector<int>> getGrid(const string filename) {
    string line;
    ifstream file;
    file.open(filename);

    vector<vector<int>> lines;
    while (getline(file, line))
    {
        vector<int> row;

        for (char c : line)
        {
            row.push_back(c - '0');
        }

        lines.push_back(row);
    }

    file.close();

    return lines;
}

void dump(const vector<vector<int>> grid) {
    for (vector<int> row : grid) {
        for (int n : row) {
            cout << n;
        }
        cout << '\n';
    }
}

int dijkstra_search(const vector<vector<int>> grid) {
    // create a list of final distances (we only need the last one)
    map<pair<size_t, size_t>, size_t> distances;
    vector<pair<size_t,size_t>> queue;
    set<pair<size_t, size_t>> visited;

    for (size_t i = 0; i < grid.size(); i++) {
        for (size_t j = 0; j < grid[i].size(); j++) {
            pair<size_t, size_t> n(i, j);
            distances[n] = INT_MAX;
            queue.push_back(n);
        }
    }

    // initialize root node as zero, all others "infinite"
    pair<size_t, size_t> first(0, 0);
    distances[first] = 0; 

    while (!queue.empty()) {
        // get the node
        auto it = min_element(queue.begin(), queue.end());
        pair<size_t, size_t> node = *it;

        visited.insert(node);

        size_t x = node.second;
        size_t y = node.first;

        vector<pair<size_t, size_t>> neighbors;

        // down
        pair<size_t, size_t> down(y+1, x);
        if (y < grid.size() - 1 && visited.find(down) == visited.end()) { // it isn't the end of the grid and isn't already visited
            neighbors.push_back(down);
        }

        // right
        pair<size_t, size_t> right(y, x+1);
        if (x < grid[0].size() - 1 && visited.find(right) == visited.end()) {
            neighbors.push_back(right);
        }

        // up
        pair<size_t, size_t> up(y-1, x);
        if (y > 0 && visited.find(up) == visited.end()) {
            neighbors.push_back(up);
        }

        // left
        pair<size_t, size_t> left(y, x-1);
        if (x > 0 && visited.find(left) == visited.end()) {
            neighbors.push_back(left);
        }

        for (pair<size_t, size_t> neigh : neighbors) {
            int weight = grid[neigh.second][neigh.first];

            if (distances[node] + weight < distances[neigh]) {
                distances[neigh] = distances[node] + weight;
            }
        }

        queue.erase(it);
    }

    // dump    
    // for (auto const& [key, val] : distances) {
    //     cout << "(" << key.first << ", " << key.second << ") " << val << '\n';
    // }

    const pair<size_t, size_t> goal(grid.size() - 1, grid[grid.size()-1].size() - 1);

    return distances[goal];
}

int main() {
    
    auto grid = getGrid("Input.txt");

    // dump(grid);

    int depth = dijkstra_search(grid);

    cout << "Depth: " << depth << '\n';

    return EXIT_SUCCESS;
}