# First edit tournament.py so that a single run performs more competitions

cp game_agent.py.more_moves game_agent.py
python tournament.py > log/more-moves.log 2>&1

cp game_agent.py.center_distance game_agent.py
python tournament.py > log/center-distance.log 2>&1

cp game_agent.py.position_distance game_agent.py
python tournament.py > log/position-distance.log 2>&1
