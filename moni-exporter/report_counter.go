package main

import (
	"fmt"
	"os"
	"strconv"

	"moni-exporter/gomonitor"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Printf("Usage: %s id value\n", os.Args[0])
		return
	}
	id, err := strconv.ParseInt(os.Args[1], 10, 64)
	if err != nil {
		fmt.Printf("id param error\n")
		return
	}
	value, err := strconv.ParseInt(os.Args[2], 10, 64)
	if err != nil {
		fmt.Printf("value param error\n")
		return
	}
	gomonitor.Add(int(id), value)
}
