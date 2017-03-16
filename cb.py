from functools import wraps
from datetime import datetime, timedelta
import redis


class CircuitBreaker(object):
    def __init__(self, name=None, expected_exception=Exception, max_failure_to_open=3, reset_timeout=10):
        self._name = name
        self._expected_exception = expected_exception
        self._max_failure_to_open = max_failure_to_open
        self._reset_timeout = reset_timeout
        self.host2failcount_dict={}
        self.close()

    def close(self):
        self._is_closed = True
        self._failure_count = 0

    def open(self, address):
        r = redis.Redis('127.0.0.1')
        r.lrem('activeServer', address, num=0)
        self.host2failcount_dict[address] = 0

    def can_execute(self):
        if not self._is_closed:
            self._open_until = self._opened_since + timedelta(seconds=self._reset_timeout)
            self._open_remaining = (self._open_until - datetime.utcnow()).total_seconds()
            return self._open_remaining <= 0
        else:
            return True

    def __call__(self, func, *args, **kwargs):
        if self._name is None:
            self._name = func.__name__
            print "Initial Failure count is: ",self._failure_count

        @wraps(func)
        def with_circuitbreaker(*args, **kwargs):
            return self.call(func, *args, **kwargs)

        return with_circuitbreaker

    def call(self, func, *args, **kwargs):
        address=args[args.__len__()-1]
        if not self.can_execute():
            err = 'CircuitBreaker[%s] is OPEN until %s (%d failures, %d sec remaining)' % (
                self._name,
                self._open_until,
                self._failure_count,
                round(self._open_remaining)
            )
            raise Exception(err)

        try:
            value = func(*args, **kwargs)
            self.host2failcount_dict[address]=0
            print "Current Failure after is: ", self.host2failcount_dict[address]
        except self._expected_exception:

            if address in self.host2failcount_dict:
                self.host2failcount_dict[address]= self.host2failcount_dict[address] + 1
            else:
                self.host2failcount_dict[address]=1
            	print "Current Failure count is: ", self.host2failcount_dict[address]
	    if self.host2failcount_dict[address] >= self._max_failure_to_open:
                self.open(address)            
            raise self._expected_exception

        self.close()
        return value
