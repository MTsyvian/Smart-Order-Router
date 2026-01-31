# High-Frequency Smart Order Router (HFT Ecosystem)

## Overview
This project is an institutional-grade **Smart Order Routing (SOR)** system designed to optimize liquidity execution across fragmented markets.

The system simulates a full-stack trading infrastructure where:
1.  **Core Engine (C)** handles ultra-low latency execution and graph-based routing.
2.  **Dashboard (Java)** provides real-time visualization and system control.
3.  **Analytics (Python)** generates predictive signals using Machine Learning.

**Key Objective:** To minimize slippage and toxic flow execution using **Min-Cost Max-Flow** algorithms augmented by **ML signals**.

---

## Target Architecture (The Stack)

### 1. Core Execution Engine (Planned)
* **Language:** C (C11/C17 standard) for deterministic latency.
* **Role:** The "Muscle" of the system.
* **Key Features:**
    * **Graph Theory:** Implementation of the **Min-Cost Max-Flow** algorithm to route orders through the most liquid and cheapest paths.
    * **Low Latency:** Direct memory management (no GC), bitwise optimizations, and O(1) ML inference.
    * **IPC:** Communication with the UI via **TCP Sockets** or **Shared Memory**.

### 2. Quantitative Research (Implemented)
* **Language:** Python (Pandas, Scikit-Learn).
* **Role:** The "Brain" of the system.
* **Key Features:**
    * Market Data Mining (Binance L1 Order Book).
    * **Linear Regression Model:** Predicts short-term price shifts based on Order Book Imbalance.
    * **Coefficient Extraction:** Generates `WEIGHT` and `BIAS` parameters for the C-engine.

### 3. Trader Dashboard (Planned)
* **Language:** Java.
* **Role:** The "Face" of the system.
* **Key Features:**
    * Real-time visualization of the Routing Graph.
    * Live PnL (Profit and Loss) monitoring.
    * Manual overrides (Start/Stop/Emergency Kill Switch).

---

## The Math: ML-Driven Optimization (Implemented)
The core innovation of this router is the integration of a predictive signal into the graph weights.

We calculate the **Normalized Imbalance ($I$)**:
$$I = \frac{Q_{bid} - Q_{ask}}{Q_{bid} + Q_{ask}}$$

The engine applies a dynamic penalty/bonus to exchange nodes based on the prediction:
$$\Delta P = (I \times \text{WEIGHT}) + \text{BIAS}$$

### Why Linear Regression?
In HFT, latency is the bottleneck. Deep Learning models (LSTM/Transformers) are too slow for nanosecond-level execution.
* **Neural Network Inference:** ~1-5 ms.
* **Linear Regression Inference:** ~10-50 ns.
We sacrifice complex pattern matching for **speed**, gaining a statistical edge without introducing latency overhead.

---
## ⚙️ Core Architecture: The Routing Graph (Planned)
The C-engine models the fragmented crypto market as a **Weighted Directed Graph**, where:
* **Nodes ($V$):** Exchanges (Binance, Bybit, OKX) and Intermediary assets (USDT, BTC).
* **Edges ($E$):** Trading pairs with associated costs (Trading Fee + Latency + Slippage).

### The Cost Function
Each edge in the graph has a dynamic weight $W$ representing the total cost of execution. The engine aims to find a path where $\sum W$ is minimal.

The weight formula combines static fees with our ML predictions:
$$W_{total} = C_{fee} + C_{latency} + P_{slippage} + \Delta P_{ML}$$

Where:
* $C_{fee}$: Maker/Taker fees (e.g., 0.1%).
* $C_{latency}$: Network RTT normalized to cost.
* $\Delta P_{ML}$: **The predictive penalty** calculated by our Linear Regression model.
    * *If the model predicts a price drop, the "cost" to buy increases, forcing the router to wait or switch venues.*

### Algorithm: Min-Cost Max-Flow
To route large orders without moving the market, we treat liquidity as a "flow" problem.
Instead of a simple Dijkstra (shortest path), we plan to implement a **Min-Cost Max-Flow** algorithm (e.g., Successive Shortest Path using SPFA or Bellman-Ford) to split the order volume across multiple optimal paths simultaneously.

---
## User Interface: The Trader's Cockpit (Planned)
While the C-engine runs headless in the background, the **Java Dashboard** serves as the command center for the operator.

I chose **Java (JavaFX)** for the frontend to ensure robust, cross-platform performance and strict separation of concerns.

### Architecture: Decoupled UI
The system follows a client-server model:
* **The Server (C Engine):** Pushes high-frequency telemetry via TCP Sockets / IPC (Inter-Process Communication).
* **The Client (Java UI):** Listens for updates and renders them at 60 FPS without blocking the critical trading thread.

*Why this matters?* If the UI crashes due to a rendering bug, the C-engine continues to manage positions safely. The trading logic is immune to GUI lags.
---
### Roadmap
Phase 1: Quantitative Research (Data & ML) (done)

Phase 2: C Engine Core (Graph Structs, Memory Allocators) (work in progress)

Phase 3: Networking (Socket Server implementation) (planned)

Phase 4: Java GUI (Dashboard & Charts) (planned)

Disclaimer: This project is for educational purposes. It demonstrates high-performance software architecture and quantitative finance concepts.
---
## 📂 Repository Structure

```text
├── research/           # ✅ [Python] Data Mining & ML Training
│   ├── data_collector.py
│   └── ML_Unit.py 
│
└── README.md
