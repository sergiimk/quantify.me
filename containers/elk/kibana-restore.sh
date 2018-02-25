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
			--input=/opt/data/kibana.mapping.json \
			--output=http://elasticsearch:9200/.kibana \
			--type=mapping

		elasticdump \
			--input=/opt/data/kibana.data.json \
			--output=http://elasticsearch:9200/.kibana \
			--type=data;
"