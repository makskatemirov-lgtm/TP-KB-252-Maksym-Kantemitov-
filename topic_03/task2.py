def test_list_methods():
    numbers = [10, 20, 30]
    
    numbers.append(40)
    numbers.extend([50, 60])
    numbers.insert(1, 15)
    numbers.remove(30)
    numbers.reverse()
    numbers.sort()
    
    numbers_copy = numbers.copy()
    numbers.clear()