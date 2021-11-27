(import 
    [random [randrange]]
    [algo [Algorithm]]
    [level [Level]]
    [game_state [GameState]]
    math
)

(setv height 5)
(setv width 5)
(setv maxWals 5)
(setv player_coords (, 0 2))
(setv ghosts_coords [(, 3 2)])
(setv target (, (randrange 0 (- width 1)) (randrange 0 (- height 1))))


(defn levelGenerate []
    (setv matrix [])
    (setv wals 0)
    (lfor row (range height)
        (matrix.append (* ["."] width))
    )
    (while (< wals maxWals)
        (setv x (randrange 0 (- width 1)))
        (setv y (randrange 0 (- height 1)))
        (if (and (= x (get player_coords 0)) (= y (get player_coords 1)))
            (continue)
        )
        (if (and (= x (get (get ghosts_coords 0) 0)) (= y (get (get ghosts_coords 0) 0)))
            (continue)
        )
        (setv (get matrix y x) "=")
        (setv wals (+ wals 1))
    )
    (return matrix)
)

(setv matrix (levelGenerate))
(setv level (Level matrix width height))
(setv algo (Algorithm level))
(setv state (GameState matrix player_coords ghosts_coords))
(setv root_node (algo.generateTree state target))
(setv tree (algo.minimax root_node (- math.inf) math.inf 0))
(print root_node)

