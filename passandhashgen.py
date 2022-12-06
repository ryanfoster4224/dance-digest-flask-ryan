import hashlib
import uuid


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.


pw = '4yFG5byD88'
pw = my_random_string(10)
print(pw)
# encode it to bytes using UTF-8 encoding
message = b"Some text to hash"
hash = ("SHA-256:", hashlib.sha256(pw.encode()).hexdigest())
print(hash[1])
