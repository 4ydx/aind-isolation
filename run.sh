cp game_agent.py.more_moves game_agent.py
for i in {0..9}; do
	python tournament.py > log/more-moves-$i.log 2>&1
done

cp game_agent.py.center_distance game_agent.py
for i in {0..9}; do
	python tournament.py > log/center-distance-$i.log 2>&1
done

cp game_agent.py.position_distance game_agent.py
for i in {0..9}; do
	python tournament.py > log/position-distance-$i.log 2>&1
done
