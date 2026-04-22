# 134084423
def main():
    # ヽ(´▽`)/
    robots = sorted(list(map(int, input().split())))
    limit = int(input())
    left_pointer = 0
    right_pointer = len(robots) - 1
    result = 0
    while left_pointer <= right_pointer:
        if robots[right_pointer] == limit:
            right_pointer -= 1
            result += 1
        elif robots[left_pointer] == limit:
            left_pointer += 1
            result += 1
        elif robots[left_pointer] + robots[right_pointer] <= limit:
            right_pointer -= 1
            left_pointer += 1
            result += 1
        elif robots[right_pointer] <= limit:
            right_pointer -= 1
            result += 1
        elif robots[left_pointer] <= limit:
            left_pointer += 1
            result += 1
    return result

if __name__ == '__main__':
    print(main())
