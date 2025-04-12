(let [start (os.clock)]
  (var result 0)
  (for [i 0 10000000]
    (set result (+ result i)
         )
    )
  (let [end (os.clock)]
    (print (- end start)
           )
    )
  )
