from jax import numpy,random,jit
numpy.set_printoptions(formatter={"bool": lambda x: "i" if x else ":"})

key = random.PRNGKey(0)

@jit
def mutate(array, key):  # invert a random element of the array
    key, = random.split(key, 1)
    idx = random.randint(key, shape=(1,), minval=0, maxval=array.shape[0])
    array = array.at[idx].set(~array[idx])
    return array,key

step=0
best = random.bernoulli(key, shape=(9,))
bt_count = numpy.sum(best)
while not best.all():
    print(best, step:=step+1)
    candidae,key = mutate(best,key)
    ni_count = numpy.sum(candidae)
    if ni_count > bt_count:
        best = candidae
        bt_count = ni_count
print(best)