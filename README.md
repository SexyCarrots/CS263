# Python Concurrency on macOS: Threads vs Async vs Multiprocessing under the GIL

CS263 Project by Xinghan Yang
## Specs
 - **Machine:** Apple Silicon (a.k.a. my laptop) 
 - **Endpoint:** `POST /score` → request `{"mode":"cpu"| "GIL", "TBD"}` → response  
 - **Deliverables:** mini-survey of GIL & models, reproducible results with scripts, visualization of result, 5-page PDF, 10–15 min video, slides 
 - **Weekly Progress check Commits:** every Fri ~5pm PT 
 - *Final due:* **Tue Dec 9, 11:59pm PT**

## Overview, Goals, Questions, Hypotheses
**Goal:** Show how Python concurrency models behave on Apple Silicon for two types of workloads: 
 1. **CPU-bound** (SHA-256 chaining, pure Python) 
 2.  **I/O-bound** (SQLite KV GET).  

**Research questions:** 
 1. Throughput & p50/p95/p99 latency across **threads / asyncio / multiprocessing** 
 2.  Does **async** improve tail latency at higher concurrency vs threads? 
**Hypotheses:** CPU-bound → threads/async plateau due to GIL; **multiprocessing** wins for moderate+ task sizes. I/O-bound → **asyncio** best tail latency at high concurrency; threads competitive at moderate; mp overkill. Memory → threads ≲ asyncio ≪ mp. Energy (opt.) → mp highest under CPU; async most efficient when I/O-wait dominated.

## Repository Structure

```
#TODO
```

> **API contract:** #TODO

## Tools & Setup
**Python & libs:** Python 3.12+ (Apple Silicon), `Flask` (threads + mp), `aiohttp` (async), optional `uvloop`, `sqlite3` / `aiosqlite`, `orjson` (fast JSON), `matplotlib`, `pandas`.  
**Bench & system tools:** `wrk` (primary), `hyperfine` (sanity), `/usr/bin/time -l` (RSS/page faults), optional `powermetrics` (energy), `jq` (CLI JSON).  
**Install:**
```bash
brew install wrk hyperfine jq
python3 -m venv .venv && source .venv/bin/activate
pip install flask aiohttp uvicorn uvloop orjson aiosqlite matplotlib pandas
```

## System Design (Our code)

**Interchangeable backends:**
 - WIP


**Workloads:**
 - CPU: SHA-256 chaining, tunable iters ∈ {80k, 150k, 300k}
 - I/O: SQLite SELECT val FROM kv WHERE key=? (1k? keys, random access)

**Fairness/Environment controls for reproducibility:**

Result CSV schema: TBD


Evaluation Plan (Tbale/Plots): TBD


## Timeline (Week 6 → Week 9, final due Dec 9)

**Rule: push at leaset one substantial commit by every Friday ~5pm PT.**
**Week 5 - Beginning:**
 - [x] Brainstormed the overall plan for the project
 - [x] Narrow down the scope of work and chose the Tech Stack
 - [x] Finished the `README` with a clear abstract and timeline
 - [x] Configure the environment and prototyped the minimal experiment


**Week 6 — Foundations:** 
 - [ ] Scaffold repo , add more to README.md, requirements.txt (env)
 - [ ] Implement one mode (threads or async) with score/metrics (CPU + I/O)
 - [ ] db/setup_db.py to build db/test.db 
 - [ ] Smoke tests:  baseline
 - [ ] Deliverables : minimal server running, DB ready, draft bench scripts, baseline p50/p95/p99 snippet

**Week 7 - Backends & First Benchmark:**
- [ ] Add remaining modes: threads, asyncio, mp (unified API, mode switch)
- [ ] Launch scripts: run_threads.sh, run_async.sh ..
- [ ] Bench each mode: Get the result with metrics
- [ ] Deliverables (Fri Nov 7): all modes runnable; first benchmark with CPU+I/O  different modes(GIL/..
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
)
  
**Week 8 - TBD:**
- [ ] TBD
  
**Week 9 - TBD:**
- [ ] TBD

**Week 10~Finals - TBD:**
- [ ] TBD
