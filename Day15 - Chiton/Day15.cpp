// https://adventofcode.com/2021/day/15
// clear && g++ -Wall -Wextra -Werror -std=c++20 -o Day15.out ./Day15.cpp && ./Day15.out

#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
#include <deque>
#include <queue>
#include <set>
#include <map>
#include <climits>
#include <unordered_set>
#include <string>

using namespace std;

struct Node {
    size_t x;
    size_t y;
    size_t weight;
    size_t distance;
    bool visited;

    Node(const int x, const int y, const int weight)
        : x(x), y(y), weight(weight), distance(INT_MAX), visited(false) {};
};

ostream& operator<< (ostream& os, const Node* node) {
    return os << "(x: " << node->x << ", y: " << node->y << ", w: " << node->weight << ", " << (node->visited ? "visited" : "unvisited") << ")";
}


struct Grid {
    vector<vector<Node>> nodes;

    Grid(const string &filename) : nodes() {
        string line;
        ifstream file;
        file.open(filename);

        vector<vector<Node>> lines;
        size_t y = 0;
        while (getline(file, line)) {
            vector<Node> row;

            for (size_t x = 0; x < line.size(); ++x) {
                char c = line[x];
                int weight = c - '0';

                Node node(x, y, weight);

                row.push_back(node);
            }

            lines.push_back(row);
            ++y;
        }

        file.close();

        this->nodes = lines;
    }

    void dump() {
        for (vector<Node> row : this->nodes) {
            for (Node n : row) {
                cout << (n.visited ? "*" : to_string(n.weight));
            }
            cout << '\n';
        }
    }

    void engorge() {
        vector<vector<Node>> result;
        vector<vector<Node>> first = this->nodes; // get the initial section
        size_t section_height = first.size();
        size_t section_width = first[0].size();

        for (int i = 0; i < 5; ++i) { // repeat the secionts five times
            vector<vector<Node>> new_first; // the next row of sections will start from this template

            for (vector<Node> line : first) { // repeat the template line-by-line
                vector<Node> full_line; // the completed line
                vector<Node> new_first_line; // the new line of the next template
                
                for (Node n : line) {
                    full_line.push_back(n); // push the first section through to the final line

                    Node next(n);
                    next.weight = n.weight+1 > 9 
                        ? 1 
                        : n.weight+1;
                    next.y += section_height; // add the sections worth of x-values

                    new_first_line.push_back(next); // the next first line will have this value
                }

                vector<Node> prev = line;
                for (int j = 1; j < 5; ++j) { // repeat the first section and increase the weights
                    vector<Node> new_prev;

                    for (Node n : prev) {
                        Node next(n);
                        next.weight = n.weight+1 > 9 ? 1 : n.weight+1;
                        next.visited = false;
                        next.x += section_width; // increase the x by the section size

                        full_line.push_back(next);
                        new_prev.push_back(next);
                    }

                    prev = new_prev;
                }
                
                result.push_back(full_line);
                new_first.push_back(new_first_line);
            }

            first = new_first;
        }

        this->nodes = result;
    }

    vector<Node*> unvisited_neighbors(const Node *node) const {
        vector<Node*> neighbors;

        // down
        if (node->y < this->nodes.size() - 1 && !(this->nodes[node->y + 1][node->x]).visited) {
            neighbors.push_back(
                const_cast<Node *>(&this->nodes[node->y + 1][node->x])
            );
        }

        // right
        if (node->x < this->nodes[node->y].size() - 1 && !this->nodes[node->y][node->x+1].visited) {
            neighbors.push_back(
                const_cast<Node *>(&this->nodes[node->y][node->x+1])
            );
        }

        // up
        if (node->y > 0 && !this->nodes[node->y-1][node->x].visited) {
            neighbors.push_back(
                const_cast<Node *>(&this->nodes[node->y-1][node->x])
            );
        }

        // left
        if (node->x > 0 && !this->nodes[node->y][node->x-1].visited) {
            neighbors.push_back(
                const_cast<Node *>(&this->nodes[node->y][node->x-1])
            );
        }

        return neighbors;
    }

    Node* first() const {
        return const_cast<Node*>(&(this->nodes[0][0]));
    }

    int result() const {
        vector last_row = this->nodes[this->nodes.size() - 1];
        Node last = last_row[last_row.size() - 1];

        return last.distance;
    }
};

int dijkstra_search(const Grid &grid) {
    deque<pair<Node*, size_t>> queue;

    Node* first = grid.first();
    pair<Node*, size_t> start(first, 0);
    queue.push_back(start);

    auto comparer = [](pair<Node*,size_t> &a, pair<Node*, size_t> &b)
    {
        return a.second < b.second;
    };

    while (!queue.empty()) {
        sort(queue.begin(), queue.end(), comparer);

        // get the node
        pair<Node*, size_t> next = queue.front();
        queue.pop_front();

        Node* node = next.first;
        size_t distance = next.second;

        if (node->y == grid.nodes.size() - 1 && node->x == grid.nodes[grid.nodes.size() - 1].size() - 1) {
            return distance;
        }

        if (node->visited) {
            continue; // skip already visited nodes
        }

        node->visited = true;

        for (Node *neigh : grid.unvisited_neighbors(node)) {
            size_t new_distance = distance + neigh->weight;

            if (new_distance < neigh->distance) {
                neigh->distance = new_distance;

                pair<Node*, size_t> p(neigh, new_distance);
                queue.push_back(p);
            }
        }

        if (queue.empty()) {
            cout << "empty queue\n";
        }
    }

    return grid.result();
}

int main() {
    
    Grid grid("Input.txt");

    // grid.dump();

    grid.engorge();

    int depth = dijkstra_search(grid);

    // grid.dump();

    cout << "Depth: " << depth << '\n';

    return EXIT_SUCCESS;
}
