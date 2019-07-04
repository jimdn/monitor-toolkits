#ifndef __MONITOR_H__
#define __MONITOR_H__

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

#pragma pack(1)
typedef struct _Node {
	int32_t k;  // key
	int32_t t;  // type, 0-counter 1-gauge
	int64_t v;  // value
} Node;
#pragma pack()

int moni_init();

int64_t moni_get_value(int id);

int moni_get_type(int id);

int moni_add_value(int id, int64_t value);

int moni_set_value(int id, int64_t value);

int moni_set_type(int id, int type);

int moni_get_row();

int moni_get_col();

const Node *moni_walk(int row_index, int col_index);

#ifdef __cplusplus
}
#endif

#endif /* __MONITOR_H__ */
