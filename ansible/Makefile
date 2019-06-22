## -- Variables -- ##

opts ?= $(args)

ifneq ("$(host)", "")
    opts := $(opts) --limit="$(host)"
else
    $(error Playbook runs must specify a target host.)
endif

ifneq ("$(step)", "")
    opts := $(opts) --tag="$(step)"
else
    $(error Playbook runs must specify a step.)
endif

## -- Commands -- ##

.PHONY: run
run:  ## make run [host=<ansible host limit>] [step=<ansible task tag>] [args=<ansible-playbook arguments>] # Run a playbook
	ansible-playbook playbook.yml --inventory-file=hosts.ini $(opts)
