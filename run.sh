# First edit tournament.py so that a single run performs more competitions

cp game_agent.py.1 game_agent.py
python tournament.py > log/1.log 2>&1

cp game_agent.py.2 game_agent.py
python tournament.py > log/2.log 2>&1

cp game_agent.py.3 game_agent.py
python tournament.py > log/3.log 2>&1

cp game_agent.py.4 game_agent.py
python tournament.py > log/4.log 2>&1

cp game_agent.py.5 game_agent.py
python tournament.py > log/5.log 2>&1
