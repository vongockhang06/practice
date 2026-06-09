#!/bin/bash

main () {
    n="$1"
    temp="$n"
    len="${#1}"
    amstrong_num=0
    while [[ "$temp" != 0 ]]; do
        amstrong_num=$((amstrong_num+(temp%10)**len))
        temp=$((temp/10))
    done
    if [[ "$amstrong_num" == "$n" ]]; then
        echo "$n is an Armstrong number"
    else
        echo "$n is not an Armstrong number"
    fi
}

main "$@"

