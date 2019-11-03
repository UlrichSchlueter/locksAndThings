import consul

c = consul.Consul()


# in another process
c.kv.put('foo', 'bar')
