

#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using namespace std;

const int INF = numeric_limits<int>::max();

struct gr {
    int to;      
    int weight;   
};

void Levit(const vector<vector<gr>>& graph, int start, vector<int>& distances) {
    int n = graph.size();
    distances.assign(n, INF);
    distances[start] = 0;

    
    deque<int> fastqueue;   
    queue<int> slowqueue;   
    vector<bool> infast(n, false);
    vector<bool> inslow(n, false);

    fastqueue.push_back(start);
    infast[start] = true;

    while (!fastqueue.empty() || !slowqueue.empty()) {
        int current;
        if (!fastqueue.empty()) {
            current = fastqueue.front();
            fastqueue.pop_front();
            infast[current] = false;
        }
        else {
            current = slowqueue.front();
            slowqueue.pop();
            inslow[current] = false;
        }

        for (const gr& edge : graph[current]) {
            if (distances[edge.to] > distances[current] + edge.weight) {
                distances[edge.to] = distances[current] + edge.weight;

                if (!infast[edge.to]) {
                    if (inslow[edge.to]) {
                        inslow[edge.to] = false;
                    }
                    fastqueue.push_back(edge.to);
                    infast[edge.to] = true;
                }
            }
        }
    }
}

int main() {
    int n = 5;
    vector<vector<gr>> graph(n);

    graph[0] = { {1, 10}, {2, 5} };
    graph[1] = { {2, 2}, {3, 1} };
    graph[2] = { {1, 3}, {3, 9}, {4, 2} };
    graph[3] = { {4, 4} };
    graph[4] = { {3, 6}, {0, 7} };

    


    vector<int> distances;
    Levit(graph, 0, distances);

    cout << "Shortest distances:\n";
    for (int i = 0; i < n; ++i) {
        cout << "To vertex " << i << ": ";
        if (distances[i] == INF) {
            cout << "no path\n";
        }
        else {
            cout << distances[i] << "\n";
        }
    }

    return 0;
}