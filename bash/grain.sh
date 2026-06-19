#!/bin/bash
# -eq is just for integer not string.
# String need to use ==
#to handle overflow or decimal => use bc
main () {
    n="$1"

    if [[ "$n" == "total" ]]; then
        # Hardcoded because Bash math overflows at 2^64
        total_grain="18446744073709551615"
        echo "$total_grain"
    elif [[ "$n" -gt 64 || "$n" -lt 1 ]]; then
        echo "Error: invalid input"
        exit 1
    else
       echo "2^($n - 1)" | bc
    fi
    
}

main "$@"