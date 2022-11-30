user: hypercorn user --reload --debug --bind user.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
api: bin/litefs -config etc/primary.yml
api: bin/litefs -config etc/secondary.yml
api: bin/litefs -config etc/secondary2.yml