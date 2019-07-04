package gomonitor

/*
#cgo CFLAGS: -O2
#include <stdlib.h>
#include <stdint.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#pragma pack(1)
typedef struct _Node {
	int32_t k;  // key
	int32_t t;  // type, 0-counter 1-gauge
	int64_t v;  // value
} Node;
#pragma pack()

const static key_t g_key = 0x15fee;
const static int g_mods[] = {
	1999, 1997, 1993, 1987, 1979, 1973, 1951, 1949, 1933, 1931,
	1913, 1907, 1901, 1889, 1879, 1877, 1873, 1871, 1867, 1861,
	1847, 1831, 1823, 1811, 1801, 1789, 1787, 1783, 1777, 1759,
	1753, 1747, 1741, 1733, 1723, 1721, 1709, 1699, 1697, 1693
};
const static int g_row = 40;
const static int g_col = 2000;

static void *g_table = NULL;

static int init() {
	// initialized:
	//   0 - not init
	//   1 - init ing
	//   2 - init finish
	static int initialized = 0;
	if (initialized == 2) {
		return 1;
	} else if (initialized == 1) {
		return -1;
	} else if (!__sync_bool_compare_and_swap(&initialized, 0, 1)) {
		return -2;
	}
	const int size = g_row * g_col * sizeof(Node);
	int shmid = shmget(g_key, size, 0666);
	if (shmid == -1) {
		if (errno != ENOENT) {
			initialized = 0;
			return -3;
		}
		shmid = shmget(g_key, size, 0666|IPC_CREAT);
		if (shmid == -1) {
			initialized = 0;
			return -4;
		}
	}
	g_table = shmat(shmid, NULL, 0);
	if (g_table == (void *)-1) {
		initialized = 0;
		return -5;
	}
	initialized = 2;
	return 0;
}

// only find, not allocate
static Node* find(int id) {
	if (id <= 0) {
		return NULL;
	}
	if (init(g_row, g_col) >= 0) {
		int x = 0;
		for (x = 0; x < g_row; x++) {
			Node *ptr = (Node *)(g_table) + x * g_col + id % g_mods[x];
			if (ptr->k == id) {
				return ptr;
			}
		}
	}
	return NULL;
}

// find and allocate
// id : attrid
// depth : recursive depth
static Node* find_alloc(int id, int depth) {
	if (id <= 0 || depth > 10) {
		return NULL;
	}
	if (init(g_row, g_col) >= 0) {
		int x = 0;
		for (x = 0; x < g_row; x++) {
			Node *ptr = (Node *)(g_table) + x * g_col + id % g_mods[x];
			if (ptr->k == id) {
				return ptr;
			} else if (ptr->k == 0) {
				if (__sync_bool_compare_and_swap(&ptr->k, 0, id)) {
					return ptr;
				} else {
					return find_alloc(id, (depth+1));
				}
			}
		}
	}
	return NULL;
}


int moni_init()
{
	return init();
}

int64_t moni_get_value(int id)
{
	Node *ptr = find(id);
	if (!ptr) {
		return -1;
	}
	return ptr->v;
}

int moni_get_type(int id)
{
	Node *ptr = find(id);
	if (!ptr) {
		return -1;
	}
	return ptr->t;
}

int moni_add_value(int id, int64_t value)
{
	Node *ptr = find_alloc(id, 0);
	if (!ptr) {
		return -1;
	}
	if (value <= 0) {
		return 0;
	}
	int x = 0;
	for (x = 0; x < 10; x++) {
		int64_t old = ptr->v;
		int64_t new = ptr->v + value;
		if (__sync_bool_compare_and_swap(&ptr->v, old, new))
			return new;
	}
	return -2;
}

int moni_set_value(int id, int64_t value)
{
	Node *ptr = find_alloc(id, 0);
	if (!ptr) {
		return -1;
	}
	// set type=1
	int x = 0;
	for (x = 0; x < 10; x++) {
		int old = ptr->t;
		int new = 1;
		if (__sync_bool_compare_and_swap(&ptr->t, old, new)) {
			break;
		}
	}
	// set value
	if (x < 10) {
		int y = 0;
		for (y = 0; y < 10; y++) {
			int64_t old = ptr->v;
			int64_t new = value;
			if (__sync_bool_compare_and_swap(&ptr->v, old, new))
				return new;
		}
	}
	return -2;
}

int moni_set_type(int id, int type)
{
	Node *ptr = find_alloc(id, 0);
	if (!ptr) {
		return -1;
	}
	int x = 0;
	for (x = 0; x < 10; x++) {
		int old = ptr->t;
		int new = type;
		if (__sync_bool_compare_and_swap(&ptr->t, old, new))
			return new;
	}
	return -2;
}

int moni_get_row()
{
	return g_row;
}

int moni_get_col()
{
	return g_col;
}

const Node *moni_walk(int row_index, int col_index)
{
	if (init(g_row, g_col) >= 0) {
		if (row_index < g_row && col_index < g_mods[row_index]) {
			Node *ptr = (Node *)(g_table) + row_index * g_col + col_index;
			return ptr;
		}
	}
	return NULL;
}

int moni_get_id(int row_index, int col_index){
	int id = 0;
	if (init(g_row, g_col) >= 0) {
		if (row_index < g_row && col_index < g_mods[row_index]) {
			Node *ptr = (Node *)(g_table) + row_index * g_col + col_index;
			id = ptr->k;
		}
	}
	return id;
}
*/
import "C"

func init() {
	C.init()
}

func Get(id int) int64 {
	v := C.moni_get_value(C.int(id))
	return int64(v)
}

func GetType(id int) (int) {
	t := C.moni_get_type(C.int(id))
	return int(t)
}

func Add(id int, value int64) int64 {
	v := C.moni_add_value(C.int(id), C.long(value))
	return int64(v)
}

func Set(id int, value int64) int64 {
	v := C.moni_set_value(C.int(id), C.long(value))
	return int64(v)
}

func SetType(id, typ int) int64 {
	v := C.moni_set_type(C.int(id), C.int(typ))
	return int64(v)
}

func MaxRow() int {
	return int(C.moni_get_row())
}

func MaxCol() int {
	return int(C.moni_get_col())
}

func AttrWalk(rowIdx, colIdx int) (int, int, int64) {
	id := int(C.moni_get_id(C.int(rowIdx), C.int(colIdx)))
	if id != 0 {
		t := int(C.moni_get_type(C.int(id)))
		v := int64(C.moni_get_value(C.int(id)))
		return id, t, v
	}
	return 0, 0, 0
}
