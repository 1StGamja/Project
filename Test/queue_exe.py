import queue

# Queue 객체 생성
q = queue.Queue()

# Queue에 아이템 추가
q.put("item 1")
q.put("item 2")
q.put("item 3")

# Queue에서 아이템 제거 및 반환
print(q.get())  # "item 1"
print(q.get())  # "item 2"
print(q.get())  # "item 3"
