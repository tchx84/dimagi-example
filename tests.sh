#!/usr/bin/env bash

#test 00: testing if receiving the proper response content
content=$(curl --silent --get --data-urlencode "values=[1, 2, 3]" http://127.0.0.1:8888/)
expected="{\"sum\": 6, \"product\": 6}"

# XXX this test will fail when the keys order changes
if [ "$content" == "$expected" ]; then
    echo "test 00: passed"
else
    echo "test 00: failed"
fi

# test 01: testing when everything is fine
response=$(curl --write-out %{http_code} --silent --output /dev/null --get --data-urlencode "values=[1, 4, 7, -2]" http://127.0.0.1:8888/)

if [ $response == 200 ]; then
    echo "test 01: passed"
else
    echo "test 01: failed"
fi

# test 02: testing when missing the "values" params
response=$(curl --write-out %{http_code} --silent --output /dev/null --get http://127.0.0.1:8888/)

if [ $response == 400 ]; then
    echo "test 02: passed"
else
    echo "test 02: failed"
fi

# test 03: testing when the content of "values" is not JSON valid
response=$(curl --write-out %{http_code} --silent --output /dev/null --get --data-urlencode "values=notvalid" http://127.0.0.1:8888/)

if [ $response == 400 ]; then
    echo "test 03: passed"
else
    echo "test 03: failed"
fi

# test 04: testing when one element of the list is not a number
response=$(curl --write-out %{http_code} --silent --output /dev/null --get --data-urlencode "values=[1, 2, "a"]" http://127.0.0.1:8888/)

if [ $response == 400 ]; then
    echo "test 04: passed"
else
    echo "test 04: failed"
fi

# test 05: testing when the list is empty.
response=$(curl --write-out %{http_code} --silent --output /dev/null --get --data-urlencode "values=[]" http://127.0.0.1:8888/)

if [ $response == 400 ]; then
    echo "test 05: passed"
else
    echo "test 05: failed"
fi

# test 06: testing when the list has only 1 element
response=$(curl --write-out %{http_code} --silent --output /dev/null --get --data-urlencode "values=[1]" http://127.0.0.1:8888/)

if [ $response == 200 ]; then
    echo "test 06: passed"
else
    echo "test 06: failed"
fi
