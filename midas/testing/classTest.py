class Parent(object):
  def __init__(self, raw):
    self.raw = raw

  def __repr__(self):
    return '{name}{raw}'.format(
      name=self.__class__.__name__,
      raw=self.raw,
    )

class Child(Parent):
  pass

def main():
  c = Child('adi')
  print('c', c)

if __name__ == '__main__':
  main()