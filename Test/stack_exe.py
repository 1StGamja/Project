# Stack 클래스 정의
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not bool(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

# Stack 객체 생성
s = Stack()

# Stack에 아이템 추가
s.push("item 1")
s.push("item 2")
s.push("item 3")

# Stack에서 아이템 제거 및 반환
print(s.pop())  # "item 3"
print(s.pop())  # "item 2"
print(s.pop())  # "item 1"
