from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        '''
        We update the key/value pair in the hash map following specific conditions.
        '''
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)
        hash = self._hash_function(key) % self._buckets.length()
        chaining = self._buckets.get_at_index(hash)
        # Check if the key exist or not and make the necessary changes.
        if chaining.length() != 0:
            # Iterate through the bucket to see if the key is there or not.
            for a in chaining:
                if a.key == key:
                    chaining.remove(key)
                    chaining.insert(key, value)
                    return
                else:
                    pass
            chaining.insert(key, value)
            self._size += 1
        # There is nothing at that spot so we can just insert the key, value
        else:
            chaining.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        '''
        Tell us how many empty buckets there are.
        '''
        counter = 0
        # Iterate through the hashmap and if the bucket length is 0, we increase the counter.
        for a in range(self._capacity):
            if self._buckets.get_at_index(a).length() == 0:
                counter += 1
            else:
                pass
        return counter

    def table_load(self) -> float:
        '''
        Gives us the load factor.
        '''
        # Formula from module
        load_factor = self._size / self._capacity
        return load_factor
    def clear(self) -> None:
        '''
        Clears the hashmap contents.
        '''
        self._buckets = DynamicArray()
        self._size = 0
        # We are adding linkedlist because we want to make sure that the buckets have the ability to add more than
        # one key/value pair.
        for a in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        '''
        Resizes the table if certain conditions are met.
        '''
        # The following two if statements are conditions for resizing.
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)
        else:
            pass
        another_HashMap = HashMap(new_capacity, self._hash_function)
        # We iterate through the hashmap here and add the contents to our "another_hashmap"
        for a in range(self._capacity):
            # We don't do anything at this if statement cause there is nothing to add.
            if self._buckets.get_at_index(a).length() == 0:
                pass
            elif self._buckets.get_at_index(a).length() > 0:
                for b in self._buckets.get_at_index(a):
                    another_HashMap.put(b.key, b.value)
        self._size = another_HashMap._size
        self._capacity = another_HashMap._capacity
        self._buckets = another_HashMap._buckets

    def get(self, key: str):
        '''
        We get the value that is attached to the key input.
        '''
        hash = self._hash_function(key) % self._capacity
        chaining = self._buckets.get_at_index(hash)
        # We use a loop to check if the key is there only if there is something in the bucket.
        # Pass if there is nothing in the bucket because there is nothing to check.
        if chaining.length() != 0:
            for a in self._buckets.get_at_index(hash):
                if a.key == key:
                    return a.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        '''
        Checks if the key exist in the hash map or not.
        '''
        for a in range(self._capacity):
            if self._buckets.get_at_index(a).length() == 0:
                pass
            # since there is something in the bucket, then we check if the key is there or not.
            else:
                for b in self._buckets.get_at_index(a):
                    if b.key == key:
                        return True
        return False

    def remove(self, key: str) -> None:
        '''
        Removes the key and the value associated with it.
        '''
        for a in range(self._capacity):
            if self._buckets.get_at_index(a).length() == 0:
                pass
            # Since there is something in the bucket, we use a loop to check for the key and remove if there.
            else:
                for b in self._buckets.get_at_index(a):
                    if b.key == key:
                        self._buckets.get_at_index(a).remove(key)
                        self._size -= 1
                    else:
                        pass
    def get_keys_and_values(self) -> DynamicArray:
        '''
        return a key/value tuple in a dynamic array if it is there.
        '''
        # Initialize a new array to store the pairs that we want returned.
        new_array = DynamicArray()
        for a in range(self._capacity):
            if self._buckets.get_at_index(a).length() == 0:
                pass
            # Since there is something in the bucket, we add it to the new array we created.
            else:
                for b in self._buckets.get_at_index(a):
                    new_array.append((b.key, b.value))
        return new_array

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    '''
    returns a tuple which contains the mode values of the given array.
    '''
    new_map = HashMap()
    # The for loop will be used to obtain the necessary data that will be stored in an array as a tuple
    for i in range(da.length()):
        if new_map.contains_key(da.get_at_index(i)) == True:
            new_map.put(da.get_at_index(i), new_map.get(da.get_at_index(i))+1)
        else:
            new_map.put(da.get_at_index(i),1)
    # We create the array with the tuples and initialize dyanamic array.
    array = new_map.get_keys_and_values()
    new_array = DynamicArray()
    frequency = 0
    # This for loop will be used to check for frequency which will tell us the mode values.
    for i in range(array.length()):
        if array.get_at_index(i)[1] > frequency:
            frequency = array.get_at_index(i)[1]
    # This for loop will add the mode values to an array that will be displayed with frequency in the output.
    for i in range(array.length()):
        if array.get_at_index(i)[1] == frequency:
            new_array.append(array.get_at_index(i)[0])
    return new_array, frequency



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
