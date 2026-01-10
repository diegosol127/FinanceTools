#!/bin/bash
docker run --rm -v "$(realpath $HOME/Projects/FinanceManager/data):/app/data" financemanager
