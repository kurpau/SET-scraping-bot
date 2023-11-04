import os

class CacheManager:
    def _write_cache(self, cache):
        cache_path = os.path.join(os.getcwd(), "cache.txt")
        with open(cache_path, "a") as f:
            for stock_id, (eps_values, stock_name) in cache.items():
                f.write(f"{stock_id}|{eps_values[0]}|{eps_values[1]}|{stock_name}\n")

    def _read_cache(self):
        cache_path = os.path.join(os.getcwd(), "cache.txt")
        if not os.path.exists(cache_path):
            return {}
        with open(cache_path, "r") as f:
            data = f.readlines()
        cache = {}
        for line in data:
            parts = line.strip().split("|")
            stock_id, curr_eps, prev_eps, stock_name = parts
            if curr_eps == "None" or prev_eps == "None":
                cache[stock_id] = (None, stock_name)
            else:
                cache[stock_id] = ([float(curr_eps), float(prev_eps)], stock_name)
        return cache
    
