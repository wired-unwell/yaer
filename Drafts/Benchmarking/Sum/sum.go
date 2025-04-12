package main

// GPT-4o

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	result := 0
	for i:=1; i<10000000; i++ {
		result += i
	}
	elapsed := time.Since(start)
	fmt.Printf("\x1b[36mGo: %.6f seconds.\x1b[0m\n", elapsed.Seconds())
}
