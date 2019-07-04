#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "monitor.h"

int main(int argc, const char *argv[])
{
	int id = 0;
	int t = 0;
	int64_t v = 0;

	moni_init();

	id = 10000;
	moni_add_value(id, 1);
	t = moni_get_type(id);
	v = moni_get_value(id);
	printf("id=%d, t=%d, v=%lu\n", id, t, v);

	id = 10001;
	moni_set_value(id, 3);
	t = moni_get_type(id);
	v = moni_get_value(id);
	printf("id=%d, t=%d, v=%lu\n", id, t, v);


	printf("walk:\n");
	int row = moni_get_row();
	int col = moni_get_col();
	int row_idx, col_idx;
	for (row_idx = 0; row_idx < row; row_idx++) {
		for (col_idx = 0; col_idx < col; col_idx++) {
			const Node *n = moni_walk(row_idx, col_idx);
			if (n != NULL && n->k != 0) {
				printf("id=%d, t=%d, v=%lu\n", n->k, n->t, n->v);
			}
		}
	}

	return 0;
}
