# First edit tournament.py so that a single run performs more competitions

cp game_agent.py.greedy game_agent.py
python tournament.py > log/greedy.log 2>&1

cp game_agent.py.center_distance game_agent.py
python tournament.py > log/center-distance.log 2>&1

cp game_agent.py.position_distance game_agent.py
python tournament.py > log/position-distance.log 2>&1
