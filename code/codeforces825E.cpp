#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<vector<int>> adj(n + 1);
    vector<int> in_degree(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[v].push_back(u);
        in_degree[u]++;
    }

    priority_queue<int> pq;

    for (int i = 1; i <= n; i++) {
        if (in_degree[i] == 0) {
            pq.push(i);
        }
    }

    vector<int> label(n + 1);
    int current_label = n;

    while (!pq.empty()) {
        int u = pq.top();
        pq.pop();

        label[u] = current_label;
        current_label--;

        for (int v : adj[u]) {
            in_degree[v]--;
            if (in_degree[v] == 0) {
                pq.push(v);
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        cout << label[i] << (i == n ? "" : " ");
    }
    cout << "\n";

    return 0;
}