import multiprocessing as mp

def job(x, q):
    result = x
    for i in range(10):
        result += i
    print(result)
    q.put(result)

# 使用 multiprocessing 須在 main 裡面用
if __name__=='__main__':
    q = mp.Queue()   # 使用 queue 接收 function 的回傳值
    p1 = mp.Process(target=job, args=(55, q)) # 特別注意 這邊的傳入參數只有一個的話，後面要有逗號
    p2 = mp.Process(target=job, args=(33, q))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(q.qsize())
    ans = [ q.get() for x in range(q.qsize())]
    print(ans)
    #res1 = q.get()
    #res2 = q.get()

    #print(res1)      # 45
    #print(res2)      # 45
    #print(res1+res2) # 90
