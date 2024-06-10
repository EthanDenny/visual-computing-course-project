int find_match(char* dic, long dic_size, char* buf, int buf_size, int* match_length) {
    char potential_indices[dic_size];
    char return_now = 1;

    for (long i = 0; i < dic_size; i++) {
        if (dic[i] == buf[0]) {
            potential_indices[i] = 1;
            return_now = 0;
        } else {
            potential_indices[i] = 0;
        }
    }

    if (return_now) {
        return 0;
    }

    long potential_return;

    for (int l = 2; l <= buf_size; l++) {
        potential_return = -1;
        return_now = 1;

        for (long i = 0; i < dic_size; i++) {
            if (potential_indices[i]) {
                if (i <= dic_size - l) {
                    if (dic[i + l - 1] == buf[l - 1]) {
                        return_now = 0;
                    } else {
                        potential_return = i;
                        potential_indices[i] = 0;
                    }
                } else {
                    potential_return = i;
                    potential_indices[i] = 0;
                    break;
                }
            }
        }

        if (return_now) {
            *match_length = l - 1;
            return dic_size - potential_return;
        }
    }

    *match_length = potential_return < buf_size ? potential_return : buf_size - 1; // Won't verify without this?
    return dic_size - potential_return;
}
