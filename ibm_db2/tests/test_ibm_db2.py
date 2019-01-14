# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.ibm_db2 import IbmDb2Check
from . import metrics

pytestmark = pytest.mark.integration


@pytest.mark.usefixtures('dd_environment')
def test_standard(aggregator, instance):
    check = IbmDb2Check('ibm_db2', {}, [instance])
    check.check(instance)

    for metric in metrics.STANDARD:
        aggregator.assert_metric_has_tag(metric, 'db:datadog')
        aggregator.assert_metric_has_tag(metric, 'foo:bar')

    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures('dd_environment')
def test_buffer_pool_tags(aggregator, instance):
    check = IbmDb2Check('ibm_db2', {}, [instance])
    check.check(instance)

    for metric in metrics.BUFFERPOOL:
        aggregator.assert_metric_has_tag_prefix(metric, 'bufferpool:')


@pytest.mark.usefixtures('dd_environment')
def test_table_space_tags(aggregator, instance):
    check = IbmDb2Check('ibm_db2', {}, [instance])
    check.check(instance)

    for metric in metrics.TABLESPACE:
        aggregator.assert_metric_has_tag_prefix(metric, 'tablespace:')


@pytest.mark.usefixtures('dd_environment')
def test_table_space_state_change(aggregator, instance):
    check = IbmDb2Check('ibm_db2', {}, [instance])
    check._table_space_states['USERSPACE1'] = 'test'
    check.check(instance)

    aggregator.assert_event('State of `USERSPACE1` changed from `test` to `NORMAL`.')
