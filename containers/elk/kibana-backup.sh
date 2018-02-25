#!/bin/bash
set -e

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

docker run \
	-it --rm \
	--net elk_default \
	-v ${SCRIPT_DIR}/backups:/opt/data \
	node bash -c "
		set -xe;
		npm install elasticdump -g;

		elasticdump \
			--input=http://elasticsearch:9200/.kibana \
			--output=/opt/data/kibana.data.json \
			--type=data;

		elasticdump \
			--input=http://elasticsearch:9200/.kibana \
			--output=/opt/data/kibana.mapping.json \
			--type=mapping
"