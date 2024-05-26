from collections import Counter
import heapq
import timeit

def find_coins_greedy(rest_sum: int, available_coins: list) -> dict:
    """Greedy algorithm for finding rest coins"""
    rest_coins = {}
    # init coins max heap
    coins_heap = []
    for cv in available_coins:
        heapq.heappush(coins_heap, -cv)
    
    while rest_sum > 0:
        coin = -heapq.heappop(coins_heap)
        coins = rest_sum // coin
        if coins == 0:
            continue
            
        rest_coins[coin] = coins
        rest_sum -= coins * coin

    return rest_coins

def find_min_coins(rest_sum: int, available_coins: list) -> dict:
    """Dinamic algorithm"""
    rest_map = {}
    return recursive_find_min_coins(rest_sum, available_coins, rest_map)

def recursive_find_min_coins(rest_sum: int, available_coins: list, rest_map: dict) -> dict:
    """Dinamic algorithm: recursive function with memorization"""
    if rest_sum in rest_map:
        return rest_map[rest_sum]
    
    variants = {}
    for coin in available_coins:
        if coin > rest_sum:
            continue
        if coin == rest_sum:
            rest_map[rest_sum] = {'count': 1, 'coins': {coin: 1}}
            return rest_map[rest_sum]
        
        variants[coin] = recursive_find_min_coins(rest_sum - coin, available_coins, rest_map)
        if variants[coin] is None:
            variants.pop(coin)

    if len(variants) == 0:
        return None
    
    best_coin = min(variants, key=lambda x: variants[x]['count'])
    rest_coins = variants[best_coin].copy()
    rest_coins['count'] += 1
    rest_coins['coins'] = dict(Counter(rest_coins['coins']) + Counter({best_coin: 1}))

    rest_map[rest_sum] = rest_coins
    return rest_coins

if __name__ == "__main__":
    coins = [50, 25, 10, 5, 2, 1]

    for rest_sum in [113, 7913, 15226, 15226234]:
        print(f"Rest sum is {rest_sum}")
        print(f"Greedy:  Rest coins {find_coins_greedy(rest_sum, coins)}")
        print(f"Dinamic: Rest coins {find_min_coins(rest_sum, coins)['coins']}")

        greedy_t = timeit.timeit('find_coins_greedy(rest_sum, coins)', number=20, globals=globals())/20.0
        dinamic_t = timeit.timeit('find_min_coins(rest_sum, coins)', number=20, globals=globals())/20.0
            
        print(f"Analyze time: for greedy algorithm {greedy_t:.9f} and for dinamic algorithm {dinamic_t:.9f}\n")
            
