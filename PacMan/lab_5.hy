(import [pandas :as pd]
        math
)

(setv data (pd.read_csv "game.csv" ))
(setv time (get data "Time"))
(setv score (get data "Score"))

(defn getMathExpectation[column]
    (/ (column.sum) (len column))
)

(defn square[num]
 (* num num)
)

(defn getDispersion[column]
    ( - (getMathExpectation (column.map square) ) (math.pow (getMathExpectation column ) 2) 
)) 

(
    print "Math Expectation on time:"
    (getMathExpectation time)
)

(
    print "Dispersion on score:"
    (getDispersion time)
)