from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        We update key/value pair but following open addressing.
        '''
        # This if condition is for resizing purposes.
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        hash = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(hash) != None:
            j = 1
            quad_probing = hash
            # This loop checks to see if the key exist or not and make appropriate changes.
            while self._buckets.get_at_index(quad_probing):
                if self._buckets.get_at_index(quad_probing).key == key:
                    # We also need to check if the tombstone exist or not.
                    if not self._buckets.get_at_index(quad_probing).is_tombstone:
                        self._buckets.set_at_index(quad_probing, HashEntry(key, value))
                    else:
                        self._size += 1
                        self._buckets.set_at_index(quad_probing, HashEntry(key, value))
                        self._buckets.get_at_index(quad_probing).is_tombstone = False
                    return
                # Updates the quad probing in the while loop using a formula from module.
                quad_probing = (hash + j**2) % self._capacity
                j += 1
            self._buckets.set_at_index(quad_probing, HashEntry(key, value))
            self._size += 1
        else:
            self._size += 1
            self._buckets.set_at_index(hash, HashEntry(key, value))

    def table_load(self) -> float:
        '''
        We return the load factor here.
        '''
        # Formula from the module.
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        '''
        We check to see how many empty buckets there are.
        '''
        # Formula to check how many empty buckets there are.
        counter = self._capacity - self._size
        return counter

    def resize_table(self, new_capacity: int) -> None:
        '''
        We resize the table but following open addressing rules.
        '''
        # The two if statements are conditions for resizing.
        if new_capacity <= self._size:
            return
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)
        else:
            pass
        # Create a new hashmap that will be are updated hashmap.
        another_HashMap = HashMap(new_capacity, self._hash_function)
        # If the bucket does exist, then we add accordingly, otherwise leave it alone.
        for a in self:
            if a:
                another_HashMap.put(a.key, a.value)
        self._size = another_HashMap._size
        self._capacity = another_HashMap.get_capacity()
        self._buckets = another_HashMap._buckets

    def get(self, key: str) -> object:
        '''
        We get the value that is associated with the inputted key.
        '''
        for a in self:
            if a:
                # We need to make sure that it is not a tombstone and the key exist in order to return.
                # Otherwise we just pass.
                if a.is_tombstone == False and a.key == key:
                    return a.value
                else:
                    pass
            else:
                pass
        return None

    def contains_key(self, key: str) -> bool:
        '''
        We check if the key exist or not and return True if it does (follows open addressing rules).
        '''
        for a in self:
            if a:
                # We follow the same logic as the method above, we need to check if it is a tombstone or not.
                # Otherwise we just pass.
                if a.is_tombstone == False and a.key == key:
                    return True
                else:
                    pass
            else:
                pass
        return False

    def remove(self, key: str) -> None:
        '''
        We remove the key and the associated value but following open addressing rules.
        '''
        for a in self:
            if a:
                # Follows the same logic and checks if it is a tombstone first in order to remove.
                if a.is_tombstone == False and a.key == key:
                    self._size -= 1
                    # We make the removal by making it a tombstone.
                    a.is_tombstone = True
                else:
                    pass
            else:
                pass

    def clear(self) -> None:
        '''
        We clear the Hashmap  contents.
        '''
        self._buckets = DynamicArray()
        for a in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        '''
        We return an array with a key/value tuple.
        '''
        new_array = DynamicArray()
        for a in self:
            # Need to make sure what we are iterating isn't a tombstone first.
            if a.is_tombstone == False and a:
                new_array.append((a.key, a.value))
            else:
                pass
        return new_array

    def __iter__(self):
        '''
        Enables us to iterate for this project.
        '''
        self._index = 0
        return self

    def __next__(self):
        '''
        Will return the next item in the hashmap.
        '''
        # The following code implementation is similar to the module lesson.
        try:
            value = None
            for a in range(self._capacity):
                if value == None or value.is_tombstone == True:
                    value = self._buckets.get_at_index(self._index)
                    self._index += 1
                else:
                    pass
        except DynamicArrayException:
            raise StopIteration
        return value


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
