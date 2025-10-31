#  minimal timing for CPU vs I/O across threads/async/mp
import time, os, random, hashlib, sqlite3, asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from itertools import repeat

DB="mini_time.db"; NCPU=80; NIO=300; CPU_ITERS=15000

def init_db(n=1000):
    con=sqlite3.connect(DB); c=con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS kv(key TEXT PRIMARY KEY, val TEXT)")
    c.executemany("INSERT OR IGNORE INTO kv(key,val) VALUES(?,?)",[(f"k{i}",str(i)) for i in range(n)])
    con.commit(); con.close()

def cpu_task(iters):
    h=b"0"
    for _ in range(iters): h=hashlib.sha256(h).digest()
    return h

def io_task(db,key):
    con=sqlite3.connect(db); c=con.cursor()
    c.execute("SELECT val FROM kv WHERE key=?", (key,)); r=c.fetchone()
    con.close(); return r[0] if r else None

def time_threads(fn, *iterables, workers):
    t=time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as ex: list(ex.map(fn, *iterables))
    return time.perf_counter()-t

def time_mp(fn, *iterables, procs):
    t=time.perf_counter()
    with ProcessPoolExecutor(max_workers=procs) as ex: list(ex.map(fn, *iterables, chunksize=1))
    return time.perf_counter()-t

async def time_async(fn, args_list, workers):
    t=time.perf_counter()
    loop=asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs=[loop.run_in_executor(ex, fn, *args) for args in args_list]
        await asyncio.gather(*futs)
    return time.perf_counter()-t

if __name__=="__main__":
    random.seed(0); init_db()
    keys=[f"k{random.randint(0,999)}" for _ in range(NIO)]
    procs=os.cpu_count() or 4

    # CPU runs
    t_thr=time_threads(cpu_task, repeat(CPU_ITERS, NCPU), workers=8)
    t_mp =time_mp(cpu_task, repeat(CPU_ITERS, NCPU), procs=procs)
    t_async=asyncio.run(time_async(cpu_task, [(CPU_ITERS,)]*NCPU, workers=8))
    print(f"CPU iters={CPU_ITERS}, tasks={NCPU} | threads={t_thr:.3f}s, async={t_async:.3f}s, mp={t_mp:.3f}s")

    # I/O runs
    t_thr=time_threads(io_task, repeat(DB, NIO), keys, workers=32)
    t_mp =time_mp(io_task, repeat(DB, NIO), keys, procs=procs)
    t_async=asyncio.run(time_async(io_task, [(DB,k) for k in keys], workers=64))
    print(f"IO tasks={NIO}         | threads={t_thr:.3f}s, async={t_async:.3f}s, mp={t_mp:.3f}s")