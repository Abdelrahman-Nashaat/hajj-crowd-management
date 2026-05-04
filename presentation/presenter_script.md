# Hajj Crowd Management System — Presenter Script

## How to Use This Script
- Each section maps to one slide in `slides.html`
- Estimated total presentation time: **8–10 minutes**
- Practice 2–3 times before presenting
- Keep eye contact with the audience — use this as a backup, not a teleprompter
- The most important slide is **Slide 12** — spend the most time there

---

## Slide 1 — Title (15 seconds)

"Good morning. My name is [Your Name], and today I am presenting my final project for the
Algorithm Design and Analysis course: a Hajj Crowd Management System. This project applies
five classical algorithms from our course to a real, life-or-death engineering problem."

---

## Slide 2 — The Problem (40 seconds)

"Every year, approximately two and a half million Muslims perform Hajj. They all need to
visit the same five holy sites — Masjid Al Haram, Mina, Arafat, Muzdalifah, and Jamarat —
during the same few days, because the Islamic ritual defines a completely fixed schedule.
There is no flexibility in when people move — only in how they move and in what order groups
travel. This combination of massive scale and rigid timing creates extreme, predictable
congestion. And predictable problems have algorithmic solutions."

---

## Slide 3 — Real-World Impact (45 seconds)

"This is not a theoretical exercise. The table on this slide shows three real disasters.
In 1990, a stampede in the Mina tunnel killed over fourteen hundred people. In 2006, the
Jamarat bridge collapsed and over three hundred died. In 2015 — only eleven years ago —
the Mina stampede killed more than two thousand four hundred pilgrims. These are not random
accidents. They are routing and scheduling failures. The wrong groups were in the wrong
place at the wrong time. Computer science and algorithm design exist precisely to solve
these kinds of problems."

---

## Slide 4 — Our Approach (40 seconds)

"We model the Hajj route network as a weighted undirected graph. The five holy sites become
the five nodes. The ten roads connecting them become the ten edges. Each edge carries two
weights: the physical distance in kilometers, and a congestion-aware weight that is
distance multiplied by one plus the road's load percentage. A road at ninety percent load
is treated as much more expensive than a longer but empty road. This graph is the foundation
for all five algorithms. You can see the full network visualization on the right."

---

## Slide 5 — Algorithms Overview (35 seconds)

"We implement five algorithm techniques across three phases. First, graph modeling. Then
Kruskal's Minimum Spanning Tree and Dijkstra's Shortest Path for infrastructure and routing.
And finally, two scheduling algorithms: a greedy heuristic and a dynamic programming solution.
Each one answers a different question about the Hajj network, and each one appears in our
Algorithm Design course curriculum."

---

## Slide 6 — Kruskal's Concept (45 seconds)

"Kruskal's algorithm answers the question: what is the minimum set of roads needed to keep
all five sites connected? The algorithm is elegant. Sort all ten edges by distance. Pick the
cheapest one. If adding it would create a cycle, reject it. Otherwise, add it to the MST.
Repeat until you have four edges — which is N minus one for five nodes. The key data
structure is Union-Find with path compression, which detects cycles in near-constant time.
The result on our network is four edges with a total cost of 21.5 kilometers."

---

## Slide 7 — Kruskal's Result (35 seconds)

"This figure shows the algorithm running step by step. Panel one shows the first edge added:
Mina to Jamarat at 1.5 kilometers — the shortest road in the network. Panel two shows the
first rejection: adding Muzdalifah to Jamarat would form a triangle with Mina — a cycle —
so it is rejected and drawn in red dashed. Panel three shows three edges built up. Panel four
shows the final MST — four green edges, 21.5 kilometers total, connecting all five sites
at minimum cost."

---

## Slide 8 — Dijkstra's Concept (45 seconds)

"While Kruskal answers infrastructure questions, Dijkstra answers routing questions.
Given that we want to send pilgrims from Mina to Jamarat, which path has the lowest
congestion-weighted cost? The edge weight formula — distance times one plus load
percentage — penalizes heavily loaded roads. A road at 90 percent capacity gets a weight
multiplier of 1.9. Dijkstra's algorithm uses a priority queue to always expand the
currently cheapest path, guaranteeing the globally optimal route. We tested the Mina to
Jamarat route specifically because that road has the highest historical death toll."

---

## Slide 9 — Dijkstra's Result (35 seconds)

"The three panels show Dijkstra running step by step. Panel one is the initial state:
Mina starts at distance zero, all others at infinity. Panel two shows the frontier
expanded after processing Mina — we can see the tentative distances for all four
neighboring sites shown in yellow. Panel three shows the result: the direct Mina to
Jamarat edge is the optimal path, with a physical distance of 1.5 kilometers and a
congestion weight of 2.85."

---

## Slide 10 — Scheduling Problem (40 seconds)

"Now for the scheduling phase. We have ten pilgrim groups that must transit the
Mina-Jamarat bottleneck road one at a time. Each group has a size, an urgency level
from one to five — where five means critical, such as elderly or medically vulnerable
pilgrims — and a processing time measured in hours. The objective is to minimize total
weighted waiting time, which is the sum of urgency times wait time for every group.
We compare three strategies: FCFS, Greedy, and Dynamic Programming."

---

## Slide 11 — Greedy vs DP Comparison (40 seconds)

"This figure shows the Gantt chart for all three algorithms side by side. The color of
each bar represents urgency level: red for critical groups, orange for high urgency,
yellow for medium, blue for low, and gray for minimal. Look at the FCFS chart on the
top left: low-urgency groups are scattered throughout, making critical groups wait.
The Greedy chart improves this significantly. But look at the DP chart on the bottom
left — it finds a qualitatively different ordering that the greedy missed. The bar
chart on the bottom right makes the cost difference concrete."

---

## Slide 12 — Key Insight (60 seconds — THE MOST IMPORTANT SLIDE)

"This is the central result of the project. FCFS gives a total weighted wait of 174.
Greedy reduces this to 103.1 — a forty percent improvement. Impressive. But Dynamic
Programming finds 89.8, which is the true mathematical optimum. Greedy is still
fourteen-point-eight percent worse than optimal. Why does greedy fail here? Because
it sorts purely by urgency, ignoring processing time. A highly urgent group with a
very long processing time blocks all subsequent groups for hours. The optimal rule —
which DP rediscovers through exhaustive search — is to sort by urgency divided by
processing time: the weighted shortest processing time rule. Greedy is O of n log n
and runs in milliseconds. DP is O of n times two to the n — it tries all
1024 orderings for our 10 groups. This is the core trade-off of Algorithm Design
and Analysis: speed versus optimality. Greedy is fast but suboptimal. DP is slower
but always correct. There is no free lunch."

---

## Slide 13 — Project Dashboard (30 seconds)

"This dashboard brings all five algorithms together in a single view. Top row: the
full network, the MST overlay, and the Dijkstra path visualization. Bottom row: the
optimal DP schedule as a Gantt chart, the cost comparison, and a summary card with
all key metrics. This is the complete answer to our original question: given the Hajj
holy sites network, how do we build the minimum infrastructure, route pilgrims most
efficiently, and schedule groups optimally? Five algorithms, one project."

---

## Slide 14 — Thank You (15 seconds)

"Thank you for your attention. I am happy to answer any questions about the algorithms,
the data, or the implementation."

---

## Tips for the Q&A

**Q: Why did you choose these specific 10 pilgrim groups?**
"The group properties were chosen deliberately so that greedy is provably suboptimal —
specifically, groups with high urgency but very long processing times create the
counterexample. Without this design, a greedy algorithm might accidentally give the
optimal answer and the comparison would be uninteresting."

**Q: Why MST if Dijkstra already gives shortest paths?**
"They answer different questions. MST asks: what is the minimum road network to build
so all sites are reachable? Dijkstra asks: given the existing network, what is the
best route for a single trip? MST is an infrastructure planning tool; Dijkstra is a
routing tool. Both matter."

**Q: Is the data real?**
"All distances, capacities, and congestion levels are simulated for academic purposes,
inspired by published Hajj statistics. The algorithms are real and the conclusions
about relative performance hold regardless of the exact data values."

**Q: What about Divide and Conquer?**
"The bitmask DP is implicitly divide and conquer: it solves the optimal scheduling
problem for every subset of groups, building up from smaller subsets to the full set.
Each state depends on strictly smaller subsets — that is divide and conquer applied
to combinatorial search."

**Q: Does the DP scale?**
"For n = 10 groups, 2 to the 10 is only 1024 states — it runs in milliseconds.
For n = 20, it would be one million states, still feasible. For n = 30, about one
billion — that becomes impractical. In practice, scheduling at this scale uses
approximation algorithms or branch-and-bound, which are topics for a graduate
algorithms course."
