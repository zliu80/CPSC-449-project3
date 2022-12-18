user: hypercorn user --reload --debug --bind user.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
game1: bin/litefs -config etc/primary.yml
game2: bin/litefs -config etc/secondary.yml
game3: bin/litefs -config etc/secondary2.yml
leaderboard: hypercorn leaderboard --reload --debug --bind leaderboard.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
queue: rq worker --with-scheduler --verbose