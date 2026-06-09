#!/bin/bash
#Description: find difference between (1+..+n)^2 and 1^2+...+n^2

main () {
    action="$1"
    n="$2"
    square_of_sum=$((   (n*(n+1)/2)**2    ))
    sum_of_square=$((   (n*(n+1)*(2*n+1)) / 6 ))
    if [[ "$action" == "square_of_sum" ]]; then
        echo "${square_of_sum}"
    elif [[ "$action" == "sum_of_squares" ]]; then
        echo "${sum_of_square}"
    else
        diff=$((square_of_sum - sum_of_square))
        echo "${diff}"
    fi
}

main "$@"