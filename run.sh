#!/bin/bash

docker run --rm \
  -v /etc/localtime:/etc/localtime:ro \
  -v "$(realpath $HOME/Projects/FinanceManager/data):/app/data" financemanager ingest

docker run --rm \
  -v /etc/localtime:/etc/localtime:ro \
  -v "$(realpath $HOME/Projects/FinanceManager/data):/app/data" financemanager categorize

docker run --rm \
  -v /etc/localtime:/etc/localtime:ro \
  -v "$(realpath $HOME/Projects/FinanceManager/data):/app/data" financemanager export

docker run --rm \
  -v /etc/localtime:/etc/localtime:ro \
  -v "$(realpath $HOME/Projects/FinanceManager/data):/app/data" financemanager status
