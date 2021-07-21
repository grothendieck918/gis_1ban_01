def decorator(func):
    def decorated(input_text):
        print('start')
        func(input_text)
        print('end')
    return decorated

def decorator2(func):
    def decorated(w, h, user):
        if not (w > 0 and h > 0):
            raise ValueError('Input must be positive value')
        return func(w,h,user)

    return decorated

def decorator3(func):
    def decorated(w, h, user):
        if user.is_authenticated:
            return func(w,h,user)
        else:
            raise PermissionError('loing required')

    return decorated

class User:
    def __init__(self,a):
        self.is_authenticated = a



@decorator
def hello_world(input_text):
    print(input_text)

@decorator2
@decorator3
def tri_area(w,h, user):
    return w*h/2

@decorator2
@decorator3
def sq_area(w,h, user):
    return w*h

user1 = User(False)

hello_world('hello world!')

s1=sq_area(2 ,4 , user1)

print(s1)




